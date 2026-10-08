import torch
torch.manual_seed(0)  # 固定随机种子：每次跑结果一样

x=torch.tensor(2.0)
y=torch.tensor(11.0)

w=torch.tensor(2.0,requires_grad=True)
b=torch.tensor(5.0,requires_grad=True)
lr=0.1

y_hat=w*x+b
loss=(y_hat-y)**2
print("y_hat =", y_hat)
print("loss =", loss)
loss.backward()
print("d_loss_d_w =", w.grad)
print("d_loss_d_b =", b.grad)
with torch.no_grad():
    w-=lr*w.grad
    b-=lr*b.grad
print("w =", w)
print("b =", b)
y_hat=w*x+b
newloss=(y_hat-y)**2
print("newy_hat =", y_hat)
print("newloss =", newloss)