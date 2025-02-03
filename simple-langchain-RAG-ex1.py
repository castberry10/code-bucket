from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

model = ChatOpenAI(model='gpt-4o-mini')
loader = WebBaseLoader('https://github.com/facebookresearch/segment-anything-2')
docs = loader.load()

# template = ChatPromptTemplate.from_template("""
#     질문에 대해서 context부분을 읽고 답변을 작성해줘:
#     context: {context}
#     질문: {question}
#     답변:
# """)
# chain = template | model | StrOutputParser()
# result = chain.invoke({'context' : docs, 'question' : 'SAM2 모델 설치는 어떻게 해'})
# print(result) 
template = ChatPromptTemplate.from_template("""
    질문에 대해서 context부분을 읽고 답변을 작성해줘:
    context: {context}
    질문: {question}
    답변:
""")

def func(a):
  return docs

chain = {
        "context": func,
        "question": RunnablePassthrough(),
    } | template | model | StrOutputParser()
result = chain.invoke({'question' : 'SAM2 모델 설치는 어떻게 해'})
print(result)