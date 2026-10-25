# agent-lab

Java 后端 + AI / Agent 工程双线发展的学习载体。用「出题 - 解题」积累可运行、可解释的成果。

## 为什么走这条路

Java 后端是已有基础，AI / Agent 是可以独立发展的技术路线。两条路线并行积累，未来根据能力、兴趣和就业机会选择方向。后端经验能帮助理解 Agent 工程中的运行时、上下文管理、工具协议和容错，但不限定使用的语言或职业方向。

Java 继续发展后端能力，Python 逐步发展独立构建 AI 应用与 Agent 系统的能力。AI / Agent 内部的 **A 模型原理线 + B 开发工程线**，与 Java / AI 两条职业发展路线区分；完整路线见 [`学习计划.md`](./学习计划.md)。

## 当前学习进度 · 第三周

**Advanced RAG + Agent 工程实践**：在 Python 基础 RAG 上做诊断、方案选择与对照验证，Day 6 对照已有 Java Agent Loop。下一步：**Day 2 · Query Transformation**。

| 天数 | 学习内容 | 状态 | 验收结果 |
|---|---|---|---|
| Day 1 | RAG 故障诊断 | ✅ 已完成 | **37/40（92.5%）**；8 dev Top-3、3 道生成测试；人工初步完整证据覆盖率 **5/6=83.3%** |
| Day 2 | Query Transformation | ⬜ 未开始 | 待验收 |
| Day 3 | BM25 + Hybrid Search | ⬜ 未开始 | 待验收 |
| Day 4 | Reranking | ⬜ 未开始 | 待验收 |
| Day 5 | RAG Evaluation | ⬜ 未开始 | 待验收 |
| Day 6 | ReAct 与已有 Agent 工程 | ⬜ 未开始 | 待验收 |
| Day 7 | 独立解决陌生问题 | ⬜ 未开始 | 待验收 |

任务与逐日打卡以 [`第三周-执行表.md`](./第三周-执行表.md) 为准。Day 1 的 case-03 检索证据不完整，case-04 正确拒答；详见 [Day 1 诊断报告](./research-assistant/rag-lab/reports/day1-diagnosis.md)。完整生成 Prompt / 原始回答日志尚未落盘；上述覆盖率为人工初步评估，不等同于正式宏平均 Recall@3，也不代表已有优化提升。

### 历史摘要

- **第一周已完成**：Python 基础调用、RAG 链路与故障复盘 → [`第一周-执行表.md`](./第一周-执行表.md)。
- **第二周主要任务已完成并验收**：Java 手写 Agent 循环（B 线 Day 1–4）+ PyTorch、反向传播、Excel 手算 Self-Attention（A 线 Day 5–7）→ [`第二周-执行表.md`](./第二周-执行表.md)。

Multi-Head Attention / Transformer Block 留待后续，尚未开始；Spring Boot validation 学习已暂停。

## 实践项目

| 产出物 | 核心问题 | 进展 |
|---|---|---|
| [`min-agent-loop/`](./min-agent-loop/题目.md) | Agent 循环如何决定下一步、执行工具并终止 | 已完成并验收；保留 Java 手写实现，不引 Agent 框架 |
| [`research-assistant/`](./research-assistant/题目.md) | 工具调用、检索与多轮记忆如何组合 | `rag-lab/` 检索实验进行中；完整项目要求尚未完成 |
| [`harness-demo/`](./harness-demo/题目.md) | 如何控制稳定性、成本并追查错误 | 未开始 |

每个项目的 `题目.md` 保留目标与验收标准；第三周 RAG 实验不等同于完整 research-assistant 项目验收。

## 怎么跑起来

在项目根目录准备 Python 环境，依赖以 `requirements.txt` 为准：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

按实际运行的脚本设置环境变量，Key 只保存在本地环境中，不写入代码或提交 Git：

```bash
# 历史 day1.py / day2.py：智谱 open.bigmodel.cn
export ZHIPU_API_KEY="你自己的智谱 Key"

# 当前 RAG 相关脚本及第三周实验：SiliconFlow api.siliconflow.cn
export SILICONFLOW_API_KEY="你自己的 SiliconFlow Key"
```

第三周固定基线见 [`baseline.json`](./research-assistant/rag-lab/config/baseline.json)：SiliconFlow，Embedding `BAAI/bge-m3`，生成模型 `zai-org/GLM-5.3-Flash`，Top-K=3。历史 `python/first/` 脚本的模型与资料输入可能不同，不能直接当作第三周固定基线重跑入口；实验细节以执行表与记录为准。

| 用途 | 运行方式（从项目根目录开始） |
|---|---|
| 历史模型调用 | `python3 python/first/day1.py` |
| 历史对话服务 | `cd python/first && uvicorn day2:app --reload`，访问 `http://127.0.0.1:8000/xmy/?message=你好` |
| 基础 RAG 检索 | `python3 python/first/day4.py` |
| 基础 RAG 问答 | `python3 python/first/day5.py "你的问题"` |
| 切分边界 / 标题栈观察 | `python3 python/first/day6.py` / `python3 python/first/day6_trace.py` |
| PyTorch 训练循环 | `python3 python/second/my_train.py` |
| 反向传播实验 | `python3 python/second/Backward.py` / `python3 python/second/Backward2.py` |

## 文档导航

| 需要了解什么 | 入口 |
|---|---|
| 当前任务、验收要求与每日打卡 | [`第三周-执行表.md`](./第三周-执行表.md) |
| 长期路线、A/B 线与学习安排 | [`学习计划.md`](./学习计划.md) |
| 广度自检与岗位覆盖 | [`了解清单.md`](./了解清单.md) |
| 协作方式与学习规则 | [`CODEBUDDY.md`](./CODEBUDDY.md) |
| RAG 复盘笔记 | [`notes/rag.md`](./notes/rag.md) |
| Self-Attention 手算表格 | [`notes/token.xlsx`](./notes/token.xlsx) |

从本目录开启会话，一次只推进当天任务；关窗口前将代码、结果与自己的解释落盘。详细过程写进对应执行表，README 只保留进度概览与入口。
