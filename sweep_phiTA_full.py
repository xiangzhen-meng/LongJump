import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ===================== 三刚体模型参数 =====================
m_T = 37.0; m_A = 7.0; m_L = 28.0; M = m_T + m_A + m_L
d_T = 0.32; d_A = 0.28; d_L = 0.35; L_T = 0.60; l_L = 0.95
I_T = 1.5; I_A = 0.3; I_L = 2.1

beta_T = (m_T*d_T + m_A*L_T) / M
beta_A = m_A*d_A / M
beta_L = m_L*d_L / M

K_TT = m_T*(d_T - beta_T)**2 + m_A*(L_T - beta_T)**2 + m_L*beta_T**2
K_AA = (m_T + m_L)*beta_A**2 + m_A*(d_A - beta_A)**2
K_LL = (m_T + m_A)*beta_L**2 + m_L*(d_L - beta_L)**2
K_TA = (-m_T*beta_A*(d_T - beta_T) + m_A*(d_A - beta_A)*(L_T - beta_T) + m_L*beta_A*beta_T)
K_TL = (-m_T*beta_L*(d_T - beta_T) - m_A*beta_L*(L_T - beta_T) - m_L*beta_T*(d_L - beta_L))
K_AL = (m_T*beta_A*beta_L - m_A*beta_L*(d_A - beta_A) - m_L*beta_A*(d_L - beta_L))

def run_jra(phi_TA_deg):
    T = 0.5; dt = 0.001
    pod_LT = np.radians(180.0)
    theta_T = np.radians(60.0)
    phi_TA = np.radians(phi_TA_deg)
    phi_LT = np.radians(-155.0)
    t = 0.0
    while t < T - dt/2:
        theta_A = theta_T + phi_TA
        theta_L = theta_T + phi_LT
        cTA = np.cos(theta_T - theta_A)
        cTL = np.cos(theta_T - theta_L)
        cAL = np.cos(theta_A - theta_L)
        A_T = I_T + K_TT + K_TA*cTA + K_TL*cTL
        A_A = I_A + K_AA + K_TA*cTA + K_AL*cAL
        A_L = I_L + K_LL + K_TL*cTL + K_AL*cAL
        omega_T = -(A_A*0 + A_L*pod_LT) / (A_T + A_A + A_L)
        theta_T += omega_T*dt
        phi_LT += pod_LT*dt
        t += dt
    theta_A = theta_T + phi_TA
    theta_L = theta_T + phi_LT
    dx = l_L*np.cos(theta_L) - (
        m_T*d_T*np.cos(theta_T)
        + m_A*(L_T*np.cos(theta_T) + d_A*np.cos(theta_A))
        + m_L*d_L*np.cos(theta_L)
    ) / M
    return dx, np.degrees(theta_T), np.degrees(theta_L)

# ===================== 全角度扫描 =====================
phis = np.arange(0, 361, 1)
dxs = np.zeros_like(phis, dtype=float)

for i, phi in enumerate(phis):
    dxs[i], _, _ = run_jra(phi)

# ===================== 绘图 =====================
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(phis, dxs, 'b-', linewidth=1.5, label=r'$\Delta x$ (JRA, $\dot\varphi_{TA}=0$)')
ax.axhline(y=0.31, color='tab:orange', linestyle='--', linewidth=1.2, alpha=0.8,
           label=r'Exp. JFA: $\Delta x = 0.31$ m')
ax.axhline(y=0.29, color='tab:red', linestyle='--', linewidth=1.2, alpha=0.8,
           label=r'Exp. JRA: $\Delta x = 0.29$ m')

# 关键角度标注
for phi_tag, color in [(145, 'tab:green'), (180, 'tab:purple')]:
    dx_val = dxs[phi_tag]
    ax.plot(phi_tag, dx_val, 'o', color=color, markersize=8, zorder=5)
    offset_x = -45 if phi_tag < 360 else -20
    ax.annotate(r'$\varphi_{TA}=%d^{\circ}$'%phi_tag + f'\n$\\Delta x={dx_val:.3f}$ m',
                xy=(phi_tag, dx_val),
                xytext=(phi_tag + offset_x, dx_val + 0.007),
                fontsize=9, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

# 极值标注
ax.annotate(r'$\varphi_{TA}=180^{\circ}$ (min)', xy=(180, dxs[180]),
            xytext=(195, dxs[180] - 0.018), fontsize=8, color='tab:purple',
            arrowprops=dict(arrowstyle='->', color='tab:purple', lw=0.8))

idx_max = np.argmax(dxs)
ax.annotate(f'${phis[idx_max]}^{{\\circ}}$ (max: ${dxs[idx_max]:.3f}$ m)',
            xy=(phis[idx_max], dxs[idx_max]),
            xytext=(phis[idx_max] + 12, dxs[idx_max] + 0.002),
            fontsize=8, color='gray',
            arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

# 区间阴影
ax.axvspan(0, 360, alpha=0.03, color='gray')

ax.set_xlabel(r'Fixed arm angle $\varphi_{TA}$ ($^\circ$)', fontsize=12)
ax.set_ylabel(r'Landing foot protrusion $\Delta x$ (m)', fontsize=12)
ax.set_title(r'$\Delta x$ vs. static arm angle $\varphi_{TA}$ in three-body JRA ($L_0=0$)', fontsize=13)
ax.legend(fontsize=9, loc='lower left')
ax.set_xlim(0, 360)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fig_phiTA_sweep.pdf', dpi=150, bbox_inches='tight')
plt.savefig('fig_phiTA_sweep.png', dpi=150, bbox_inches='tight')
print("Saved: fig_phiTA_sweep.pdf, fig_phiTA_sweep.png")
print(f"Min Δx = {dxs[180]:.4f} m at φ_TA=180°")
print(f"φ_TA=145° Δx = {dxs[145]:.4f} m")
print(f"Δx(145°) - Δx(180°) = {dxs[145]-dxs[180]:.4f} m")
