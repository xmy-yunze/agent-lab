import torch
torch.manual_seed(0)

x = torch.tensor(2.0)
y = torch.tensor(10.0)
lr = 0.01

w1 = torch.tensor(1.0, requires_grad=True)
b1 = torch.tensor(1.0, requires_grad=True)
w2 = torch.tensor(2.0, requires_grad=True)
b2 = torch.tensor(1.0, requires_grad=True)

h = w1 * x + b1
y_hat = w2 * h + b2
loss = (y_hat - y) ** 2

print("loss =", loss.item())          # 9.0

# 手动链式求导：梯度全部存到普通变量
dL_dyhat = 2 * (y_hat - y)            # -6  (d loss / d y_hat)
dL_dh    = dL_dyhat * w2              # -12 (d loss / d h)
dw1 = dL_dh * x                       # -24
db1 = dL_dh                           # -12
dw2 = dL_dyhat * h                    # -18
db2 = dL_dyhat                        # -6

with torch.no_grad():
    w1 -= lr * dw1
    b1 -= lr * db1
    w2 -= lr * dw2
    b2 -= lr * db2

h_new = w1 * x + b1
y_hat_new = w2 * h_new + b2
newloss = (y_hat_new - y) ** 2
print("newloss =", newloss.item())    # ≈1.19
