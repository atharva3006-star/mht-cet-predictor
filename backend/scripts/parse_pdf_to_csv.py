"""
MHT-CET CAP Cutoff PDF Parser
-------------------------------
Converts official State CET Cell cutoff PDFs (CAP-1, CAP-2, CAP-3, CAP-4)
into a single unified CSV.

Usage:
    python parse_pdf_to_csv.py --pdf CAP-1_2024.pdf --year 2024 --round 1 --out cap1_2024.csv
    (run once per PDF, then concatenate / append all outputs into one master CSV)

Output schema (one row per category-cell):
    year, round, college_code, college_name, branch_code, branch_name,
    college_status, college_home_university, seat_pool, category,
    stage, cutoff_rank, cutoff_percentile
"""

import argparse
import csv
import re
import sys
import pdfplumber

SECTION_HEADERS = {
    "State Level": "STATE",
    "Home University Seats Allotted to Home University Candidates": "HOME_TO_HOME",
    "Home University Seats Allotted to Other Than Home University Candidates": "HOME_TO_OTHER",
    "Other Than Home University Seats Allotted to Other Than Home University Candidates": "OTHER_TO_OTHER",
}

COLLEGE_RE = re.compile(r'^(\d{5})\s*-\s*(.+)$')
BRANCH_RE = re.compile(r'^(\d{10})\s*-\s*(.+)$')
STATUS_RE = re.compile(r'^Status:\s*(.+?)\s+Home University\s*:\s*(.*)$')
STAGE_TOKEN_RE = re.compile(r'^(I|II|III|IV|V)$')
PERCENTILE_RE = re.compile(r'\(([\d.]+)\)')

COL_TOL = 28  # x-distance tolerance (points) for matching a value to a header column


def lines_from_words(words, tol=2.5):
    """Group words on a page into visual lines based on vertical position."""
    words = sorted(words, key=lambda w: (round(w['top'], 1), w['x0']))
    lines, cur, cur_top = [], [], None
    for w in words:
        if cur_top is None or abs(w['top'] - cur_top) <= tol:
            cur.append(w)
            cur_top = w['top'] if cur_top is None else cur_top
        else:
            lines.append(sorted(cur, key=lambda w: w['x0']))
            cur, cur_top = [w], w['top']
    if cur:
        lines.append(sorted(cur, key=lambda w: w['x0']))
    return lines


def line_text(line):
    return " ".join(w['text'] for w in line)


def match_columns(value_words, header_cols):
    """
    Map each value word to the nearest header column (by x0) within COL_TOL.
    header_cols: list of (x0, category_code)
    Returns dict {category_code: text}
    """
    result = {}
    for w in value_words:
        best_cat, best_dist = None, None
        for x0, cat in header_cols:
            d = abs(w['x0'] - x0)
            if d <= COL_TOL and (best_dist is None or d < best_dist):
                best_cat, best_dist = cat, d
        if best_cat:
            result[best_cat] = w['text']
    return result


def parse_pdf(path, year, round_num):
    rows = []
    college_code = college_name = None
    branch_code = branch_name = None
    status = home_university = None
    seat_pool = None
    header_cols = None  # list of (x0, category)
    pending_stage = None
    pending_ranks = None  # dict category -> rank text, awaiting percentile line

    with pdfplumber.open(path) as pdf:
        total = len(pdf.pages)
        for pno, page in enumerate(pdf.pages):
            words = page.extract_words()
            if not words:
                continue
            lines = lines_from_words(words)

            for line in lines:
                text = line_text(line)

                # --- College header ---
                m = COLLEGE_RE.match(text)
                if m and len(m.group(1)) == 5:
                    college_code, college_name = m.group(1), m.group(2).strip()
                    branch_code = branch_name = None
                    header_cols = None
                    continue

                # --- Branch header ---
                m = BRANCH_RE.match(text)
                if m:
                    branch_code, branch_name = m.group(1), m.group(2).strip()
                    header_cols = None
                    continue

                # --- Status line ---
                m = STATUS_RE.match(text)
                if m:
                    status, home_university = m.group(1).strip(), m.group(2).strip()
                    continue

                # --- Section header (seat pool) ---
                if text.strip() in SECTION_HEADERS:
                    seat_pool = SECTION_HEADERS[text.strip()]
                    header_cols = None
                    continue

                # --- Column header row (contains "Stage" + category codes) ---
                if "Stage" in line_text(line).split() and any(
                    re.match(r'^[A-Z]+[A-Z0-9]*[SHO]$', w['text']) for w in line
                ):
                    header_cols = [
                        (w['x0'], w['text']) for w in line if w['text'] != "Stage"
                    ]
                    pending_stage, pending_ranks = None, None
                    continue

                if header_cols is None:
                    continue  # skip noise (legends, footers, titles) outside a table

                # --- Rank row: starts/ends with roman numeral stage marker ---
                stage_words = [w for w in line if STAGE_TOKEN_RE.match(w['text'])]
                if stage_words and not text.strip().startswith("("):
                    stage = stage_words[0]['text']
                    value_words = [w for w in line if not STAGE_TOKEN_RE.match(w['text'])]
                    ranks = match_columns(value_words, header_cols)
                    pending_stage, pending_ranks = stage, ranks
                    continue

                # --- Percentile row: all tokens are "(number)" ---
                if PERCENTILE_RE.search(text) and pending_ranks is not None:
                    value_words = []
                    for w in line:
                        mm = PERCENTILE_RE.match(w['text'])
                        if mm:
                            value_words.append({'x0': w['x0'], 'text': mm.group(1)})
                    percentiles = match_columns(value_words, header_cols)

                    for cat, rank in pending_ranks.items():
                        rows.append({
                            "year": year,
                            "round": round_num,
                            "college_code": college_code,
                            "college_name": college_name,
                            "branch_code": branch_code,
                            "branch_name": branch_name,
                            "college_status": status,
                            "college_home_university": home_university,
                            "seat_pool": seat_pool,
                            "category": cat,
                            "stage": pending_stage,
                            "cutoff_rank": rank,
                            "cutoff_percentile": percentiles.get(cat),
                        })
                    pending_stage, pending_ranks = None, None
                    continue

            page.flush_cache()
            page.close()

            if (pno + 1) % 100 == 0:
                print(f"  processed {pno+1}/{total} pages...", file=sys.stderr)

    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--year", required=True, type=int)
    ap.add_argument("--round", required=True, type=int)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    print(f"Parsing {args.pdf} ...", file=sys.stderr)
    rows = parse_pdf(args.pdf, args.year, args.round)
    print(f"Extracted {len(rows)} rows.", file=sys.stderr)

    fieldnames = [
        "year", "round", "college_code", "college_name", "branch_code", "branch_name",
        "college_status", "college_home_university", "seat_pool", "category",
        "stage", "cutoff_rank", "cutoff_percentile",
    ]
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
