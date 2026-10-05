"""
Day 6 · 标题栈观察台（教学脚本，不是生产代码）

用途：把「逐行扫 + 标题栈」这件事打印出来看，看清它是怎么走的。
跑法：.venv/bin/python python/day6_trace.py

⚠️ 真正要改的是 rag.py 里的 split_chunks —— 那份由你自己敲。
   这个脚本只负责：① 让你看见栈怎么动 ② 给你一个「靶子」（修复后应该是多少段）
"""

import os
import re

HEADING_RE = re.compile(r"^(#{1,6}) +(.*)$")
MIN_SPLIT_LEVEL = 2          # 最低切分级别：2 表示 ## 及以上才切，# 不切

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = ["学习计划.md", "第一周-执行表.md", "README.md"]

# ============================================================
# 第 0 部分：迷你文档（就是我给你的那张表）
# ============================================================
DEMO = """# 学习计划
导语
## 三、B 线
B 线占 70%
### B1 · 最小可跑
只学基本语法"""


# ============================================================
# 第 1 部分：走一遍，只看「栈」怎么动
# ============================================================
def trace(lines, title, show_buf=False):
    """逐行走，每步打印：行号 / 内容 / 判定 / 栈"""
    print()
    print("=" * 96)
    print(f"【走一遍】{title}")
    print("=" * 96)
    print(f"{'行':<4}{'内容':<26}{'判定':<36}栈（祖先 → 自己）")
    print("-" * 96)

    stack = []

    for lineno, line in enumerate(lines, start=1):
        shown = (line[:22] + "…") if len(line) > 22 else line
        m = HEADING_RE.match(line)

        if not m:
            print(f"{lineno:<4}{shown:<26}{'正文（攒进 buf）':<36}{' / '.join(t for _, t in stack) or '(空)'}")
            continue

        level = len(m.group(1))
        head_title = m.group(2).strip()

        if level >= MIN_SPLIT_LEVEL:
            # 封口时用的前缀 = 栈去掉栈顶（因为栈顶是"当前段自己"）
            prefix = " > ".join(t for _, t in stack[:-1])
            verdict = f"★ 切段（封口前缀 = {prefix!r}）"
        else:
            verdict = f"H{level} 不切，只进栈"

        # 先弹到父层，再把自己挂上去
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, head_title))

        path = " / ".join(t for _, t in stack)
        print(f"{lineno:<4}{shown:<26}{verdict:<36}{path}")

    print()


# ============================================================
# 第 2 部分：参考实现（靶子用）
# ------------------------------------------------------------
# ⚠️ 建议：先别看这段，自己按观察到的规律写一版 split_chunks，
#    写完了再回来对拍。对不上再回来看。
# ============================================================
def reference_split(text):
    """带标题路径的切分：每段正文前面拼上它的祖先标题链"""
    stack = []      # [(level, title), ...] 栈顶 = 当前段自己的标题
    chunks = []
    buf = []        # 当前段正在攒的行

    def seal():
        """给 buf 里攒着的这一段封口"""
        if not buf:
            return
        body = "\n".join(buf).strip()
        buf.clear()
        if not body:
            return
        prefix = " > ".join(t for _, t in stack[:-1])   # 去掉栈顶 = 只留祖先
        chunks.append(prefix + "\n" + body if prefix else body)

    for line in text.split("\n"):
        m = HEADING_RE.match(line)
        if not m:
            buf.append(line)
            continue
        level = len(m.group(1))
        if level >= MIN_SPLIT_LEVEL:
            seal()                                      # ① 先给上一段封口
        while stack and stack[-1][0] >= level:          # ② 退回到父层
            stack.pop()
        stack.append((level, m.group(2).strip()))       # ③ 挂上自己
        buf.append(line)                                # ④ 标题行自己进段
    seal()                                              # ⑤ 收尾，别漏最后一段
    return chunks


def old_split(text):
    """你现在 rag.py 里的那份（无标题路径）"""
    raw = re.split(r"\n(?=#{2,} )", text)
    return [c for c in raw if len(c) != 0]


# ============================================================
# 运行
# ============================================================
if __name__ == "__main__":
    # ---- 第 1 部分：迷你文档走一遍（含 buf 实况）----
    trace(DEMO.split("\n"), "迷你文档（6 行）")

    print("=" * 96)
    print("【看结果】迷你文档切出来是这 3 段（整段原文，一眼看清前缀拼在哪）：")
    print("=" * 96)
    for i, c in enumerate(reference_split(DEMO), start=1):
        print(f"  段{i}  {c!r}")
    print("  ↑ 注意 段1 没有前缀（它是根，祖先为空）；段3 的前缀最长（祖先是两级）")
    print()

    # ---- 第 2 部分：挑战关卡（写完自己的版本再来对）----
    for name in DOCS:
        path = os.path.join(ROOT, name)
        if not os.path.exists(path):
            print(f"  (跳过，不存在：{path})")
            continue
        text = open(path, encoding="utf-8").read()
        old = old_split(text)
        new = reference_split(text)
        print(f"  {name:<22} 修复前 {len(old):>3} 段  →  修复后 {len(new):>3} 段")

    print()
    print("=" * 96)
    print('【靶子】"B 线"这两个字，到底出现在多少段里？（直接决定检索能不能捞到）')
    print("=" * 96)
    text = open(os.path.join(ROOT, "学习计划.md"), encoding="utf-8").read()
    old, new = old_split(text), reference_split(text)
    KEY = "B 线"

    if len(old) != len(new):
        print(f"  ⚠️ 段数不一致（{len(old)} vs {len(new)}），下面的逐段对照可能对不齐")

    print(f"\n  修复前：{sum(KEY in c for c in old):>2} / {len(old)} 段 含「{KEY}」")
    print(f"  修复后：{sum(KEY in c for c in new):>2} / {len(new)} 段 含「{KEY}」")

    gained = [i for i in range(min(len(old), len(new))) if KEY not in old[i] and KEY in new[i]]
    if gained:
        print(f"\n  ↓ 这 {len(gained)} 段是修复后*新拿到*「{KEY}」字样的 —— 它们正文里没写，是前缀带进来的：")
        for i in gained:
            print(f"\n  段{i + 1} · 修复前（{len(old[i])} 字）第二行：")
            print(f"      {old[i].splitlines()[1]!r}")
            print(f"  段{i + 1} · 修复后（{len(new[i])} 字）前两行：")
            print(f"      {new[i].splitlines()[0]!r}")
            print(f"      {new[i].splitlines()[1]!r}")
    print()
    print("  这就是「标题路径」的全部作用：不改边界、不改段数，只给每段补上它的来路。")
    print("  段数一个字没变（23→23），但「B 线」的可检索范围从上面那个数变成下面那个数。")
    print()
