import numpy as np
import lumapi
import matplotlib.pyplot as plt

# 打开FDTD session
fdtd = lumapi.FDTD("C:\\Users\\18454\\Desktop\\example1.fsp")

# 参数定义
theta = np.linspace(0, 60, 7)  # 角度 sweep
A = None  # 先不初始化矩阵，等第一次读数据确定尺寸

# 常量
c = 3e8  # 光速 (m/s)

# 主循环
for i, angle in enumerate(theta):
    fdtd.switchtolayout()

    fdtd.setnamed('source', 'plane wave type', 'BFAST')  # 开启 BFAST
    fdtd.setnamed('source', 'angle theta', angle)

    fdtd.run()

    try:
        # 读取数据
        T = -fdtd.transmission('T')  # 注意负号
        R = fdtd.transmission('R')

        # 初始化A矩阵
        if A is None:
            num_points = len(R)
            A = np.zeros((len(theta), num_points))

        # 计算吸收率 A
        A[i, :] = 1 - R - T

        print(f"Finished theta {angle:.2f} degrees ({i + 1}/{len(theta)})")

    except Exception as e:
        print(f"Error at theta={angle}: {e}")

# 还原源设置
fdtd.switchtolayout()
fdtd.setnamed('source1', 'plane wave type', 'Bloch/periodic')
fdtd.setnamed('source1', 'angle theta', 0)

# 取频率数据，换成波长（um）
f = fdtd.getdata('R', 'f')  # 频率，单位是 Hz
wavelength_um = c * 1e6 / f  # μm单位

# 创建meshgrid，便于后续保存数据
theta_grid, wavelength_grid = np.meshgrid(theta, wavelength_um, indexing='ij')  # (theta,wavelength)结构

# --- 绘制吸收图 ---
plt.figure(figsize=(10, 7))
plt.imshow(
    A.T,  # 注意转置
    extent=[theta.min(), theta.max(), wavelength_um.max(), wavelength_um.min()],
    aspect='auto',
    cmap='inferno'
)
plt.colorbar(label='Absorption A')
plt.xlabel('Incidence angle θ (degrees)')
plt.ylabel('Wavelength (μm)')
plt.title('Absorption Map (A)')
plt.tight_layout()
plt.show()
