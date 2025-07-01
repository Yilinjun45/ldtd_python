import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz


def calculate_displacement(time, acceleration, initial_velocity=0, initial_displacement=0):
    t = np.asarray(time)
    a = np.asarray(acceleration)
    velocity = cumtrapz(a, t, initial=0) + initial_velocity
    displacement = cumtrapz(velocity, t, initial=0) + initial_displacement
    return t, velocity, displacement


if __name__ == "__main__":
    input_file = ‘D:\桌面\cupt\14\2.xlsx’  # 修改为你的Excel文件名
    try:
        df = pd.read_excel(input_file)

    time = df.iloc[:, 0].values
    acceleration = df.iloc[:, 1].values
    t, velocity, displacement = calculate_displacement(time, acceleration)
    result_df = pd.DataFrame({
        '时间(s)': t,
        '加速度(m/s²)': acceleration,
        '速度(m/s)': velocity,
        '位移(m)': displacement
    })

    # 4. 保存结果到新Excel文件
    output_file = "displacement_results.xlsx"

    plt.figure(figsize=(12, 10))

    plt.subplot(3, 1, 1)
    plt.plot(t, acceleration, 'r-o', markersize=4, linewidth=1.5)
    plt.title('加速度-时间曲线', fontsize=12)
    plt.ylabel('加速度 (m/s²)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 速度图
    plt.subplot(3, 1, 2)
    plt.plot(t, velocity, 'b-o', markersize=4, linewidth=1.5)
    plt.title('速度-时间曲线', fontsize=12)
    plt.ylabel('速度 (m/s)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 位移图
    plt.subplot(3, 1, 3)
    plt.plot(t, displacement, 'g-o', markersize=4, linewidth=1.5)
    plt.title('位移-时间曲线', fontsize=12)
    plt.xlabel('时间 (s)', fontsize=10)
    plt.ylabel('位移 (m)', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout(pad=3.0)
