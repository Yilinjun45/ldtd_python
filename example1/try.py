import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 定义常量（与Mathematica一致）
k1 = 0.2
k2 = 0.3
X1 = 1
X2 = 2
H1 = 1
H2 = 5
L1 = 2
L2 = 2
m = 2
g = 9.81
vx0 = 0.01
vy0 = 0.01


# 定义弹簧力函数
def N1(x, y):
    return k1 * (np.sqrt((x - X1) ** 2 + (y - H1) ** 2) - L1)


def N2(x, y):
    return k2 * (np.sqrt((x - X2) ** 2 + (y - H2) ** 2) - L2)


# 定义微分方程组
def equations(t, state):
    x, y, vx, vy = state
    dx = x - X1
    dy = y - H1
    dist1 = np.sqrt(dx ** 2 + dy ** 2)

    dx2 = x - X2
    dy2 = y - H2
    dist2 = np.sqrt(dx2 ** 2 + dy2 ** 2)

    # 计算加速度 (x方向和y方向)
    ax = (N1(x, y) * np.abs(X1 - x) / dist1 + N2(x, y) * np.abs(X2 - x) / dist2) / m
    ay = (N1(x, y) * np.abs(H1 - y) / dist1 + N2(x, y) * np.abs(H2 - y) / dist2) / m - g

    return [vx, vy, ax, ay]


# 初始状态 [x0, y0, vx0, vy0]
initial_state = [-5, 4, vx0, vy0]

# 时间范围 (0到2秒)
t_span = (0, 2)
t_eval = np.linspace(0, 2, 1000)

# 求解微分方程
solution = solve_ivp(equations, t_span, initial_state, t_eval=t_eval, method='LSODA')

# 提取结果
x_sol = solution.y[0]
y_sol = solution.y[1]
t_sol = solution.t

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(t_sol, x_sol, label='x(t)')
plt.plot(t_sol, y_sol, label='y(t)')
plt.xlabel('Time (s)')
plt.ylabel('Position')
plt.title('Spring-Mass System Motion')
plt.legend()
plt.grid(True)
plt.show()