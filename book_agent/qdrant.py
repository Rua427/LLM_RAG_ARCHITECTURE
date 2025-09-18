import json
import os

# 현재 스크립트 파일의 디렉토리 경로를 가져옵니다.
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# JSON 파일의 절대 경로를 구성합니다.
_JSON_PATH = os.path.join(_CURRENT_DIR, "best-seller-books.json")

with open(_JSON_PATH, "r", encoding="utf-8") as f:
    books = json.load(f)

# pip install sentence-transformers hf_xet
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from qdrant_client.models import PointStruct
points = [PointStruct(id=idx+1, vector=model.encode(book["description"]).tolist(),
                      payload=book) for idx, book in enumerate(books)]

client = QdrantClient(url="http://localhost:6333")


client.recreate_collection(
    collection_name="best-seller-books",
    vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.DOT))

client.upsert(collection_name="best-seller-books", points=points)

result = client.query_points(
    collection_name="best-seller-books",
    query=model.encode("인공지능").tolist(),
    limit=3,
)

print(result)
    