"""
Prediction Engine for MHT-CET College Predictor
-------------------------------------------------
Given a student's percentile, category, home university, and optional
branch/region filters, returns a bucketed list of colleges:
    - Safe      : comfortably above last year's cutoff
    - Target    : within margin of last year's cutoff
    - Reach     : a stretch, but not unrealistic

Core ideas:
1. Percentile-dependent margin (tighter bands at the top, since the field
   is denser there and a fixed absolute margin would be misleading).
2. Uses the most recent year as the base cutoff, blended with the prior
   year via a simple trend adjustment (so a single anomalous year doesn't
   dominate the prediction).
3. Home-University aware: only considers the seat_pool relevant to the
   student (STATE + HOME_TO_HOME if they belong to the college's home
   university, else STATE + OTHER_TO_OTHER).
"""

from dataclasses import dataclass, field
from typing import Optional
import pandas as pd


# ---------------------------------------------------------------------------
# Margin table — your original logic, formalized
# ---------------------------------------------------------------------------
def get_margin(percentile: float) -> float:
    """Returns the +/- percentile margin band based on the student's score bracket."""
    if percentile >= 98:
        return 0.5
    elif percentile >= 96:
        return 1.0
    elif percentile >= 90:
        return 1.5
    else:
        return 2.0


# ---------------------------------------------------------------------------
# Data container for one prediction result row
# ---------------------------------------------------------------------------
@dataclass
class PredictionResult:
    college_code: str
    college_name: str
    branch_code: str
    branch_name: str
    region: Optional[str]
    college_home_university: Optional[str]
    category: str
    seat_pool: str
    latest_cutoff_percentile: float
    previous_cutoff_percentile: Optional[float]
    trend: str  # "rising" | "falling" | "stable" | "new"
    bucket: str  # "Safe" | "Target" | "Reach"


class PredictionEngine:
    def __init__(self, master_csv_path: str, region_map_path: Optional[str] = None):
        self.df = pd.read_csv(master_csv_path, dtype={"branch_code": str, "college_code": str})
        self.df["cutoff_percentile"] = pd.to_numeric(
            self.df["cutoff_percentile"], errors="coerce"
        )
        self.df = self.df.dropna(subset=["cutoff_percentile"])

        # Use only the LAST round of each year as that year's representative
        # cutoff (final round = most settled cutoff for that year).
        self._latest_round_per_year = (
            self.df.groupby("year")["round"].max().to_dict()
        )

        self.region_map = {}
        if region_map_path:
            import json
            with open(region_map_path) as f:
                self.region_map = json.load(f)

    def _region_for(self, college_code: str) -> Optional[str]:
        return self.region_map.get(str(college_code))

    def _relevant_pools(self, is_home_university: bool) -> list[str]:
        if is_home_university:
            return ["STATE", "HOME_TO_HOME", "HOME_TO_OTHER"]
        return ["STATE", "OTHER_TO_OTHER"]

    def predict(
        self,
        percentile: float,
        category: str,
        home_university: Optional[str] = None,
        branch_keyword: Optional[str] = None,
        region: Optional[str] = None,
    ) -> list[PredictionResult]:
        df = self.df
        df = df[df["category"] == category]

        if branch_keyword:
            df = df[df["branch_name"].str.contains(branch_keyword, case=False, na=False)]

        if df.empty:
            return []

        years = sorted(df["year"].unique())
        if not years:
            return []
        latest_year = years[-1]
        prev_year = years[-2] if len(years) > 1 else None

        latest_round = self._latest_round_per_year[latest_year]
        latest_df = df[(df["year"] == latest_year) & (df["round"] == latest_round)]

        prev_df = pd.DataFrame()
        if prev_year is not None:
            prev_round = self._latest_round_per_year[prev_year]
            prev_df = df[(df["year"] == prev_year) & (df["round"] == prev_round)]

        margin = get_margin(percentile)
        lower_bound = max(0.0, percentile - 2 * margin)  # how far down we still show as "Reach"

        results: list[PredictionResult] = []
        seen_keys = set()

        for _, row in latest_df.iterrows():
            college_code = row["college_code"]
            branch_code = row["branch_code"]
            seat_pool = row["seat_pool"]
            college_home_uni = row.get("college_home_university")

            is_home = bool(
                home_university
                and isinstance(college_home_uni, str)
                and college_home_uni.strip().lower() == home_university.strip().lower()
            )
            allowed_pools = self._relevant_pools(is_home)
            if seat_pool not in allowed_pools:
                continue

            cutoff = row["cutoff_percentile"]
            if cutoff < lower_bound:
                continue  # too far below to be realistic even as a reach

            # Region filter (optional)
            college_region = self._region_for(college_code)
            if region and college_region and region.strip().lower() != college_region.strip().lower():
                continue

            # Find matching previous-year cutoff for trend
            prev_cutoff = None
            if not prev_df.empty:
                match = prev_df[
                    (prev_df["college_code"] == college_code)
                    & (prev_df["branch_code"] == branch_code)
                    & (prev_df["seat_pool"] == seat_pool)
                ]
                if not match.empty:
                    prev_cutoff = float(match.iloc[0]["cutoff_percentile"])

            trend = "new"
            if prev_cutoff is not None:
                diff = cutoff - prev_cutoff
                if diff > 0.5:
                    trend = "rising"
                elif diff < -0.5:
                    trend = "falling"
                else:
                    trend = "stable"

            # Bucket classification
            if percentile > cutoff + margin:
                bucket = "Safe"
            elif percentile >= cutoff - margin:
                bucket = "Target"
            else:
                bucket = "Reach"

            key = (college_code, branch_code, seat_pool)
            if key in seen_keys:
                continue
            seen_keys.add(key)

            def _clean(v):
                """Convert pandas NaN to None so Pydantic doesn't choke on float('nan') in a str field."""
                if v is None:
                    return None
                if isinstance(v, float) and pd.isna(v):
                    return None
                return v

            results.append(PredictionResult(
                college_code=str(college_code),
                college_name=_clean(row["college_name"]),
                branch_code=str(branch_code),
                branch_name=_clean(row["branch_name"]),
                region=_clean(college_region),
                college_home_university=_clean(college_home_uni),
                category=category,
                seat_pool=seat_pool,
                latest_cutoff_percentile=cutoff,
                previous_cutoff_percentile=prev_cutoff,
                trend=trend,
                bucket=bucket,
            ))

        # Sort: Safe first (closest to cutoff), then Target, then Reach
        bucket_order = {"Safe": 0, "Target": 1, "Reach": 2}
        results.sort(key=lambda r: (bucket_order[r.bucket], -r.latest_cutoff_percentile))
        return results
