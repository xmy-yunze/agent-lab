import math
import re
import jieba
from rag import split_chunks,retrieve,embed
import numpy as np
from pathlib import Path
import json
jieba.add_word("B线")
jieba.add_word("A线")
jieba.add_word("时长")
def tokenize(text:str)->list[str]:
    text = text.replace("B 线","B线")
    text = text.replace("A 线","A线")
    tokens=jieba.lcut(text) # 把中文字符串切分成词语列表。
    STOPWORDS = {
    "？", "?", "，", "。", "、",
    "的", "了", "是", "有", "哪些", "及其"
    }
    return [
        token.strip().lower() 
        for token in tokens 
        if token.strip() and token.strip() not in STOPWORDS]

def term_frequency(words:list[str],term:str)->int:
    count = 0
    for word in words:
        if word == term:
            count += 1
    return count

def document_frequency(documents:list[list[str]],term:str)->int:
    count = 0
    for doc in documents:
        if term in doc:
            count += 1
    return count

def inverse_document_frequency(documents:list[list[str]],term:str)->float:
    n = len(documents)
    df = document_frequency(documents, term)
    if df == 0:
        return 0.0
    return math.log(1 + (n - df + 0.5) / (df + 0.5))

def average_document_length(documents:list[list[str]])->float:
    total_length = sum(len(doc) for doc in documents)
    return total_length / len(documents) if documents else 0.0

def bm25_score(
        query:list[str],
        doc:list[str],
        documents:list[list[str]], 
        k1:float=1.2, 
        b:float=0.75)->float:
            score = 0.0
            avgdl = average_document_length(documents)
            doc_len=len(doc)
            if avgdl == 0:
                return 0.0
            for term in set(query):
                tf = term_frequency(doc, term)
                if tf == 0:
                    continue
                idf = inverse_document_frequency(documents, term)
                score += idf * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * doc_len / avgdl))
            return score

def bm25_retrieve(
        query:list[str],
        documents:list[list[str]],
        k:int
        ):
            scores = []
            for i, doc in enumerate(documents):
                score = bm25_score(query, doc, documents)
                scores.append((i, score,doc))
            scores.sort(key=lambda x: x[1], reverse=True)
            return scores[:k]

def bm25_search(
        query:str,
        chunks:list[str],
        k:int
        ):
            query_tokens = tokenize(query)
            tokenized_docs = [tokenize(chunk) for chunk in chunks]
            bm25_results = bm25_retrieve(query_tokens, tokenized_docs, k)
            results=[]
            for chunk_id,score,tokens in bm25_results:
                original_chunk = chunks[chunk_id]
                results.append((chunk_id,score,original_chunk))
            return results


def rrf_fusion(dense_results, bm25_results, rrf_k=60):
    scores = {}
    contents={}
    for rank,(chunk_id,score,content) in enumerate(dense_results,start=1):
         contribution=1/(rrf_k + rank)
         scores[chunk_id] = scores.get(chunk_id, 0.0) + contribution
         contents[chunk_id] = content
    for rank,(chunk_id,score,content) in enumerate(bm25_results,start=1):
        contribution=1/(rrf_k + rank)
        scores[chunk_id] = scores.get(chunk_id, 0.0) + contribution
        contents[chunk_id] = content
    ranked=sorted(scores.items(), key=lambda x: x[1], reverse=True)
    final_result=[]
    for cid,rrf_score in ranked:
        final_result.append((cid, rrf_score, contents[cid]))
    return final_result

def print_results(name, results):
    print(f"\n===== {name} =====")
    for chunk_id, score, content in results:
        print(f"Chunk {chunk_id}, Score: {score:.5f}")
        print(content[:100])

def debug_bm25(query: str, chunks: list[str], chunk_ids: list[int]):
    query_tokens = tokenize(query)
    tokenized_docs = [tokenize(chunk) for chunk in chunks]

    print("Query Tokens:", query_tokens)

    for cid in chunk_ids:
        doc = tokenized_docs[cid]

        print(f"\n===== Chunk {cid} =====")

        for term in set(query_tokens):
            tf = term_frequency(doc, term)
            df = document_frequency(tokenized_docs, term)
            idf = inverse_document_frequency(tokenized_docs, term)

            print(
                f"term={term!r}, "
                f"TF={tf}, DF={df}, IDF={idf:.4f}"
            )

if __name__ == "__main__":
    # dense_results = [
    #     (13, 0.85, "B1 阶段"),
    #     (15, 0.78, "B3 阶段"),
    #     (17, 0.72, "B5 阶段")
    # ]

    # bm25_results = [
    #     (15, 3.5, "B3 阶段"),
    #     (13, 2.8, "B1 阶段"),
    #     (16, 1.5, "B4 阶段")
    # ]
    # scores = rrf_fusion(dense_results, bm25_results)
    # for chunk_id, score, content in scores:
    #     print(f"\n{chunk_id}, {score:.5f}, {content}")
    # assert len(scores)==4
    # assert {scores[0][0],scores[1][0]} == {13,15}
    # assert scores[0][1]>=scores[1][1]>=scores[2][1]
    # assert len(scores[0]) == 3
    # print("RRF fusion passed")
    project_root = Path(__file__).resolve().parents[3]
    config_path = project_root /  "research-assistant/rag-lab/config/baseline.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    corpus_path = project_root / config["corpus_path"]

    chunks = split_chunks(corpus_path)

    mat=np.array(embed(chunks))
    question = "B线有哪些阶段及其时长？"

    dense_results = retrieve(question,chunks,mat, k=3)
    bm25_results = bm25_search(question, chunks, k=3)
    hybrid_results = rrf_fusion(dense_results, bm25_results)[:3]
    print_results("Dense", dense_results)
    print_results("BM25", bm25_results)
    print_results("Hybrid", hybrid_results)

