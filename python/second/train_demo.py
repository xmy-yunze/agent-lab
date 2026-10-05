# train_demo.py —— A 线第一个例子：训练循环的裸形状
# 业务域故意选「华氏-摄氏换算」，跟你今天要写的任务不同域，所以它是例子不是答案。
#
# 物理规律：F = 1.8 * C + 32。
# 「训练」就是：不给模型这个公式，只给它 50 组 (C, F) 数据点，
# 让它自己把 1.8 和 32 这两个数「学」出来。
#
# Java 对照：
#   torch.tensor ≈ 多维数组（int[][] 的加强版），但它会记住「自己参与了哪些运算」
#   requires_grad=True ≈ 给这个变量打开「记账开关」，之后才知道该往哪调
#   loss.backward() ≈ 自动求导：算出 loss 对每个参数的导数（明天的作业是手写这个）

import torch

torch.manual_seed(0)  # 固定随机种子：让每次跑的结果一样（Java 对照：new Random(0)）

# ========== 第 0 步：张量基本操作（Day 5 动手做第 2 条） ==========

# 创建：一维张量（对照 Java 的 double[]，但只装一种类型）
temps_c = torch.tensor([-10.0, 0.0, 37.0, 100.0])
print("一维张量:", temps_c)
print("形状:", temps_c.shape)  # 形状 [4] —— 有 4 个数

# 矩阵乘：torch.matmul(A, B)，要求 A 的列数 = B 的行数（和线代一模一样）
# [2,3] 的矩阵乘 [3,2] 的矩阵 → [2,2]
A = torch.tensor([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])          # 形状 [2, 3]
B = torch.tensor([[1.0, 0.0],
                  [0.0, 1.0],
                  [1.0, 1.0]])               # 形状 [3, 2]
print("矩阵乘结果:\n", torch.matmul(A, B))   # [2,2]，手算可验

print("\n========== 训练循环开始 ==========\n")

# ========== 第 1 步：造数据（带一点噪声，更真实） ==========
C = torch.linspace(-10.0, 38.0, 50).unsqueeze(1)   # 50 个摄氏度，形状 [50, 1]
F = 1.8 * C + 32 + 0.5 * torch.randn(C.shape)      # 对应华氏度 = 真实公式 + 噪声

# ========== 第 2 步：定义「模型」—— 只有 w、b 两个参数 ==========
# 学到的目标：w 趋近 1.8，b 趋近 32
w = torch.randn(1, 1, requires_grad=True)   # requires_grad=True ← 自动求导总开关
b = torch.randn(1, requires_grad=True)     # 没有 True 的话 backward 会报错

lr = 0.002    # 学习率：每步往好方向挪多大（⚠️ 0.01 会震荡爆炸 → loss 飞到 inf/nan，可自己改坏试试）

for step in range(3000):

    # ---------- 前向：拿当前 w、b 算预测 ----------
    F_pred = w * C + b                     # 一行就是「模型」：y = w*x + b

    # ---------- 算损失：预测离真实平均差多远 ----------
    loss = ((F_pred - F) ** 2).mean()      # MSE：差值平方再取平均（都是正数，不会正负抵消）

    # ---------- 反向传播：自动算出 dL/dw 和 dL/db ----------
    loss.backward()                       # 算完 w.grad / b.grad 里就有数了

    # ---------- 更新参数：往「让 loss 更小」的方向挪一步 ----------
    with torch.no_grad():                  # 更新本身不需要记账，先关掉
        w -= lr * w.grad                   # w = w - lr * 梯度（梯度指 loss 上升最快方向，所以减）
        b -= lr * b.grad
        w.grad.zero_()                     # 清零！不清零下一轮会累加（阴坑）
        b.grad.zero_()

    if step % 500 == 0 or step == 2999:
        print(f"step {step:3d}  loss={loss.item():10.4f}  w={w.item():.4f}  b={b.item():.4f}")

print(f"\n学到的公式：F = {w.item():.3f} * C + {b.item():.3f}")
print(f"真实公式是：F = 1.800 * C + 32.000")
print(f"loss 从开头的数一路降下来了 —— 这就是「模型在学」。")
