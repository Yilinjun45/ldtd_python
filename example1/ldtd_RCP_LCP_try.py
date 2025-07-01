import lumapi
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

c = 3e8  # 光速，单位 m/s

# ─────────────────────────────────────────────
# 1. 启动 FDTD 会话并载入项目
# ─────────────────────────────────────────────
fdtd = lumapi.FDTD(r"D:\桌面\大创\FDTD_trying\复现fdtd.fsp")
def run_fdtd(phase2: float):
    fdtd.switchtolayout()
    # 设置两个偏振源
    fdtd.setnamed("source_1", "polarization angle", 0)
    fdtd.setnamed("source_1", "phase", 0)
    fdtd.setnamed("source_2", "polarization angle", 90)
    fdtd.setnamed("source_2", "phase", phase2)
    fdtd.run()
    exf = fdtd.getdata("T", "Ex")
    ex = np.mean(exf, axis=(0, 1, 2))  # shape = (F,)
    eyf = fdtd.getdata("T", "Ey")
    ey = np.mean(eyf, axis=(0, 1, 2))
    f = fdtd.getdata("T", "f").squeeze()

    return ex, ey, f

#ex_L, ey_L, f_L = run_fdtd(90)   # LCP 入射
ex_R, ey_R, f_R = run_fdtd(-90)  # RCP 入射

# LCP 入射
#EL_L = (ex_L + 1j * ey_L) / 2  # LCP 入射 → LCP 分量
#ER_L = (ex_L - 1j * ey_L) / 2  # LCP 入射 → RCP 分量
# RCP 入射
EL_R = (ex_R + 1j * ey_R) / (2)  # R CP 入射 → LCP 分量
ER_R = (ex_R - 1j * ey_R) / (2)  # RCP 入射 → RCP 分量

# LCP 入射的强度
#intensity_LL = np.abs(EL_L)**2  # LCP → LCP
#intensity_LR = np.abs(ER_L)**2  # LCP → RCP
# RCP 入射的强度
intensity_RL = np.abs(EL_R)**2  # RCP → LCP
intensity_RR = np.abs(ER_R)**2  # RCP → RCP


plt.figure(1)
#plt.plot(f_L, intensity_LL, label="LCP → LCP", marker='o', markersize=2, linestyle='None')
#plt.plot(f_L, intensity_LR, label="LCP → RCP", marker='o', markersize=2, linestyle='None')
plt.plot(f_R, intensity_RL, label="RCP → LCP", linewidth=2, linestyle="-.")
plt.plot(f_R, intensity_RR, label="RCP → RCP", linewidth=2, linestyle=":")
plt.xlabel("f(tHz)", fontsize=14)
plt.ylabel("Transmittance", fontsize=14)
plt.title("Circular Polarization Transmittance", fontsize=16)
plt.grid(True)
plt.legend(fontsize=12)
# RCP 入射分量相位
phase_EL_R = np.angle(EL_R)
phase_ER_R = np.angle(ER_R)

# ———————— 计算相位差 ————————
# RCP 入射时，R→L 与 R→R 之间的相位差
delta_phase_R = (phase_EL_R - phase_ER_R) * 180 / np.pi
delta_phase_R = (delta_phase_R + 180) % 360 - 180

# ———————— 绘制相位差随频率的变化 ————————
plt.figure(2)
plt.plot(f_R, delta_phase_R, label="Δφ (RCP 入射)", linewidth=2, linestyle="--")
plt.xlabel("频率 f (tHz)", fontsize=14)
plt.ylabel("相位差 Δφ (rad)", fontsize=14)
plt.title("Circular Polarization Phase Difference", fontsize=16)
plt.legend(fontsize=12)
plt.show()