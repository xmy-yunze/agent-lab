# agent-lab

AI 与 Agent 的学习载体。用「出题 - 解题」的方式，把后端能力延伸到 AI 工程。

## 为什么走这条路

Agent 岗位实际分三层。模型/算法层要 ML 背景，跟我们无关；应用/编排层门槛低、容易被替代；**中间那层 Harness（运行时、上下文管理、工具协议、容错、可观测性、成本控制）就是后端工程**，只是换了名字。

概念其实一一对应：

| Agent 里的叫法 | 后端早就有的东西 |
|---|---|
| Agent 循环 / 工具调用 | 状态机、工作流引擎 |
| 上下文工程 / 上下文压缩 | 会话管理、缓存治理 |
| Memory 短期 / 长期记忆 | 数据库、向量检索 |
| Tool Schema / 函数调用 | 接口契约、API 网关 |
| MCP / A2A 协议 | RPC 协议、服务发现 |
| 权限分级 / 沙箱隔离 | 鉴权、多租户隔离 |
| 重试 / 成本护栏 | 熔断限流、配额幂等 |
| Trace / Replay 回放 | 链路追踪、日志回放 |

所以不需要转行，是把已有的东西接上去。

> 📄 完整学习计划见 **[`学习计划.md`](./学习计划.md)** —— 双线并行：**算法模型线（认知级 · 30%）+ 开发工程线（实战级 · 70%）**
> ✅ 了解级自检问题 + 岗位覆盖清单见 **[`了解清单.md`](./了解清单.md)**

## 当前阶段

**2026-09-20 起 · 第一周已完成（09-24 收工）· 第二周进行中**

- Spring Boot validation 的学习**已暂停**，精力转到 Agent 学习。
- **第一周（热身 + RAG 认知线）全程 Python**，逐日产出见 [`第一周-执行表.md`](./第一周-执行表.md)；跨产出物的笔记在 [`notes/rag.md`](./notes/rag.md)。
- **第二周起切回 Java**：正在走 **[`第二周-执行表.md`](./第二周-执行表.md)** —— B 线 4 天开工产出物一 `min-agent-loop`（手写 Agent 循环，**不引 Spring AI / LangChain4j**）+ A 线 3 天（PyTorch → 手撕网络 → Excel 手算注意力）。
- 正式产出物的技术栈按 **[`CODEBUDDY.md`](./CODEBUDDY.md)** 走：**Java 17 + Spring Boot 4.0.7 + Gradle**。

### 第一周进度（RAG 认知线）

| Day | 做什么 | 状态 | 产出 |
|---|---|---|---|
| 1 | 让模型开口说话 | ✅ | `python/day1.py` |
| 2 | 把它变成一个服务 | ✅ | `python/day2.py` |
| 3 | 给它一份自己的资料（文档切分） | ✅ | `python/day3.py` |
| 4 | 把意思变成数字（embedding + numpy 手算相似度） | ✅ | `python/day4.py` |
| 5 | 串成一个完整的 RAG | ✅ | `python/day5.py` + `python/rag.py` |
| 6 | 故意把它弄坏（本周最值钱的一天） | ✅ | `python/day6.py` + `python/day6_trace.py` |
| 7 | 回头看，写下来（一页纸讲清 RAG） | ✅ | `notes/rag.md` |

每天**卡在哪、花了多久、以及当天最值钱的认知**，都记在 [`第一周-执行表.md`](./第一周-执行表.md) 的「打卡区」里 —— 那里比这张表有信息量。

### 第二周进度（Java 手写 Agent 循环 + A 线 Transformer 地基）

| Day | 线 | 做什么 | 状态 | 产出 |
|---|---|---|---|---|
| 1 | B | 让 Java 说得上话（工程 + 手写 HTTP + Tool 结构） | ⬜ | `min-agent-loop/` |
| 2 | B | 让它自己决定调哪个工具（2 个工具 + `while` 循环） | ⬜ | — |
| 3 | B | 让它知道什么时候该停（三层终止条件） | ⬜ | — |
| 4 | B | 工具加到 10 个 + 产出物一验收 | ⬜ | `min-agent-loop/笔记.md` |
| 5 | A | 先把 PyTorch 跑起来 | ⬜ | — |
| 6 | A | 手撕一个神经网络（前向 + 反向传播） | ⬜ | — |
| 7 | A | 用 Excel 手算注意力（Q/K/V） | ⬜ | — |

## 学习地图

**只做下面这三件事，做完再说别的。**

| 顺序 | 产出物 | 要搞明白的核心问题 | 状态 |
|---|---|---|---|
| 1 | `min-agent-loop/` | Agent 循环到底长什么样？它凭什么能自己决定下一步 | **进行中**（第二周 Day 1-4） |
| 2 | `research-assistant/` | 工具调用 + 检索 + 多轮记忆怎么装到一起 | 未开始 |
| 3 | `harness-demo/` | 怎么让它跑得稳、跑得便宜、出错了能查 | 未开始 |

每个目录里有 `题目.md`，写清了目标、要求和验收标准。按顺序来，别跳。

## 怎么用这个文件夹

1. **从本目录打开会话**（不是桌面，不是别的文件夹）
2. 一次只推进一个产出物
3. 学完先把成果落盘，再关窗口

第 3 条是关键。窗口可以随便新开，但产出必须先落地，否则这个文件夹也会变成垃圾堆。

## 怎么跑起来

第一周的脚本都在 `python/`，直接依赖只有 4 个（`requests` / `fastapi` / `uvicorn` / `numpy`），另需一个模型 API Key。

```bash
python3 -m venv .venv && source .venv/bin/activate

# 国内建议加镜像加速：-i https://pypi.tuna.tsinghua.edu.cn/simple
python3 -m pip install -r requirements.txt

# 模型接口走智谱（open.bigmodel.cn）。Key 只放环境变量，不进代码、不进 Git。
export ZHIPU_API_KEY="你自己的 Key"
```

| 脚本 | 怎么跑（都在项目根目录下） | 看到什么 |
|---|---|---|
| `python/day1.py` | `python3 python/day1.py` | 终端打印出模型的一句话 |
| `python/day2.py` | `cd python && uvicorn day2:app --reload` | 浏览器开 `127.0.0.1:8000/xmy/?message=你好` 能跟模型对话 |
| `python/day3.py` | `python3 python/day3.py` | 把 `学习计划.md` 切成 10 段，打印每段长度和开头 |
| `python/day4.py` | `python3 python/day4.py` | 换一个问题，按相关度**从高到低**打印最相关的 3 段及分数（检索逻辑已抽到 `rag.py`） |
| `python/rag.py` | （不单独跑，被 day4 / day5 共用） | 检索这条线上的三件事：`split_chunks`（切分，**带标题路径 + 认代码围栏**）/ `embed`（向量化）/ `retrieve`（算分排序取 top-k） |
| `python/day5.py` | `python3 python/day5.py "你的问题"` | **完整 RAG**：检索 top-3 → 拼进提示（带 `[1][2][3]` 编号）→ 让模型只依据资料回答并标注引用编号（问题从命令行参数进，缺省用 `KV Cache 是什么？`） |
| `python/day6.py` | `python3 python/day6.py` | 五个**切分边界** case（标准 `##/###`、全是 `#`、夹 `####`、完全没标题、**代码块里的假标题**）各切出几段 —— 用来暴露正则和围栏识别的边界 |
| `python/day6_trace.py` | `python3 python/day6_trace.py` | **标题栈观察台**：逐行打印「行号 / 内容 / 判定 / 栈」看标题路径怎么生成；并给出三份文档修复前后的段数、以及「B 线」关键词覆盖的段数对照 |

## 进度记录

- **第一周逐日进度** → [`第一周-执行表.md`](./第一周-执行表.md) 的「打卡区」：每天卡在哪、花了多久、以及当天最值钱的认知。
- **第二周逐日进度** → [`第二周-执行表.md`](./第二周-执行表.md)：Java 手写 Agent 循环（B 线 4 天）+ A 线 Transformer 地基（3 天）。
- **三个正式产出物** → 上面「学习地图」表的「状态」列，开一个改一个。
- 跨产出物的通用笔记放 `notes/`（当前一篇：[`notes/rag.md`](./notes/rag.md) —— Day 7 的「一页纸讲清 RAG」）。
