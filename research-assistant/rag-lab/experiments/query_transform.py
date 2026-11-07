from rag import retrieve, split_chunks,embed
import numpy as np
from pathlib import Path
import json

def query_transform(question:str)->str:
    term_map={
        "第三个工程阶段":"B3 阶段",
        "第四个工程阶段":"B4 阶段",
        "B线有哪些阶段及其时长":"B 线中，B1、B2、B3、B4、B5 分别是什么阶段？各阶段的学习时长是多少"
    }
    transformed_question = question
    for raw_term,standard_term in term_map.items():
        transformed_question=transformed_question.replace(raw_term,standard_term)
    return transformed_question

def compare_queries(question:str,chunks,mat):
    original_query=question
    transformed_query=query_transform(question)
    retrieved_chunks=retrieve(original_query,chunks,mat,3)
    retrieved_chunks1=retrieve(transformed_query,chunks,mat,3)
    print("\nOriginal query:", original_query)
    print("\nTransformed query:", transformed_query)
    print("\n=== Original Top-3 ===")
    for idx,score,text in retrieved_chunks:
        print(f"Chunk ID: {idx}, Score: {score:.4f}")
        # print(text[:200])
    print("\n=== Transformed Top-3 ===")
    for idx,score,text in retrieved_chunks1:
        print(f"Chunk ID: {idx}, Score: {score:.4f}")
        # print(text[:200])
    return retrieved_chunks, retrieved_chunks1

if __name__=="__main__":
    assert query_transform("第三个工程阶段")=="B3 阶段"
    assert query_transform("第四个工程阶段")=="B4 阶段"
    assert query_transform("B3 不包括 B4 的内容吗？") == "B3 不包括 B4 的内容吗？"
    print("All tests passed.")
    project_root = Path(__file__).resolve().parents[3]
    config_path = project_root / "research-assistant/rag-lab/config/baseline.json"
    cases_path = project_root / "research-assistant/rag-lab/data/cases.jsonl"
    with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    cases = []
    with open(cases_path, "r", encoding="utf-8") as f:
        cases = []
        for line in f:
            case=json.loads(line)
            if case["split"]=="dev":
                cases.append(case)
    corpus_path = project_root/config["corpus_path"]
    chunks=split_chunks(corpus_path)
    all_vectors = embed(chunks)
    mat = np.array(all_vectors) 
    changed=0
    compare_queries(
    "B线有哪些阶段及其时长？",
    chunks,
    mat
    )
    # for case in cases:
    #     question = case["question"]
    #     compare_queries(question, chunks, mat)
    #     changed += query_transform(question) != question
    # print(f"\n成功处理：{len(cases)} 道 dev 题")
    # print(f"改变的问题数：{changed}")