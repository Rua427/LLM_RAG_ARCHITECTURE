import json
import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)

    print("국가에 정보를 제공하는 에이전트입니다. 궁금한 국가를 입력하세요. 'exit' 입력 시 종료됩니다.")
    while True:
        user_input = input("Country: ")
        if user_input.lower() == "exit": break

        session = await runner.session_service.create_session(app_name=runner.app_name,
                                                              user_id="user1")

        print(f"{user_input}에 대해 궁금한 것을 질문하세요. 'exit' or 'quit' 입력 시 종료됩니다.")
        while True:
            user_input = input("User: ")
            if user_input.lower() in [ "exit", "quit" ]: break

            for event in runner.run(
                user_id=session.user_id, session_id=session.id, new_message=UserContent(user_input)
            ):
                if event.is_final_response():
                    print(f"Agent: {event.content.parts[0].text}")

            session = await runner.session_service.get_session(app_name=session.app_name, user_id=session.user_id, session_id=session.id)
            print(session.events)
            capital = session.state.get("output")
            if capital:
                print(f"{capital['country']}의 수도는 {capital['capital']}입니다.")

asyncio.run(main())