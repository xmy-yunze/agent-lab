import torch
torch.manual_seed(0)

TRUE_W=3.0
TRUE_B=5.0

x=torch.linspace(-2,2,100).unsqueeze(1)
y=TRUE_W*x+TRUE_B+0.5*torch.randn(x.shape)

w=torch.randn(1,1,requires_grad=True)
b=torch.randn(1,requires_grad=True)
lr=0.004

for step in range(1500):
    y_pred=w*x+b
    loss=((y_pred-y)**2).mean()
    loss.backward()
    with torch.no_grad():
        w-=lr*w.grad
        b-=lr*b.grad
        w.grad.zero_()
        b.grad.zero_()
    if step%300==0 or step==1499:
        print(f"step={step},loss={loss.item():.4f},w={w.item():.4f},b={b.item():.4f}")

print(f"\n学到的公式：y = {w.item():.4f} * x + {b.item():.4f}")
print(f"真实公式：y = {TRUE_W} * x + {TRUE_B}")