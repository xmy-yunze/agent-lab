import os,requests,re
import numpy as np


def split_chunks(path):
    with open(path,encoding="utf-8") as f:
        text = f.read()
    raw=re.split(r"\n(?=#{2,3} )", text)
    return [c for c in raw if len(c)!=0]

def embed(texts):
    r=requests.post("https://open.bigmodel.cn/api/paas/v4/embeddings",
                headers={"Authorization": f"Bearer {os.environ['ZHIPU_API_KEY']}"},
                json={"model":"embedding-3","input":texts},)
    if r.status_code!=200:
        raise RuntimeError(f"embedding failed: {r.status_code} {r.text}")
    d=r.json()
    x=d["data"]
    return [res["embedding"] for res in x]
    
chunks=split_chunks("学习计划.md")
q="每天要学几个小时？"
q_vec=embed([q])[0]

vecs=embed(chunks)
scores=[]
# 循环版
# for i in range(len(chunks)):
#     a=np.array(q_vec)
#     b=np.array(vecs[i])
#     ans=a@b/(np.linalg.norm(a)*np.linalg.norm(b))
#     scores.append(ans)

# 矩阵版
q_vec=np.array(q_vec)
vecs=np.array(vecs)
scores=(q_vec@vecs.T)/(np.linalg.norm(q_vec)*np.linalg.norm(vecs,axis=1))

order=np.argsort(scores)
top3=order[::-1][:3]
for idx in top3:
    preview=chunks[idx][:60].replace("\n"," ")
    print(f"score: {scores[idx]:.4f}, chunk: {preview}")