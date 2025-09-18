from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import AgentTool, CodeRunner

# 문제 정의
problem = """
종을 한번 칠때마다 암탉은 알을 낳고, 알은 병아리가 되고, 병아리는 암탉이 된다.
처음에 암탉만 1마리 있을 때, 종을 10번 치면 암탉, 병아리, 알이 몇 개가 되는지를
출력하는 프로그램을 작성해라.
"""

# 1. Planner 에이전트: 문제 해결 계획 수립
planner_agent = Agent(
    name="PlannerAgent",
    instruction=f"""당신은 문제 해결 계획을 수립하는 AI입니다.
주어진 문제를 분석하고, 이 문제를 해결하기 위한 Python 코드 작성 계획을 단계별로 설명하세요.

**문제:**
{problem}

**출력 형식:**
- 1단계: ...
- 2단계: ...
- 3단계: ...
""",
    output_key="plan",
)

# 2. Coder 에이전트: 계획에 따라 코드 작성
coder_agent = Agent(
    name="CoderAgent",
    instruction="""당신은 숙련된 Python 프로그래머입니다.
주어진 계획에 따라 알고리즘 문제를 해결하는 Python 코드를 작성하세요.
코드는 실행 가능한 단일 코드 블록으로 작성해야 합니다.

**계획:**
{plan}
""",
    output_key="code",
)

# 3. Runner 에이전트: 코드 실행 및 결과 검증
runner_agent = Agent(
    name="RunnerAgent",
    instruction="""당신은 코드 실행 및 검증 담당자입니다.
주어진 Python 코드를 실행하고 그 결과를 'code_result' 키에 저장하세요.
""",
    tools=[CodeRunner(output_key="code_result")],
    input_keys=["code"],
)

# 4. Documenter 에이전트: 최종 문서 생성
documenter_agent = Agent(
    name="DocumenterAgent",
    instruction="""당신은 기술 문서 작성 전문가입니다.
주어진 문제, 해결 계획, 코드, 실행 결과를 바탕으로 최종 보고서를 작성하세요.

**문제:**
{problem}

**해결 계획:**
{plan}

**작성된 코드:**
```python
{code}
```

**실행 결과:**
{code_result}

**출력:**
위 모든 정보를 종합하여 명확하고 이해하기 쉬운 보고서를 생성하세요.
""",
    output_key="documentation",
)

# 5. Root 에이전트: 전체 프로세스 실행
root_agent = SequentialAgent(
    name="AlgorithmProblemSolver",
    sub_agents=[
        planner_agent,
        coder_agent,
        runner_agent,
        documenter_agent,
    ],
    instruction="알고리즘 문제를 해결하고 문서화하는 전체 프로세스를 실행합니다.",
)