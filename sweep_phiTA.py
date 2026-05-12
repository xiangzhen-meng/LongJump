import numpy as np

# ===================== 三刚体模型参数 =====================
m_T = 37.0
m_A = 7.0
m_L = 28.0
M = m_T + m_A + m_L

d_T = 0.32
d_A = 0.28
d_L = 0.35
L_T = 0.60
l_L = 0.95

I_T = 1.5
I_A = 0.3
I_L = 2.1

beta_T = (m_T * d_T + m_A * L_T) / M
beta_A = m_A * d_A / M
beta_L = m_L * d_L / M

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

def compute_A(theta_T, theta_A, theta_L):
    cTA = np.cos(theta_T - theta_A)
    cTL = np.cos(theta_T - theta_L)
    cAL = np.cos(theta_A - theta_L)
    A_T = I_T + K_TT + K_TA * cTA + K_TL * cTL
    A_A = I_A + K_AA + K_TA * cTA + K_AL * cAL
    A_L = I_L + K_LL + K_TL * cTL + K_AL * cAL
    return A_T, A_A, A_L

def run_jra(phi_TA_deg):
    T_total = 0.5
    dt = 0.001
    phi_dot_LT = np.radians(180.0)
    
    theta_T = np.radians(60.0)
    phi_TA = np.radians(phi_TA_deg)
    phi_LT = np.radians(-155.0)
    t = 0.0
    
    while t < T_total - dt/2:
        theta_A = theta_T + phi_TA
        theta_L = theta_T + phi_LT
        A_T, A_A, A_L = compute_A(theta_T, theta_A, theta_L)
        omega_T = -(A_A * 0.0 + A_L * phi_dot_LT) / (A_T + A_A + A_L)
        theta_T += omega_T * dt
        phi_LT += phi_dot_LT * dt
        t += dt
    
    theta_A = theta_T + phi_TA
    theta_L = theta_T + phi_LT
    cosT = np.cos(theta_T)
    cosA = np.cos(theta_A)
    cosL = np.cos(theta_L)
    x_B = l_L * cosL
    x_G = (m_T * d_T * cosT + m_A * (L_T * cosT + d_A * cosA) + m_L * d_L * cosL) / M
    dx = x_B - x_G
    return {
        'phi_TA': phi_TA_deg,
        'theta_T': np.degrees(theta_T),
        'theta_L': np.degrees(theta_L),
        'dx': dx
    }

# 扫描 0° 到 180°
print(f"{'phi_TA(°)':>10} {'theta_T(°)':>12} {'theta_L(°)':>12} {'Δx(m)':>10} {'Δx(cm)':>10}")
print("-" * 56)

target = 0.31
best = None
best_err = float('inf')

for deg in range(0, 181, 5):
    r = run_jra(deg)
    err = abs(r['dx'] - target)
    if err < best_err:
        best_err = err
        best = r
    marker = " ***" if err < 0.005 else ""
    print(f"{deg:10.0f} {r['theta_T']:12.1f} {r['theta_L']:12.1f} {r['dx']:10.4f} {r['dx']*100:10.2f}{marker}")

print()
print(f"最佳匹配: φ_TA = {best['phi_TA']:.0f}°, "
      f"Δx = {best['dx']:.4f} m, "
      f"误差 = {abs(best['dx']-target):.4f} m")
print(f"  theta_T = {best['theta_T']:.1f}°, theta_L = {best['theta_L']:.1f}°")

# 精细扫描 best 附近 ±5°
print()
print("精细扫描 best 附近:")
for deg in np.arange(best['phi_TA'] - 4, best['phi_TA'] + 5, 1):
    r = run_jra(deg)
    err = abs(r['dx'] - target)
    marker = " ***" if err < 0.001 else ""
    print(f"{deg:10.1f} {r['theta_T']:12.1f} {r['theta_L']:12.1f} {r['dx']:10.4f} {r['dx']*100:10.2f}{marker}")
