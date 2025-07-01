# a0的改变与李普雅诺夫指数
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# 参数设置
g = 9.81   # 重力加速度 (m/s^2)
l = 0.25   # 摆长 (m)
omega = 10  # 固定的枢轴振荡角频率 (rad/s)
m = 0.020  # 摆锤质量 (kg)
b = 0.001  # 阻尼系数 (kg/s)

# 初始条件
theta0 = 1.5  # 初始角度 (rad)
theta_dot0 = 0.0  # 初始角速度 (rad/s)
y0 = np.array([theta0, theta_dot0])

# 时间范围
t_start = 0
t_end = 50  # 增大时间范围，观察李雅普诺夫指数的收敛
num_points = 200000
t_eval = np.linspace(t_start, t_end, num_points)

# 微分方程
def diff_eq(t, y, a0):
    theta, theta_dot = y
    theta_double_dot = -((g / l + a0 * omega ** 2 / l * np.cos(omega * t)) * np.sin(theta) + (b / m) * theta_dot)
    return np.array([theta_dot, theta_double_dot])

# 定义雅可比矩阵
def jacobian(t, y, a0):
    theta, theta_dot = y
    dfdtheta = -((g / l + a0 * omega ** 2 / l * np.cos(omega * t)) * np.cos(theta))
    dfdtheta_dot = - (b / m)
    J = np.array([[0, 1],
                  [dfdtheta, dfdtheta_dot]])
    return J

# 初始扰动向量（单位向量）
delta0 = np.array([1e-8, 0])
delta0 = delta0 / np.linalg.norm(delta0)

# 枢轴振幅列表
a0_values = np.linspace(0.1, 1.0, 10)

final_lyapunov_exponents = []

for a0 in a0_values:
    # 初始化李雅普诺夫指数
    lyapunov_exp = 0.0
    sum_log_norm = 0.0

    # 初始化状态和扰动
    y = y0.copy()
    delta = delta0.copy()

    # 时间步长
    dt = t_eval[1] - t_eval[0]

    # 迭代计算
    for i in range(len(t_eval) - 1):
        t_span = [t_eval[i], t_eval[i + 1]]
        t = t_eval[i]

        # 使用Runge-Kutta方法积分主方程
        sol = solve_ivp(diff_eq, t_span, y, args=(a0,), method='RK45', atol=1e-9, rtol=1e-9)
        y = sol.y[:, -1]

        # 计算雅可比矩阵
        J = jacobian(t, y, a0)

        # 使用线性近似更新扰动向量
        delta = delta + dt * (J @ delta)

        # 计算扰动向量的范数
        norm_delta = np.linalg.norm(delta)

        # 正则化扰动向量
        delta = delta / norm_delta

        # 累加对数范数
        sum_log_norm += np.log(norm_delta)

    final_lyapunov_exponent = sum_log_norm / (t_end - t_start)
    final_lyapunov_exponents.append(final_lyapunov_exponent)

    print(f"枢轴振幅 a0 = {a0:.2f} m 时，估计的李雅普诺夫指数 λ: {final_lyapunov_exponent}")

# 李雅普诺夫指数vs角频率
plt.figure(figsize=(12, 8))
plt.plot(a0_values, final_lyapunov_exponents, marker='o', linestyle='-')

plt.xlabel('Amplitude a0 (m)', fontsize=14)
plt.ylabel('Lyapunov Exponent λ', fontsize=14)

plt.title('Variation of Lyapunov Exponent with Amplitude a0', fontsize=16)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)


plt.show()
