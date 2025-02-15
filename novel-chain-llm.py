# pip install langchain_community==0.0.29
from openai import OpenAI

ACCESS_KEY = "YOUR ACCESS KEY"
client = OpenAI(api_key = ACCESS_KEY)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "당신은 추리 소설을 집필하는 소설가입니다."},
    {"role": "user", "content": "세 문장 이내로 현대 추리 소설의 배경을 생성하고, 2명의 등장인물을 만들어주세요."}
  ])

context = response.choices[0].message.content
print(response.choices[0].message.content)
print("-----------------------------------")
### 소설가

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "당신은 추리 소설을 집필하는 소설가입니다."},
    {"role": "user", "content": "다음 조건에 따라 짧은 두 문단 분량의 소설 도입부를 흥미롭게 작성하세요.\n{}".format(context)}
  ])

draft = response.choices[0].message.content
print("소설가")
print(draft)
print("-----------------------------------")
### 편집자

prompt = """
다음 주어진 텍스트는 추리 소설의 도입부 입니다.
수정이 필요한 부분에 대해 피드백을 3문단 이하로 남겨주세요.

소설 배경: {}

텍스트: {}""".format(context, draft)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "당신은 추리소설을 출판하는 출판사의 전문 편집자입니다."},
    {"role": "user", "content": prompt}
  ])

feedback = response.choices[0].message.content
print("편집자")
print(feedback)
print("-----------------------------------")
### 소설가 (편집자 피드백 반영 단계)

prompt = """
당신은 대학교를 소재로 하는 추리 소설을 집필하고 있습니다.
다음에 주어진 '도입부'와 '도입부에 대한 편집자의 피드백'을 참고하여, '도입부'를 수정하세요.

소설 배경: {}

도입부: {}

도입부에 대한 편집자의 피드백: {}

수정된 도입부:
""".format(context, draft, feedback)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "당신은 추리 소설을 집필하는 소설가입니다."},
    {"role": "user", "content": prompt}
  ])

mod_draft = response.choices[0].message.content
print("소설가")
print(mod_draft)
print("-----------------------------------")
### 교열 전문가의 교열

prompt = """
다음 주어진 원고는 소설의 도입부 입니다.
주어진 원고에서 어색한 부분, 잘못된 맞춤법이 사용된 부분 등을 수정하세요.
수정된 원고를 출력하고, 수정된 부분을 따로 정리해서 출력하세요.

주어진 원고: {}

수정된 원고:

수정된 부분:
""".format(mod_draft)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "당신은 소설 원고의 수정을 담당하는 추리소설 출판사의 교열 전문가입니다."},
    {"role": "user", "content": prompt}
  ])
print("교열 전문가")
print(response.choices[0].message.content)
print("-----------------------------------")