
from .lambda_agent import LambdaAgent
from .json_input_agent import JsonInputAgent
from .while_agent import WhileAgent

from google.adk.agents import SequentialAgent

from typing import Optional
def increase(x: int) -> int:
    return x + 1


def fibonacci(f: Optional[list[int]]) -> list[int]:
    if f is None: f = [0, 1]
    f.append(f[-1] + f[-2])
    return f

root_agent = SequentialAgent(name="json_input_data",
                             sub_agents=[
                                JsonInputAgent(name="json_input_agent"),
                                WhileAgent(name="fibonacci_while_agent",
                                           condition="""'sequence' not in locals() or len(sequence) <= number""",
                                           sub_agents=[
                                               LambdaAgent(func=fibonacci,
                                                            name="fibonacci_agent",
                                                        input_keys=["sequence"],
                                                        output_key="sequence")
                                            ]),
                         
                                LambdaAgent(name="fibonacci_output_agent",
                                            func=lambda sequence, n: sequence[n],
                                            input_keys=["sequence", "number"],
                                            output_key="fibonacci number")


                         ])