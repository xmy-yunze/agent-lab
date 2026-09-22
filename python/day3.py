path="学习计划.md"

with open(path,encoding="utf-8") as f:
    text = f.read()
print(len(text))

raw=text.split("\n## ")

chunks=[c for c in raw if len(c)!=0]
print(len(chunks))


for i in range(len(chunks)):
    print(i, len(chunks[i]), chunks[i][:50])  

