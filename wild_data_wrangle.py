from datasets import load_dataset

ds = load_dataset("allenai/WildChat", split="train")
sample = ds.shuffle(seed=42).select(range(5000))
df_wild = sample.to_pandas()
df_english = df_wild[df_wild["conversation"].apply(lambda x: x[0]["language"] == "English")]

df_english = df_wild[df_wild["conversation"].apply(lambda x: x[0]["language"] == "English")].copy()

df_english["prompt"] = df_english["conversation"].apply(lambda x: x[0]["content"])
df_english["response"] = df_english["conversation"].apply(lambda x: x[1]["content"] if len(x) > 1 else "")

df_english[["prompt", "response"]].to_csv("wildchat_prompts.csv", index=False)

print(f"Saved {len(df_english)} rows")
print(df_english[["prompt", "response"]].head(3))