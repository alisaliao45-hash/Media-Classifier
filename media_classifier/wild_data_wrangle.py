from datasets import load_dataset

ds = load_dataset("allenai/WildChat", split="train")
sample = ds.shuffle(seed=42).select(range(5000))
df_wild = sample.to_pandas()
df_english = df_wild[df_wild["conversation"].apply(lambda x: x[0]["language"] == "English")]

# Extract the prompt
df_english = df_english.copy()
df_english["prompt"] = df_english["conversation"].apply(lambda x: x[0]["content"])

# Save to CSV
df_english[["prompt"]].to_csv("wildchat_prompts.csv", index=False)

print(f"Saved {len(df_english)} English prompts")
