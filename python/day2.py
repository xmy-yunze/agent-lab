import os
import requests
from fastapi import FastAPI

app = FastAPI()

key = os.environ["ZHIPU_API_KEY"]
URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

@app.get("/xmy/")
def read_xmy(message:str):
    body={
    "model": "glm-4.7",
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
    response = requests.post(URL, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        return {"message": data["choices"][0]["message"]["content"]}
    else:
        return {"error": response.status_code, "message": response.text}