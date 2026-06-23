import sys
sys.path.insert(0, ".")
from app.core.prediction_engine import PredictionEngine

engine = PredictionEngine("app/data/processed/mhtcet_cutoffs_master.csv")
results = engine.predict(
    percentile=88.5,
    category="GOPENS",
    home_university="Sant Gadge Baba Amravati University"
)
print("Total results:", len(results))
for r in results[:10]:
    print(r.bucket, "|", r.college_name, "|", r.branch_name, "|", r.seat_pool, "|", r.latest_cutoff_percentile, "|", r.trend)