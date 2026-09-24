import os, tempfile
from rag import split_chunks

CASES = {
    "标准 ##/###": """## 一
正文
### 小
正文
""",
    "全是一级 #": """# 一
正文
# 二
正文
""",
    "夹着四级 ####": """## 一
正文
#### 小标题
正文
""",
    "完全没标题": """一段话。
又一段。
""",
    "代码块里的 #": """## 一
正文
```
### 假标题
```
正文
""",
}

for name, text in CASES.items():
    path = os.path.join(tempfile.mkdtemp(), "t.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    chunks = split_chunks(path)
    print(f"{name:14} → {len(chunks)} 段  {[c.split(chr(10))[0][:16] for c in chunks]}")
