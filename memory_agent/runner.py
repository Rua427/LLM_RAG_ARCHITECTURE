import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)
    session = await runner.session_service.create_session(app_name=runner.app_name, user_id="user1")

    print("일상적인 대화를 하는 에이전트 입니다.\n종료하려면 'exit' 또는 'quit'을 입력하세요.")
    print("새로운 대화를 시작하려면 new를 입력하세요")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat.")
            break
        
        elif user_input.lower() == "new":
            # 현재 세션을 가져옴
            session = await runner.session_service.get_session(app_name=runner.app_name, user_id=session.user_id, session_id=session.id)

            # 세션 메모리에 저장
            await runner.memory_service.add_session_to_memory(session)

            for event in session.events:
                print("-" * 20)
                print(f"{event.content.role}: {event.content}")
                

            # 새로운 세션 생성
            session = await runner.session_service.create_session(app_name=runner.app_name, user_id=session.user_id)
            print("새로운 대화를 시작합니다.")
            continue
        else:
            for event in runner.run(user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)):
                if event.is_final_response():
                    print(f"Agent: {event.content.parts[0].text}")


    session = await runner.session_service.get_session(app_name=runner.app_name, user_id=session.user_id, session_id=session.id)


asyncio.run(main())