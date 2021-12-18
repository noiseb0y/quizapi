import pandas as pd

df = pd.read_csv("combined_season1-37.tsv", sep="\t")
print(df.columns)

cleaned_df = pd.DataFrame()

cleaned_df["category"] = df["category"].str.lower()
cleaned_df["value"] = df["value"] 
cleaned_df["question"] = df["answer"] 
cleaned_df["answer"] = df["question"]

cleaned_df.to_csv("cleaned.csv", index=False)