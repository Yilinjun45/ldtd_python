import lumapi
import numpy as np
import matplotlib.pyplot as plt

c = 3e8  # 光速，单位 m/s

# 启动 FDTD 会话并载入项目
fdtd = lumapi.FDTD(r"D:\桌面\大创\FDTD_trying\example2 - 副本.fsp")


def run_fdtd(phase2: float):
    fdtd.switchtolayout()
    fdtd.setnamed("source_1", "polarization angle", 0)
    fdtd.setnamed("source_1", "phase", 0)
    fdtd.setnamed("source_2", "polarization angle", 90)
    fdtd.setnamed("source_2", "phase", phase2)
    fdtd.run()

    # 获取数据
    ex = fdtd.getdata("T", "Ex")
    ey = fdtd.getdata("T", "Ey")
    freq = fdtd.getdata("T", "f").squeeze()
    t_lcp = fdtd.transmission('T').squeeze()

    return ex, ey, freq, t_lcp


# 运行 LCP 入射（phase2 = 90）
ex_L, ey_L, freq, t_lcp = run_fdtd(90)

# 计算圆偏振分量（保留空间维度）
EL_L = (ex_L + 1j * ey_L) / np.sqrt(2)  # LCP 分量
ER_L = (ex_L - 1j * ey_L) / np.sqrt(2)  # RCP 分量

# 计算强度
intensity_LL = np.abs(EL_L) ** 2
intensity_LR = np.abs(ER_L) ** 2
intensity_total = np.abs(ex_L) ** 2 + np.abs(ey_L) ** 2

# 空间平均
if ex_L.ndim > 1:
    spatial_axes = tuple(range(1, ex_L.ndim))
    T_LLCP = np.mean(intensity_LL, axis=spatial_axes)
    T_LRCP = np.mean(intensity_LR, axis=spatial_axes)
    T_total = np.mean(intensity_total, axis=spatial_axes)
else:
    T_LLCP = intensity_LL
    T_LRCP = intensity_LR
    T_total = intensity_total

# 确保频率维度匹配
min_len = min(len(T_LLCP), len(freq), len(t_lcp))
T_LLCP = T_LLCP[:min_len]
T_LRCP = T_LRCP[:min_len]
T_total = T_total[:min_len]
freq = freq[:min_len]
t_lcp = t_lcp[:min_len]

# 计算缩放因子以匹配 T_total 和 t_lcp
scaling = t_lcp / T_total

# 缩放 T_LLCP 和 T_LRCP
T_LLCP_scaled = T_LLCP * scaling
T_LRCP_scaled = T_LRCP * scaling

# 转换频率为波长并升序排序
wavelength = c / freq * 1e9  # 单位：nm
sort_idx = np.argsort(wavelength)
wl = wavelength[sort_idx]
T_LLCP_scaled = T_LLCP_scaled[sort_idx]
T_LRCP_scaled = T_LRCP_scaled[sort_idx]
T_total_scaled = T_total * scaling[sort_idx]  # 应等于 t_lcp
t_lcp = t_lcp[sort_idx]

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(wl, T_LLCP_scaled, label="LCP → LCP", marker='s', linestyle='None', color='g')
plt.plot(wl, T_LRCP_scaled, label="LCP → RCP", marker='o', linestyle='None', color='b')
plt.plot(wl, T_total_scaled, label="Total Transmission (scaled)", marker='x', linestyle='None', color='r')
plt.plot(wl, t_lcp, label="Total Transmission (Lumerical)", marker='.', linestyle='None', color='purple')
plt.xlabel("Wavelength (nm)", fontsize=14)
plt.ylabel("Transmittance", fontsize=14)
plt.title("Circular Polarization Transmittance", fontsize=16)
plt.grid(True)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()