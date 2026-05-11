import numpy as np

# ===================== 三刚体模型参数 =====================
m_T = 34.0       # kg, 躯干+头
m_A = 6.0        # kg, 双臂
m_L = 20.0       # kg, 双腿+足
M = m_T + m_A + m_L

d_T = 0.32       # m, 躯干质心到髋关节
d_A = 0.28       # m, 臂质心到肩关节
d_L = 0.30       # m, 腿质心到髋关节
L_T = 0.55       # m, 髋到肩(躯干长)
l_L = 0.80       # m, 腿长(髋到脚底)

I_T = 3.5        # kg m^2
I_A = 0.3
I_L = 4.3

# ===================== 约化距离系数 =====================
beta_T = (m_T * d_T + m_A * L_T) / M
beta_A = m_A * d_A / M
beta_L = m_L * d_L / M

# ===================== 附录系数 K =====================
K_TT = m_T * (d_T - beta_T)**2 + m_A * (L_T - beta_T)**2 + m_L * beta_T**2
K_AA = (m_T + m_L) * beta_A**2 + m_A * (d_A - beta_A)**2
K_LL = (m_T + m_A) * beta_L**2 + m_L * (d_L - beta_L)**2

K_TA = (-m_T * beta_A * (d_T - beta_T)
        + m_A * (d_A - beta_A) * (L_T - beta_T)
        + m_L * beta_A * beta_T)

K_TL = (-m_T * beta_L * (d_T - beta_T)
        - m_A * beta_L * (L_T - beta_T)
        - m_L * beta_T * (d_L - beta_L))

K_AL = (m_T * beta_A * beta_L
        - m_A * beta_L * (d_A - beta_A)
        - m_L * beta_A * (d_L - beta_L))

# ===================== A_i 系数函数 =====================
def compute_A(theta_T, theta_A, theta_L):
    cTA = np.cos(theta_T - theta_A)
    cTL = np.cos(theta_T - theta_L)
    cAL = np.cos(theta_A - theta_L)

    A_T = I_T + K_TT + K_TA * cTA + K_TL * cTL
    A_A = I_A + K_AA + K_TA * cTA + K_AL * cAL
    A_L = I_L + K_LL + K_TL * cTL + K_AL * cAL
    return A_T, A_A, A_L

# ===================== 控制输入 =====================
T_total = 0.5       # 腾空时间 (s)
dt = 0.001

# 收腿角速度 (rad/s)
phi_dot_LT_const = np.radians(200.0)  # 200 deg/s

# 摆臂角速度 (rad/s): 正弦半波, 向前摆
A_arm = np.radians(100.0)  # 幅值 100 deg/s
def phi_dot_TA(t):
    return A_arm * np.sin(np.pi * t / T_total)

# ===================== 初始角度 =====================
theta_T_0 = np.radians(60.0)    # deg
phi_TA_0  = np.radians(30.0)    # 臂相对躯干 +30 deg
phi_LT_0  = np.radians(-80.0)   # 腿相对躯干 -80 deg

theta_T = theta_T_0
phi_TA  = phi_TA_0
phi_LT  = phi_LT_0

# ===================== 数值积分 =====================
t = 0.0
time_vals = [t]
dx_vals = []
theta_T_vals = [theta_T]

# 初始 Δx
cosT = np.cos(theta_T)
cosA = np.cos(theta_T + phi_TA)
cosL = np.cos(theta_T + phi_LT)
x_B = l_L * cosL
x_G = (m_T * d_T * cosT
       + m_A * (L_T * cosT + d_A * cosA)
       + m_L * d_L * cosL) / M
dx_vals.append(x_B - x_G)

while t < T_total - dt / 2:
    # 当前角速度输入
    pd_TA = phi_dot_TA(t)
    pd_LT = phi_dot_LT_const

    # 计算 A 系数
    theta_A = theta_T + phi_TA
    theta_L = theta_T + phi_LT
    A_T, A_A, A_L = compute_A(theta_T, theta_A, theta_L)

    # 力学联络: ω_T 由臂腿角速度决定
    omega_T = -(A_A * pd_TA + A_L * pd_LT) / (A_T + A_A + A_L)

    # 欧拉更新
    theta_T += omega_T * dt
    phi_TA  += pd_TA * dt
    phi_LT  += pd_LT * dt
    t += dt

    # 计算 Δx
    theta_A = theta_T + phi_TA
    theta_L = theta_T + phi_LT
    cosT = np.cos(theta_T)
    cosA = np.cos(theta_A)
    cosL = np.cos(theta_L)
    x_B = l_L * cosL
    x_G = (m_T * d_T * cosT
           + m_A * (L_T * cosT + d_A * cosA)
           + m_L * d_L * cosL) / M
    dx = x_B - x_G

    time_vals.append(t)
    dx_vals.append(dx)
    theta_T_vals.append(theta_T)

# ===================== 输出 =====================
print("=" * 55)
print("三刚体模型数值积分结果")
print("=" * 55)
print(f"  beta_T = {beta_T:.4f}, beta_A = {beta_A:.4f}, beta_L = {beta_L:.4f}")
print(f"  K_TT = {K_TT:.4f}, K_AA = {K_AA:.4f}, K_LL = {K_LL:.4f}")
print(f"  K_TA = {K_TA:.4f}, K_TL = {K_TL:.4f}, K_AL = {K_AL:.4f}")
print()
print(f"  初始 theta_T = {np.degrees(theta_T_0):.1f} deg")
print(f"  初始 phi_TA  = {np.degrees(phi_TA_0):.1f} deg (臂在前)")
print(f"  初始 phi_LT  = {np.degrees(phi_LT_0):.1f} deg (腿在后)")
print(f"  初始 Delta_x  = {dx_vals[0]:.4f} m = {dx_vals[0]*100:.1f} cm")
print()
print(f"  落地 theta_T  = {np.degrees(theta_T_vals[-1]):.1f} deg")
print(f"  落地 phi_TA   = {np.degrees(phi_TA):.1f} deg")
print(f"  落地 phi_LT   = {np.degrees(phi_LT):.1f} deg")
print(f"  落地 Delta_x  = {dx_vals[-1]:.4f} m = {dx_vals[-1]*100:.2f} cm")
print()

# 对比: 相同收腿参数下，如果摆臂速率恒为零 (JRA 三体版)
# 重新积分
theta_T2 = theta_T_0
phi_TA2  = phi_TA_0
phi_LT2  = phi_LT_0
t2 = 0.0
dx2_initial = None
while t2 < T_total - dt / 2:
    pd_LT = phi_dot_LT_const
    pd_TA = 0.0  # 无摆臂
    theta_A2 = theta_T2 + phi_TA2
    theta_L2 = theta_T2 + phi_LT2
    A_T2, A_A2, A_L2 = compute_A(theta_T2, theta_A2, theta_L2)
    omega_T2 = -(A_A2 * pd_TA + A_L2 * pd_LT) / (A_T2 + A_A2 + A_L2)
    theta_T2 += omega_T2 * dt
    phi_TA2  += pd_TA * dt
    phi_LT2  += pd_LT * dt
    t2 += dt

    theta_A2 = theta_T2 + phi_TA2
    theta_L2 = theta_T2 + phi_LT2
    cosT2 = np.cos(theta_T2)
    cosA2 = np.cos(theta_A2)
    cosL2 = np.cos(theta_L2)
    x_B2 = l_L * cosL2
    x_G2 = (m_T * d_T * cosT2
            + m_A * (L_T * cosT2 + d_A * cosA2)
            + m_L * d_L * cosL2) / M
    dx2 = x_B2 - x_G2
    if dx2_initial is None:
        dx2_initial = dx2

print(f"  对照 (固定摆臂, pd_TA=0):")
print(f"    落地 Delta_x = {dx2:.4f} m = {dx2*100:.2f} cm")
print(f"    摆臂带来 Delta_x 增量 = {(dx_vals[-1] - dx2)*100:.2f} cm")
print(f"  二体模型 Delta_x = 0.3493 m = 34.93 cm")
