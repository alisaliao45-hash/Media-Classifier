'''
1. find dataset - 
2. ensure dataset is unbiased through embedding and plotting
    from sentence_transformers import SentenceTransformer
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(df["text"].tolist())

    # Reduce to 2D for visualization
    pca = PCA(n_components=2)
    coords = pca.fit_transform(embeddings)

    plt.scatter(coords[:, 0], coords[:, 1], alpha=0.3)
    plt.title("Prompt Space Coverage")
    plt.show()
2.5. scratch that idea and find an already unbiased dataset.
    The Wild dataset was:
     - hosted by Hugging Face and made public
     - collected through use of two chatbot services
     - didn't require users to make an account to use services
     - users were given a consent agreement
3. label data 
4. Make model
    Naive Bayes — first attempt
    Logistic Regression — more accuracy
    SVM — even more accuracy
    DistilBERT fine-tuned — if over 200+ data

Acknowledgements:
- The categories of media are quite broad. For example
within text, we can have essays, lists, summaries, etc.
In the future we also must consider multimedia such as
infographics, slidedecks, etc. This is only a starting point that may not effectively capture
this nuance.

'''

#to see progress so far

import sqlite3
import pandas as pd

conn = sqlite3.connect("labeling.db")

# All prompts with their current vote counts
df = pd.read_sql_query("SELECT * FROM prompts WHERE total_votes > 0", conn)

# Determine the winning label per row
label_cols = ["votes_diagram", "votes_video", "votes_audio", "votes_text"]
df["label"] = df[label_cols].idxmax(axis=1).str.replace("votes_", "")

print(df[["id", "text", "label", "total_votes"]])

conn.close()

df.to_csv("labeled_results.csv", index=False)

