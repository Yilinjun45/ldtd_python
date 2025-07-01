import matplotlib.pyplot as plt
import numpy as np
import lumapi

c = 3e8
X = []
R_values = []
T_values = []
A_values = []
f_values = []

# 创建 FDTD 会话
fdtd = lumapi.FDTD(filename='C:\\Users\\18454\\Desktop\1\example1.fsp')

# 运行仿真并获取数据
for i in range(1, 10, ):
    fdtd.switchtolayout()
    fdtd.setnamed("::model::dielectric", "z", -(0.5 * i) * 1e-9)
    fdtd.setnamed("::model::dielectric", "z span", i * 1e-9)

    # 修改 gold_bottom 结构的 z 位置
    fdtd.setnamed("::model::gold_bottom", "z", -(i + 25) * 1e-9)

    fdtd.run()

    # 读取数据
    f_i = fdtd.getdata('R', 'f')  # 获取频率数据
    R_i = fdtd.transmission('R')  # 获取反射率数据
    T_i = -fdtd.transmission('T')  # 获取透射率数据
    A_i = 1 - R_i - T_i  # 计算吸收率

    # 存储所有频率对应的波长、吸收率、反射率、透射率
    for j in range(len(f_i)):
        f_values.append(f_i[j])  # 频率
        A_values.append(A_i[j])  # 吸收率
        R_values.append(R_i[j])  # 反射率
        T_values.append(T_i[j])  # 透射率

# 计算波长
wavelength_values = [c / f for f in f_values]

# 绘制波长与吸收率、反射率、透射率的关系图
plt.figure(figsize=(8, 6))
plt.plot(wavelength_values, A_values, label='Absorption Rate', marker='o', linestyle='-', color='b')
plt.plot(wavelength_values, R_values, label='Reflection Rate', marker='x', linestyle='--', color='r')
plt.plot(wavelength_values, T_values, label='Transmission Rate', marker='s', linestyle='-.', color='g')

# 设置图表标题和标签
plt.title('Wavelength vs Absorption, Reflection and Transmission Rates')
plt.xlabel('Wavelength (m)')
plt.ylabel('Rate')

# 显示图例
plt.legend()

# 显示图像
plt.grid(True)
plt.show()
