from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel, Field
import json

class CountryInput(BaseModel):
    country: str = Field(..., description="The name of the country to get information about.")

class CapitalInfoOutput(BaseModel):
    country: str = Field(..., description="The country to get information about.")
    capital: str = Field(..., description="The capital city of the country.")

root_agent = Agent(
    name="country_agent",
    model="gemini-2.0-flash",
    input_schema=CountryInput,
    output_schema=CapitalInfoOutput,
    output_key="output", # The key in the output where the result will be stored # called capital
    description="국가에 대한 정보를 제공하는 에이전트입니다.",
    instruction=f"""사용자는 {{"country": "한국"}} 와 같은 JSON 형식으로 국가 이름을 제공합니다.
                    json객체로 응답해주세요 {json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)}""",
)

print(CountryInput.model_json_schema())