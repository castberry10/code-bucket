from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_core.output_parsers import SimpleJsonOutputParser 
model = ChatOpenAI(model="gpt-4o-mini")

template = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 영어 -> 한국어 봇이야"),
        ("human", "{data}")
    ]
)
# 보통  프롬프트 | 모델 | 파서 로 쓰임
result = (template | model | StrOutputParser()).invoke({"data":"I like Kimchi"})
print(result)