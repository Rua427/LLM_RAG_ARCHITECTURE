import dotenv
dotenv.load_dotenv()


import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent

from agent import root_agent, problem



async def main():
    """Runs the algorithm problem solver agent and prints the final documentation."""
    runner = InMemoryRunner(agent=root_agent)
    print("알고리즘 문제 해결 에이전트를 실행합니다...")
    print("=" * 30)
    print(f"문제:\n{problem}")
    print("=" * 30)

    # 에이전트 실행
    final_event = await runner.run_async(
        initial_message=UserContent(f"다음 문제를 해결해 주세요: {problem}")
    )

    # 최종 결과 출력
    if final_event and final_event.content:
        documentation = final_event.content.parts[0].text
        print("\n\n=== 최종 보고서 ===")
        print(documentation)
    else:
        print("에이전트 실행 중 오류가 발생했거나 최종 결과를 생성하지 못했습니다.")


if __name__ == "__main__":
    asyncio.run(main())
