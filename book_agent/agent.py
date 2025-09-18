from google.adk.agents import Agent

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

from qdrant_client import QdrantClient
client = QdrantClient()

def get_best_sellers(query: str):
    """
    주어진 주제에 대해 베스트셀러 책 3권을 Qdrant에서 검색하여 반환합니다.

    Args:
        query (str): 검색할 주제
        limit (int): 반환할 책의 수 (기본값: 3)
    Returns:
        list[dict]: 베스트셀러 책 목록
    """
    results = client.query_points(
        collection_name="best-seller-books",
        query=model.encode(query).tolist(),
        limit=3,
    ).points
    books = [point.payload['title'] for point in results]
    return books

root_agent = Agent(
    name="book_agent",
    model="gemini-2.0-flash",
    instruction="사용자의 베스트셀러에 관한 질문에 답하세요.\n" \
    "그리고 나온 결과를 한줄에 하나씩 순위와 함께 출력하세요.",
    tools=[get_best_sellers],
)



