import numpy as np
import matplotlib.pyplot as plt

# ===================== 参数设置 =====================
m1 = 40.0      # kg
m2 = 20.0
M = m1 + m2
mu = (m1 * m2) / M

d1 = 0.35      # m
d2 = 0.30
l2 = 0.80      # 腿长

I1 = 4.8       # kg·m²
I2 = 4.3

# 起跳初始角度 (度 -> 弧度)
theta1_0 = np.radians(60.0)
theta2_0 = np.radians(-20.0)
phi_0 = theta2_0 - theta1_0

# 主动收腿角速度 (rad/s), 正表示腿向前摆
Omega = np.radians(200.0)   # 200°/s

T_total = 0.5   # 腾空总时间 (s)
dt = 0.001      # 时间步长

# ===================== 状态更新函数 =====================
def dtheta1_dt(phi, omega):
    cos_phi = np.cos(phi)
    A = I2 + mu * d2**2 - mu * d1 * d2 * cos_phi
    B = I1 + I2 + mu * (d1**2 + d2**2) - 2 * mu * d1 * d2 * cos_phi
    if abs(B) < 1e-8:
        return 0.0
    return - (A / B) * omega

# 初始化
t = 0.0
theta1 = theta1_0
theta2 = theta2_0
phi = theta2 - theta1

# 记录结果 (在循环前先记录初始状态)
time_vals = [t]
dx_vals = []
# 计算初始 Δx
cos1 = np.cos(theta1)
cos2 = np.cos(theta2)
xB = l2 * cos2
xG = (m1 * d1 * cos1 + m2 * d2 * cos2) / M
dx_vals.append(xB - xG)

# ===================== 数值积分 (欧拉法) =====================
while t < T_total - dt/2:
    # 1. 计算当前角速度
    omega_phi = Omega   # 常数
    dot_theta1 = dtheta1_dt(phi, omega_phi)
    dot_theta2 = dot_theta1 + omega_phi
    
    # 2. 欧拉更新
    theta1 += dot_theta1 * dt
    phi += omega_phi * dt
    theta2 = theta1 + phi   # 保证 theta2 由 theta1 和 phi 决定
    t += dt
    
    # 3. 计算 Δx
    cos1 = np.cos(theta1)
    cos2 = np.cos(theta2)
    xB = l2 * cos2
    xG = (m1 * d1 * cos1 + m2 * d2 * cos2) / M
    dx = xB - xG
    
    # 存储
    time_vals.append(t)
    dx_vals.append(dx)

# ===================== 输出结果 =====================
print(f"落地时刻 t = {T_total} s 时的 Δx = {dx_vals[-1]:.4f} m = {dx_vals[-1]*100:.2f} cm")

# 绘图 (现在 time_vals 和 dx_vals 长度相同)
plt.figure(figsize=(8,5))
plt.plot(time_vals, np.array(dx_vals)*100, linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Δx (cm)")
plt.title("脚相对于质心的水平偏移随时间变化 (含精确轨道项)")
plt.grid(True)
plt.show()