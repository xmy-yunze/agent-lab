import os
import requests

key = os.environ["ZHIPU_API_KEY"]
print(key[:4])

url = "https://open.bigmodel.cn/api/paas/v4/chat/completions" 


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
}

body = {
    "model": "glm-4.7",
    "messages": [
        {"role": "user", "content": "你好"}
    ]
}

response = requests.post(url, headers=headers, json=body)
if response.status_code == 200:
    data = response.json()
    print(data["choices"][0]["message"]["content"])
else:
    print(response.status_code)   # 先看"几号错误"
    print(response.text)          # 再看服务端说的原话
