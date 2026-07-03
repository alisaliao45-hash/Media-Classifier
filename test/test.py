from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from huggingface_hub import hf_hub_download
from huggingface_hub import login
login()

from datasets import load_dataset

ds = load_dataset("reddgr/nli-chatbot-prompt-categorization")
df = ds["train"].to_pandas()

# Embed the prompts
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df["text"].tolist(), show_progress_bar=True)

# Reduce to 2D
pca = PCA(n_components=2)
coords = pca.fit_transform(embeddings)

# Plot
plt.figure(figsize=(10, 7))
plt.scatter(coords[:, 0], coords[:, 1], alpha=0.3, s=10)
plt.title("Prompt Space Coverage")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.tight_layout()
plt.show()