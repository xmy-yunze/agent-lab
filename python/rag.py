import os,re,requests
import numpy as np

EMBED_URL="https://open.bigmodel.cn/api/paas/v4/embeddings"
# HEADING_RE=re.compile(r"^(#{1,6}) +(.*)$")
# MIN_SPLIT_LEVEL=2          # 最低切分级别：2 表示 ## 及以上才切，# 不切
# def split_chunks(path):
#     with open(path,encoding="utf-8") as f:
#         text = f.read()
#     raw=re.split(r"\n(?=#{2,} )", text)
#     return [c for c in raw if len(c)!=0]

EMBED_URL="https://open.bigmodel.cn/api/paas/v4/embeddings"
HEADING_RE=re.compile(r"^(#{1,6}) +(.*)$")
MIN_SPLIT_LEVEL=2

def split_chunks(path):
    with open(path,encoding="utf-8") as f:
        text = f.read()
    stack=[]
    chunks=[]
    buf=[]
    in_fence=False
    def seal():
        if not buf:
            return
        body="\n".join(buf).strip()
        buf.clear()
        if not body:
            return
        prefix=" > ".join(t for _,t in stack[:-1])
        chunks.append(prefix+"\n"+body if prefix else body)

    for line in text.split("\n"):
        if line.startswith("```"):       # 碰到围栏：翻转开关（围栏行本身是正文，别丢）
            in_fence=not in_fence
            buf.append(line)
            continue
        if in_fence:                     # 在代码块里：一律当正文
            buf.append(line)
            continue
        m=HEADING_RE.match(line)
        if not m:
            buf.append(line)
            continue
        level=len(m.group(1))
        if level>=MIN_SPLIT_LEVEL:
            seal()
        while stack and stack[-1][0]>=level:
            stack.pop()
        stack.append((level,m.group(2).strip()))
        buf.append(line)
    seal()
    return chunks


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
