import json
from pathlib import Path

base = Path("research-assistant/rag-lab/data")
source = base / "dev_retrieval.jsonl"
target = base / "dev_retrieval_readable.md"

with source.open("r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

with target.open("w", encoding="utf-8") as f:
    f.write("# Day 1 · RAG 检索基线结果\n\n")
    f.write(f"测试题数量：{len(records)}\n\n")

    for record in records:
        f.write(f"## {record['case_id']}｜{record['question']}\n\n")
        f.write(f"**Top-K：** {record['top_k']}\n\n")

        for rank, hit in enumerate(record["hits"], start=1):
            f.write(
                f"### Top-{rank} · Chunk {hit['chunk_id']} "
                f"· 相似度 {hit['score']:.4f}\n\n"
            )
            f.write(hit["text"] + "\n\n")
            f.write("---\n\n")

print("已生成：", target)