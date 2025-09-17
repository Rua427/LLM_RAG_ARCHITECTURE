import dotenv
dotenv.load_dotenv()

from agent import root_agent

import asyncio
from google.adk.runners import InMeomoryRunner
from google.genai.types import UserContent

async def main():
    runner = InMemoryRunner(agent=root_agent, app_name=root_agent.name)
    session = await runner.session_service.create_session(app_name=runner.app_name,
                                                          user_id="user1")

    while True:

        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break


        for event in runner.run(user_id = session.user_id,
                   session_id = session.id,
                   new_message=UserContent(user_input)):
            if event.is_final_response():
                print(f"Agent: {event.content.parts[0].text}")

    print(session.events)


asyncio.run(main())  
