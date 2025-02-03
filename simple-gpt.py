from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "너는 사람에게 고민상담을 해주는 ai야"},
    {"role": "user", "content": "너무 슬퍼요"}
  ]
)
print(response.choices[0].message.content) 