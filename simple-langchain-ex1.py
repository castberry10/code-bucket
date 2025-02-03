# pip install langchain_openai langchain_core
import os
os.environ["OPENAI_API_KEY"] = 'sk-1234567890abcdef1234567890abcdef'

from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")

msg = [
    ("system", "넌 번역봇이야. 영어가 들어오면 한국어로 번역해"),
    ("human", "I love programming.")
]
result = model.invoke(msg)
print(result.content) 