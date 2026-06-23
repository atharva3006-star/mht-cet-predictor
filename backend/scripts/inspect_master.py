import pandas as pd

df = pd.read_csv("app/data/processed/mhtcet_cutoffs_master.csv")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print()
print(df.head(5).to_string())
print()
print("Years:", df["year"].unique())
print("Rounds:", df["round"].unique())
print("Sample home universities:", df["college_home_university"].unique()[:15])