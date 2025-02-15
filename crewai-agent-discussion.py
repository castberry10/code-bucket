# pip install crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29
import warnings
from openai import OpenAI
from crewai import Agent, Task, Crew
import os

warnings.filterwarnings('ignore')

ACCESS_KEY = "YOUR ACCESS KEY"
os.environ["OPENAI_API_KEY"] = ACCESS_KEY
client = OpenAI(api_key = ACCESS_KEY)


student_proponent = Agent(
    role="{topic}에 대해 찬성하는 대학생",
    goal="당신은 {topic} 주제에 대해서 토론자로 참여하였습니다. 당신이 가지고 있는 관점에서 토론 주제에 대한 생각을 제공하세요.",
    backstory=(
        "당신은 현재 한국에서 가장 권위있는 토론 대회에 참여하고 있습니다."
        "{topic} 주제에 대한 당신의 생각과 입장을 제공하세요."
        "당신의 주장을 펼칠 때 이를 뒷받침하는 논리적인 근거를 제공해야 합니다."
        "가정이나 추측을 하지 말고, 논리적이고 정돈된 내용을 제공해야 합니다."
        "한국어로 토론을 진행해야 합니다."
    ),
    allow_delegation=False,
    verbose=True,
    LLM="gpt-4o-mini"
)

student_opponent = Agent(
    role="{topic}에 대해 반대하는 대학생",
    goal="당신은 {topic} 주제에 대해서 토론자로 참여하였습니다. 당신이 가지고 있는 관점에서 토론 주제에 대한 생각을 제공하세요.",
    backstory=(
        "당신은 현재 한국에서 가장 권위있는 토론 대회에 참여하고 있습니다."
        "{topic} 주제에 대한 당신의 생각과 입장을 제공하세요."
        "당신의 주장을 펼칠 때 이를 뒷받침하는 논리적인 근거를 제공해야 합니다."
        "가정이나 추측을 하지 말고, 논리적이고 정돈된 내용을 제공해야 합니다."
        "한국어로 토론을 진행해야 합니다."
    ),
    allow_delegation=False,
    verbose=True,
    LLM="gpt-4o-mini"
)

moderator = Agent(
    role="토론의 사회를 보며, 진행과 중재를 수행하는 사회자",
    goal="당신은 {topic} 주제에 대해서 사회자로 참여하였습니다. 토론을 진행하고, 양측 토론자의 논의 과정을 정리하세요.",
    backstory=(
        "당신은 현재 한국에서 가장 권위있는 토론 대회에 사회자로 참여하고 있습니다."
        "당신은 사회자로서 토론을 이끌고, 토론자들의 토론 진행과 중재를 진행해야 합니다."
        "토론이 건전하게 진행될 수 있도록, 과도한 주장이나 억측에 대해서 중재하세요."
        "한국어로 토론을 진행해야 합니다."
    ),
    allow_delegation=False,
    verbose=True,
    LLM="gpt-4o-mini"
)

opening = Task(
    description=(
        "1. 토론의 시작에 앞서, 토론 프로그램에 대해 소개합니다.\n"
        "2. {topic}에 대한 소개와 쟁점에 대해 알립니다.\n"
        "3. 토론자들에게 각자의 발언을 요청합니다..\n"
    ),
    expected_output="토론 프로그램의 오프닝 멘트 및 토론 진행",
    agent=moderator
)

def opinion_task(agent):
    task =  Task(
            description=(
                "1. {topic}에 대한 본인의 입장과 생각을 정리합니다.\n"
                "2. 정리한 본인의 입장과 생각을 기반으로 자신의 주장을 정리합니다.\n"
                "3. 상대방을 설득할 수 있는 주장을 펼칩니다.\n"
            ),
            expected_output="주제에 대한 자신의 입장과 주장을 담은 발표",
            agent=agent
        )
    return task

opinion_proponent = opinion_task(student_proponent)
opinion_opponent = opinion_task(student_opponent)

def rebuttal_task(agent):
    task =  Task(
            description=(
                "1. 상대 토론자의 주장에 대해 반박할 수 있는 부분을 정리합니다.\n"
                "2. 상대 토론자의 주장에 대해 근거를 기반으로 반박합니다.\n"
                "3. 상대 토론자의 주장에 비해 나의 주장이 더 설득력 있는 부분을 강조합니다..\n"
            ),
            expected_output="상대 토론자에 대한 반박을 담은 발표",
            agent=agent
        )
    return task

rebuttal_proponent = rebuttal_task(student_proponent)
rebuttal_opponent = rebuttal_task(student_opponent)

ending = Task(
    description=(
        "1. 양측 토론자의 주장에 대해 정리합니다.\n"
        "2. 양측 토론자가 부족했던 점에 대해 정리합니다.\n"
        "3. 양측 토론자 중 최종 승자에 대해 판정합니다.\n"
        "4. 토론 프로그램의 종료를 알립니다.\n"
    ),
    expected_output="토론자들의 주장 정리와 피드백, 승자에 대한 판정 및 종료 멘트",
    agent=moderator
)

crew = Crew(
    agents=[student_proponent, student_opponent],
    tasks=[opening, opinion_proponent, opinion_opponent, rebuttal_proponent, rebuttal_opponent, ending],
    verbose=2
)
result = crew.kickoff(inputs={"topic": "의대 증원"})