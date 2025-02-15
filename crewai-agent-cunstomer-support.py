# pip install crewai==0.28.8 crewai_tools==0.1.6 langchain_community==0.0.29
import warnings
from openai import OpenAI
from crewai import Agent, Task, Crew
import os

warnings.filterwarnings('ignore')

ACCESS_KEY = "YOUR ACCESS KEY"

os.environ["OPENAI_API_KEY"] = ACCESS_KEY
client = OpenAI(api_key = ACCESS_KEY)

support_agent = Agent(
    role="선임 지원 담당자",
    goal="고객 지원 팀에서 고객 지원을 담당하는 역할을 수행하세요.",
    backstory=(
        "당신은 CrewAI (https://crewai.com)의 고객 지원 부서에서 근무하고 있습니다."
        "현재 회사에서 가장 중요한 고객인 {customer}에게 고객 지원 서비스를 제공하는 중입니다."
        "해당 고객에게 최고의 지원을 제공하세요."
        "가정이나 추측을 하지 말고, 완전한 답변을 제공해야 합니다."
    ),
    allow_delegation=False,
    verbose=True,
    LLM="gpt-4o-mini"
)

support_quality_assurance_agent = Agent(
    role="고객지원서비스 품질 관리자",
    goal="고객지원서비스의 품질을 보장하기 위한 관리자의 역할을 수행하세요.",
    backstory=(
        "당신은 CrewAI (https://crewai.com)의 고객 지원 부서에서 근무하고 있습니다."
        "현재 당신은 고객 지원 담당자가 {customer}의 요청에 대해 최선의 지원을 제공하고 있는지 확인하고 있습니다."
        "지원 담당자가 완전한 답변을 제공하고 있는지 확인해야 하며, 어떠한 가정이나 추측은 하지 말아야 합니다."
    ),
    allow_delegation=True,
    verbose=True,
    LLM="gpt-4o-mini"
)

from crewai_tools import SerperDevTool, \
                         ScrapeWebsiteTool, \
                         WebsiteSearchTool
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/concepts/crews"
)

inquiry_resolution = Task(
    description=(
        "{customer}는 다음과 같은 매우 중요한 문의를 하였습니다:\n"
        "{inquiry}\n\n"
        "{customer}의 {person}이 연락을 해왔습니다. 해당 고객에게 최선의 지원을 제공하세요. "
        "고객의 문의에 대해 정확한 답변을 제공하기 위해 최선을 다해야 하며, 알고 있는 지식을 모두 활용하세요."
    ),
    expected_output=(
        "고객의 문의에 대해 상세하고 도움이 되는 답변을 통해 문의의 모든 측면을 다루세요. "
        "답변에는 외부 데이터나 솔루션을 포함하여 모든 참고 자료가 포함되어야 합니다. "
        "답변은 완전해야하며, 미답변 질문이 없도록 하고, 전체적으로 도움이 되고 친절한 어조를 유지해야 합니다."
    ),
    tools=[docs_scrape_tool],
    agent=support_agent,
)

quality_assurance_review = Task(
    description=(
        "{customer}의 문의에 대해 선임 지원 담당자가 작성한 답변 초안을 검토하세요. "
        "답변이 포괄적이고 정확하며, 고객 지원에서 기대하는 고품질 수준을 만족하는지 확인하세요. "
        "도움이 되고 친절한 어조로 고객 문의의 모든 부분을 철저하게 다루었는지 확인하세요. "
        "정보를 찾는 데에 사용된 콘텐츠의 출처를 확인하여 답변이 잘 뒷받침 되고 있는지 확인하세요. "
    ),
    expected_output=(
        "고객에게 보낼 수 있는 상세하고 유익한 최종 답변이 준비되어야 합니다. "
        "이 답변은 모든 피드백과 개선 사항을 포함하여 고객의 문의를 완벽하게 해결해야 합니다. "
        "전문적이며 친절한 어조를 유지하세요."
    ),
    agent=support_quality_assurance_agent,
)

crew = Crew(
  agents=[support_agent, support_quality_assurance_agent],
  tasks=[inquiry_resolution, quality_assurance_review],
  verbose=2,
  memory=True
)

inputs = {
    "customer": "Hanyang University",
    "person": "Mingon Jeong",
    "inquiry": "CrewAI를 사용하는 과정에서 Crew를 설정하고 Kick off 하는 데에 도움이 필요합니다."
               "특히 Crew에 memory를 추가하려면 어떻게 해야하나요?"
               "안내 부탁드립니다."
}
result = crew.kickoff(inputs=inputs)

from IPython.display import Markdown
Markdown(result)