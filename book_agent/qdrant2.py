# pip install sentence-transformers hf_xet
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

from qdrant_client import QdrantClient


client = QdrantClient(url="http://localhost:6333")

results = client.query_points(
    collection_name="best-seller-books",
    query=model.encode("가장 비싼 책들 알려줘").tolist(),
    limit=3,
)

print(results)
    