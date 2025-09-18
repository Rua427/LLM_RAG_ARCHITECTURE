# pip install qdrant-client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

points=[
    PointStruct(id=0, vector=[1, 1], payload={"planet": "Mercury"}),
    PointStruct(id=1, vector=[-1, 2], payload={"planet": "Venus"}),
    PointStruct(id=2, vector=[3, 1], payload={"planet": "Earth"}),
    PointStruct(id=3, vector=[-2, -3], payload={"planet": "Mars"}),
    PointStruct(id=4, vector=[4, -4], payload={"planet": "Jupiter"}),
    PointStruct(id=5, vector=[6, 4], payload={"planet": "Saturn"}),
]


client = QdrantClient(url="http://localhost:6333")


# client.recreate_collection(
#     collection_name="planets",
#     vectors_config=VectorParams(size=2, distance=Distance.EUCLID),
# )

# client.upsert(collection_name="planets", points=points)

result = client.query_points(
    collection_name="planets",
    query=[2, 1],
    limit=3,
)

print(result)