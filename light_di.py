import lumapi
import matplotlib.pyplot as plt
import numpy as np

c = 3e8
X = []
T_values_LCP = []  # 左旋偏振光透射率
T_values_RCP = []  # 右旋偏振光透射率
f_values = []

# 初始化FDTD仿真
fdtd = lumapi.FDTD("D:\桌面\大创\FDTD_trying\example2.fsp")
fdtd.switchtolayout()  # 切换到布局模式

# 定义光源参数
x_span = 3e-5
y_span = 3e-5
z_position = -705e-9

fdtd.setnamed('source_1', 'polarization angle', 0)
fdtd.setnamed('source_1', 'phase', 0)

fdtd.setnamed('source_2', 'polarization angle', 90)
fdtd.setnamed('source_2', 'phase', 90)

fdtd.run()

# 获取数据
f_i = fdtd.getdata('T', 'f')  # 获取频率数据

# 获取左旋偏振光透射率
T_LCP = fdtd.transmission('T')  # 左旋偏振光透射率（注意符号问题）
T_values_LCP = np.abs(T_LCP)  # 取绝对值避免负值

# 获取右旋偏振光透射率
# 修改相位和偏振角度为右旋偏振光的设置
fdtd.switchtolayout()  # 确保再次切换到布局模式
fdtd.setnamed('source_1', 'polarization angle', 0)
fdtd.setnamed('source_1', 'phase', 0)
fdtd.setnamed('source_2', 'polarization angle', 90)
fdtd.setnamed('source_2', 'phase', -90)

fdtd.run()  # 重新运行仿真
T_RCP = fdtd.transmission('T')  # 右旋偏振光透射率
T_values_RCP = np.abs(T_RCP)  # 取绝对值避免负值

# 计算CD = 右旋透射率 - 左旋透射率
CD_values = T_values_RCP - T_values_LCP

# 处理数据
wavelength_values = c / f_i  # 计算波长

# 绘图
plt.figure(figsize=(8, 6))

# 绘制左旋偏振光透射率
plt.plot(wavelength_values * 1e9, T_values_LCP, label='LCP Transmission', marker='s', linestyle='-.', color='g')

# 绘制右旋偏振光透射率
plt.plot(wavelength_values * 1e9, T_values_RCP, label='RCP Transmission', marker='o', linestyle='-', color='b')

# 绘制CD值
plt.plot(wavelength_values * 1e9, CD_values, label='Circular Dichroism (CD)', marker='^', linestyle='--', color='r')

# 设置图形标签与标题
plt.xlabel('Wavelength (nm)')
plt.ylabel('Transmission / CD')
plt.title('Transmission Spectrum and Circular Dichroism (CD)')
plt.grid(True)
plt.legend()

# 显示图形
plt.show()
