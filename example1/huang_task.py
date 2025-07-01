import lumapi
import numpy as np
import matplotlib.pyplot as plt
from openpyxl.workbook import Workbook

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

c = 3e8  # 光速，单位 m/s

# ─────────────────────────────────────────────
# 1. 启动 FDTD 会话并载入项目
# ─────────────────────────────────────────────
fdtd = lumapi.FDTD(r"D:\桌面\大创\hxr学姐复现任务\try_hxr.fsp")
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

ex_L, ey_L, f_L = run_fdtd(90)   # LCP 入射
ex_R, ey_R, f_R = run_fdtd(-90)  # RCP 入射

# LCP 入射
ER_L = (ex_L + 1j * ey_L) / 2  # LCP 入射 → RCP 分量
EL_L = (ex_L - 1j * ey_L) / 2  # LCP 入射 → LCP 分量
# RCP 入射
ER_R = (ex_R + 1j * ey_R) / 2  # RCP 入射 → RCP 分量
EL_R = (ex_R - 1j * ey_R) / 2  # RCP 入射 → LCP 分量

# LCP 入射的强度
#intensity_LR = np.abs(ER_L)**2  # LCP → RCP
intensity_LL = np.abs(EL_L)**2  # LCP → LCP
# RCP 入射的强度
intensity_RR = np.abs(ER_R)**2  # RCP → RCP
#intensity_RL = np.abs(EL_R)**2  # RCP → LCP


plt.figure(1)
plt.plot(f_L, intensity_LL, label="LCP → LCP", marker='o', markersize=2, linestyle='None')
#plt.plot(f_L, intensity_LR, label="LCP → RCP", marker='o', markersize=2, linestyle='None')
plt.plot(f_R, intensity_RR, label="RCP → RCP", linewidth=2, linestyle="-.")
#plt.plot(f_R, intensity_RL, label="RCP → LCP", linewidth=2, linestyle=":")
plt.xlabel("f(tHz)", fontsize=14)
plt.ylabel("Transmittance", fontsize=14)
plt.title("Circular Polarization Transmittance", fontsize=16)
plt.grid(True)
plt.legend(fontsize=12)
# RCP 入射分量相位
phase_EL_L = np.angle(ex_L)
phase_ER_L = np.angle(ex_R)

# ———————— 计算相位差 ————————
# RCP 入射时，L→L 与 R→R 之间的相位差
delta_phase_R = (phase_EL_L - phase_ER_L) * 180 / np.pi
delta_phase_R = (delta_phase_R + 180) % 360 - 180

# ———————— 绘制相位差随频率的变化 ————————
plt.figure(2)
plt.plot(f_R, delta_phase_R, label="Δφ ", linewidth=2, linestyle="--")
plt.xlabel("频率 f (tHz)", fontsize=14)
plt.ylabel("相位差 Δφ (°)", fontsize=14)
plt.title("Circular Polarization Phase Difference", fontsize=16)
plt.legend(fontsize=12)

# 计算相位差
tanphi=abs(np.real(ex_L)/np.real(ex_R))
phi=np.arctan(tanphi) * 180 / np.pi
plt.figure(3)
plt.plot(f_R, phi, label="Phi", linewidth=2)
plt.xlabel("频率 f (tHz)", fontsize=14)
plt.ylabel("相位差 ", fontsize=14)
plt.show()
# 创建 DataFrame（列包含频率、ER_R 和 EL_R 的幅值与相位）
wb = Workbook()
ws = wb.active

# 添加标题行
headers = [
    '频率 (tHz)',
    'ER_R 幅值',
    'ER_R 相位(rad)',
    'EL_l 幅值',
    'EL_l 相位(rad)',
    'EL',
    'ER',
    '相位'
]
ws.append(headers)

# 填充数据
for i in range(len(f_R)):
    row = [
        f_R[i],
        np.abs(ER_R)[i],
        np.angle(ER_R)[i],
        np.abs(EL_L)[i],
        np.angle(EL_L)[i],
        intensity_LL[i],
        intensity_RR[i],
        delta_phase_R[i]
    ]
    ws.append(row)

# 保存文件
excel_path = r'D:\桌面\大创\hxr学姐复现任务\新建 XLSX 工作表.xlsx'
wb.save(excel_path)