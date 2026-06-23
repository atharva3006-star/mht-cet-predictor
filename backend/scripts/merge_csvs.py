import glob
import json
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE / "app" / "data" / "processed"
MAP_PATH = BASE / "app" / "data" / "meta" / "category_map.json"

def main():
    with open(MAP_PATH) as f:
        excluded = set(json.load(f)["excluded_categories"]["codes"])

    files = sorted(glob.glob(str(PROCESSED_DIR / "cap*_20*.csv")))
    files = [f for f in files if "master" not in f and "SAMPLE" not in f]

    frames = [pd.read_csv(f) for f in files]
    df = pd.concat(frames, ignore_index=True)

    before = len(df)
    df = df[~df["category"].isin(excluded)].copy()
    after = len(df)

    out_path = PROCESSED_DIR / "mhtcet_cutoffs_master.csv"
    df.to_csv(out_path, index=False)

    print(f"Merged {len(files)} files -> {after} rows (dropped {before - after} rows)")
    print("Files used:", files)

if __name__ == "__main__":
    main()