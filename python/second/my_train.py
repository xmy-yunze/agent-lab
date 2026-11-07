import torch
torch.manual_seed(0)  # 固定随机种子：每次跑结果一样

TRUE_W=3.0  #真值斜率
TRUE_B=5.0  #真值截距

x=torch.linspace(-2,2,100).unsqueeze(1)         # 100 个 x，形状 [100, 1]
y=TRUE_W*x+TRUE_B+0.5*torch.randn(x.shape)      # 对应 y = 真实公式 + 噪声

w=torch.randn(1,1,requires_grad=True)       # requires_grad=True ← 自动求导总开关
b=torch.randn(1,requires_grad=True)         # 没有 True 的话 backward 会报错
lr=0.004        # 学习率：每步往好方向挪多大

for step in range(1500):
    # ① 前向：拿当前 w、b 算预测 —— 一行就是「模型」：y = w*x + b
    y_pred=w*x+b

    # ② 算损失：预测离真实平均差多远
    loss=((y_pred-y)**2).mean()

    # ③ 反向传播：自动算出 dL/dw 和 dL/db，结果存进 w.grad / b.grad
    loss.backward()

    # ④ 更新参数：往「让 loss 更小」的方向挪一步
    with torch.no_grad():
        w-=lr*w.grad
        b-=lr*b.grad

        # ⑤ 清零梯度！不清零下一轮会累加
        w.grad.zero_()
        b.grad.zero_()
        # 每隔一段打印一次，看 loss 有没有在降
    if step%300==0 or step==1499:
        print(f"step={step},loss={loss.item():.4f},w={w.item():.4f},b={b.item():.4f}")

print(f"\n学到的公式：y = {w.item():.4f} * x + {b.item():.4f}")
print(f"真实公式：y = {TRUE_W} * x + {TRUE_B}")