# pip install crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29
import warnings
from openai import OpenAI
from crewai import Agent, Task, Crew
import os


warnings.filterwarnings('ignore')

ACCESS_KEY = "YOUR ACCESS KEY"

os.environ["OPENAI_API_KEY"] = ACCESS_KEY
client = OpenAI(api_key = ACCESS_KEY)

planner = Agent(
    role="콘텐츠 기획자",
    goal="{topic}에 대해 사실적이고 구체적인 한국어 기획안을 작성하세요.",
    backstory="당신은 주제에 대한 블로그 포스팅을 기획하고 있습니다."
              "주제: {topic}."
              "블로그 독자들이 주제에 대해 배우거나 정보를 얻는 데에 도움이 되는 요소를 수집하세요."
              "당신의 작업은 콘텐츠 작성자가 이 주제에 대한 글을 작성하는 데 기초가 됩니다.",
    allow_delegation=False,
    verbose=True,
    LLM="gpt-4o-mini"
)
writer = Agent(
    role="콘텐츠 작성자",
    goal="{topic}에 대한 사실적이고 통찰력 있는 한국어 포스팅을 작성하세요.",
    backstory="주제에 대한 개요와 관련 맥락을 제공하는 콘텐츠 기획자의 작업을 기반으로"
              "글을 작성합니다."
              "콘텐츠 기획자가 제공한 주요 목표와 방향을 따르세요."
              "객관적이고 공정한 인사이트를 제공하고, 콘텐츠 기획자가 제공한 정보로 이를 뒷받침하세요.",
    allow_delegation=False,
    verbose=True,
    LLM="gpt-4o-mini"
)
editor = Agent(
    role="콘텐츠 에디터",
    goal="지정된 글쓰기 스타일에 맞게 한국어 블로그 포스팅을 편집하세요.",
    backstory="당신은 콘텐츠 작성자로부터 블로그 포스팅을 전달받는 편집자입니다."
              "당신의 목표는 블로그 포스팅이 저널리즘 모범 사례를 따르고 있는지 확인하고, "
              "의견이나 주장을 제공할 때 균형 잡힌 관점을 제공하는지 검토하며, "
              "논란이 되는 주요 주제나 의견을 피할 수 있도록 포스팅을 수정하는 것입니다.",
    allow_delegation=False,
    verbose=True,
    LLM="gpt-4o-mini"
)

plan = Task(
    description=(
        "1. {topic}에 대한 최신 트렌드, 선도 기업 또는 주목할 만한 뉴스의 우선 순위를 정합니다.\n"
        "2. 관심사와 고객 니즈를 고려하여 타겟 고객을 식별합니다.\n"
        "3. 소개, 핵심 사항을 포함하여 자세한 콘텐츠 개요를 만듭니다.\n"
    ),
    expected_output="주제에 대한 소개와 핵심 사항을 포함하는 포괄적인 콘텐츠 기획 문서",
    agent=planner
)
write = Task(
    description=(
        "1. 콘텐츠 기획안을 기반으로 {topic}에 대한 흥미로운 블로그 포스팅을 작성합니다.\n"
        "2. 섹션 명칭과 부제목을 포스팅에 적절하게 통합합니다.\n"
        "3. 흥미로운 소개 섹션, 본문, 요약된 결론을 중심으로 포스팅을 구성합니다.\n"
        "4. 문법 오류나 오타를 교정하고, 글의 내용이 브랜드의 이미지와 일치하는지 확인합니다."
    ),
    expected_output="블로그에 게시할 준비가 되어 있으며, 각 섹션은 2~3개의 단락으로 구성되어 있고,"
                    "markdown format으로 잘 작성된 블로그 포스팅",
    agent=writer
)
edit = Task(
    description=(
        "주어진 블로그 포스팅의 문법 오류와 오타를 교정하고, 글이 브랜드의 이미지와 일치하는지 확인합니다."
    ),
    expected_output="블로그에 게시할 준비가 되어 있으며, 각 섹션은 2~3개의 단락으로 구성되어 있고,"
                    "markdown format으로 잘 작성된 블로그 포스팅",
    agent=writer
)

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

result = crew.kickoff(inputs={"topic": "프로 축구 스카우팅"})

from IPython.display import Markdown
Markdown(result)