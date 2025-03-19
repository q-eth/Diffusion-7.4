import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import maxwell

# Параметры
N = 500  # Количество частиц
steps = 200  # Количество шагов
bins_v = 25

delta = 1  # Размер шага
x = np.zeros((N, steps))
y = np.zeros((N, steps))

# Генерация случайного блуждания
for t in range(1, steps):
    dx, dy = np.random.randn(N), np.random.randn(N)
    x[:, t] = x[:, t - 1] + dx * delta
    y[:, t] = y[:, t - 1] + dy * delta

# Создание фигуры для анимации
fig, (ax_walk, ax_hist) = plt.subplots(1, 2, figsize=(12, 6))
ax_walk.set_xlim(-50, 50)
ax_walk.set_ylim(-50, 50)
ax_walk.set_title("Случайное блуждание частиц")
ax_hist.set_xlim(0, 50)
ax_hist.set_ylim(0, N // 5)
ax_hist.set_title("Гистограмма расстояний")

# Объекты для анимации
particles, = ax_walk.plot([], [], 'ko', markersize=3)
hist_values, _, _ = ax_hist.hist([], bins=20, range=(0, 50), alpha=0.6, color='b')

def init():
    particles.set_data([], [])
    return particles,

def update(frame):
    # Обновление позиций частиц
    particles.set_data(x[:, frame], y[:, frame])
    
    # Обновление гистограммы расстояний
    distances = np.sqrt(x[:, frame]**2 + y[:, frame]**2)
    ax_hist.cla()
    ax_hist.hist(distances, bins=bins_v, range=(0, 50), alpha=0.6, color='#777777', label="Эмпирические данные")
    
    # Теоретическая кривая Максвелла-Больцмана
    r = np.linspace(0, 50, 100)
    sigma = np.sqrt(frame)  # Оценка дисперсии
    theoretical_pdf = (r / sigma**2) * np.exp(-r**2 / (2 * sigma**2))
    ax_hist.plot(r, theoretical_pdf * N * 2, 'r-', label="Теоретическое распределение")
    
    ax_hist.set_xlim(0, 50)
    ax_hist.set_ylim(0, 500)
    ax_hist.set_title("Гистограмма расстояний")
    ax_hist.legend()
    ax_hist.set_ylim(0, 150)
    
    return particles,

ani = animation.FuncAnimation(fig, update, frames=steps, init_func=init, blit=False, interval=10)
plt.show()