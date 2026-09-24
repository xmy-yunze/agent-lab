import numpy as np
from rag import split_chunks, embed, retrieve
import os,requests,sys

CHAT_URL="https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL="glm-4.7"

PROMPT_TEMPLATE = """你是一个资料助手，只依据下面提供的资料回答问题。
===== 资料 =====
{blocks}
===== 资料结束 =====
问题：{question}
要求：
1. 只依据上面的资料回答。资料里没有提到的，直接回答「资料里没有」，不要用自己的知识补充。
2. 回答末尾用 [1] [2] 这样的编号，标出你依据的是哪几段资料。
"""

def build_prompt(question, hits):
    blocks="\n".join([f"[{i}] {text}" for i,(_,_,text) in enumerate(hits,start=1)])    
    return PROMPT_TEMPLATE.format(question=question, blocks=blocks)


def ask(prompt):
    r=requests.post(CHAT_URL,
                headers={"Authorization": f"Bearer {os.environ['ZHIPU_API_KEY']}"},
                json={"model":MODEL,"temperature":0,"messages":[{"role":"user","content":prompt}]},
                timeout=60)
    if r.status_code!=200:
        raise RuntimeError(f"chat failed: {r.status_code} {r.text}")
    d=r.json()
    return d["choices"][0]["message"]["content"]

if __name__=="__main__":
    question=sys.argv[1] if len(sys.argv)>1 else "KV Cache 是什么？"
    chunks=split_chunks("学习计划.md")  
    mat=np.array(embed(chunks))  
    hits=retrieve(question,chunks,mat,k=3)
    for idx, score, text in hits:
        print(f"{score:.4f}  [{idx}] len={len(text):4d}  {text.split(chr(10))[0][:40]}")
    prompt=build_prompt(question,hits)
    print("=== Prompt ===")
    print(prompt)
    print("=== Answer ===")
    print(ask(prompt))