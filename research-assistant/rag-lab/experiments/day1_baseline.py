import json
from rag import split_chunks, embed,retrieve
import numpy as np
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root / "python" / "first"))
from day5 import build_prompt, ask

with open("research-assistant/rag-lab/data/cases.jsonl","r",encoding="utf-8") as f:
    dev_cases = []
    for line in f:
        case = json.loads(line)
        if case["split"]=="dev":
            # print(case["id"], case["question"])
            dev_cases.append(case)

with open("research-assistant/rag-lab/config/baseline.json","r",encoding="utf-8") as f:
    config = json.load(f)

chunks=split_chunks(config["corpus_path"])
all_vectors = []

for i in range(0, len(chunks), 2):
    batch = chunks[i:i + 2]
    vectors = embed(batch)
    all_vectors.extend(vectors)

mat = np.array(all_vectors)
print("文档向量矩阵：", mat.shape)
for index in [0,2,3]:
    case = dev_cases[index]
    hits=retrieve(case["question"], chunks, mat, config["top_k"])
    prompt=build_prompt(case["question"], hits)
    answer=ask(prompt)
    print("\n问题：", case["question"])
    print("答案：", answer)
# for case in dev_cases:
#     hits=retrieve(case["question"], chunks, mat, config["top_k"])
#     print("问题：", case["question"])
#     for rank, (idx, score, text) in enumerate(hits, start=1):
#         print(f"\nTop-{rank},Chunk{idx} 相关度：{score:.4f}")
#         print(text[:300])

# prompt=build_prompt(case["question"], hits)
result=[]
for case in dev_cases:
    hits=retrieve(case["question"], chunks, mat, config["top_k"])
    hit_records=[]
    for idx,score,text in hits:
        hit_records.append({"chunk_id":int(idx),"score":float(score),"text":text})
    record={
        "case_id": case["id"],
        "question": case["question"],
        "top_k": config["top_k"],
        "hits": hit_records,
    }
    result.append(record)
print("已记录题目数量：", len(result))
output_path = "research-assistant/rag-lab/data/dev_retrieval.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for record in result:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
print("实验结果已保存到：", output_path)