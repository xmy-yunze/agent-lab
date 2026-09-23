import numpy as np
from rag import split_chunks, embed, retrieve
    
chunks=split_chunks("学习计划.md")
mat=np.array(embed(chunks))
q="第二周的任务是什么？"

hits=retrieve(q,chunks,mat,k=3)

for idx,score,chunk in hits:
    preview=chunk[:60].replace("\n"," ")
    print(f"score={score:.4f} chunk={preview}...")