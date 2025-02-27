# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI

client = OpenAI(
    api_key="sk-/BP7Ouh4WX9zxNIciwaF0XBgIrdEqSa0jUVBUQSxSX0=",  # 请填写您自己的APIKey
    base_url="https://api.wisediag.com/v1",
)

response = client.chat.completions.create(
    model="zzkj",  # # 填写需要调用的模型名称
    messages=[{"role": "user", "content": "我感冒了怎么办？"}],
)


msg = response.choices[0].message
content = msg.content

print(111, content)
