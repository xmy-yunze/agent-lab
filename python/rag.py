import os,re,requests
import numpy as np

EMBED_URL="https://open.bigmodel.cn/api/paas/v4/embeddings"

def split_chunks(path):
    with open(path,encoding="utf-8") as f:
        text = f.read()
    raw=re.split(r"\n(?=#{2,3} )", text)
    return [c for c in raw if len(c)!=0]

def embed(texts):
    r=requests.post(EMBED_URL,
                headers={"Authorization": f"Bearer {os.environ['ZHIPU_API_KEY']}"},
                json={"model":"embedding-3","input":texts},)
    if r.status_code!=200:
        raise RuntimeError(f"embedding failed: {r.status_code} {r.text}")
    d=r.json()
    x=d["data"]
    return [res["embedding"] for res in x]

def retrieve(question,chunks,mat,k):
    q_vec=embed([question])[0]
    q_vec=np.array(q_vec)
    scores=(mat@q_vec)/(np.linalg.norm(q_vec)*np.linalg.norm(mat,axis=1))
    order=np.argsort(scores)
    topk=order[::-1][:k]
    return [(idx,scores[idx],chunks[idx]) for idx in topk]
