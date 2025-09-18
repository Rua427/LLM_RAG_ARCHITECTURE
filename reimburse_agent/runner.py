import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai.types import UserContent, Part

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)
    session = await runner.session_service.create_session(app_name=root_agent.name, user_id="user1")

    request = "회식 비용 $250을 환급해주세요."

    for event in runner.run(
        user_id=session.user_id, session_id=session.id,
        new_message=UserContent(request)
    ):
        if event.content.parts[0].function_response is not None:
            approval_request = event.content.parts[0].function_response
        if event.is_final_response():
            print(f"Agent: {event.content.parts[0].text}")

    if approval_request is not None:
        user_input = input(f"승인 요청이 있습니다: {approval_request}\n승인하시겠습니까? (y/n): ")
        approval_response = approval_request.model_copy(deep=True)
        approval_response.response["status"] = "approved" if user_input.lower() == 'y' else "rejected"

        for event in runner.run(
            user_id=session.user_id, session_id=session.id,
            new_message=UserContent(parts=[Part(function_response=approval_response)])
        ):
            if event.is_final_response():
                print(f"Agent: {event.content.parts[0].text}")

    session = await runner.session_service.get_session(app_name=runner.app_name, user_id=session.user_id, session_id=session.id)

    for event in session.events:
        print("-" * 20)
        print(f"{event.content.role}: {event.content}")


asyncio.run(main())