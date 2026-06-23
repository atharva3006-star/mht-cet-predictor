"""
Scans one or more parsed cutoff CSVs and reports any 'category' code
that is NOT yet present in app/data/meta/category_map.json.

Usage:
    python scripts/check_unmapped_categories.py app/data/processed/*.csv
"""
import csv
import json
import sys
from pathlib import Path

MAP_PATH = Path(__file__).resolve().parent.parent / "app" / "data" / "meta" / "category_map.json"


def main(csv_paths):
    with open(MAP_PATH) as f:
        cat_map = json.load(f)["categories"]

    seen = set()
    for path in csv_paths:
        with open(path) as f:
            for row in csv.DictReader(f):
                seen.add(row["category"])

    unmapped = sorted(c for c in seen if c not in cat_map)
    if unmapped:
        print(f"⚠  {len(unmapped)} category codes found in data but missing from category_map.json:")
        for c in unmapped:
            print(f"   - {c}")
        print("\nAdd these manually to category_map.json with a label before going live.")
    else:
        print("✅ All category codes in the data are already mapped.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_unmapped_categories.py <csv1> [csv2 ...]")
        sys.exit(1)
    main(sys.argv[1:])
