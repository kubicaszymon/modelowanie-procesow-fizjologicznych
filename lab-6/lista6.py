import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

r, K, k, alpha, P0, delta = 0.71, 1e6, 1e-7, 1.2, 1e4, 0.2

def f(t: float, state: tuple[float, float], mode: str = "r") -> tuple[float, float]:
    """""
    Function calculating dP and dI based on previous state and current time in simulation. Constants are passed as global variables
    Args:
    t(float): time in simulation
    state(tuple[float, float]): tuple containing current values of P and I
    Returns:
    tuple[float, float]: dP and dI at given time step
    """
    P, I = state
    r_local, k_local = r, k

    if 12 <= t <= 72:
        if mode == "r":
            r_local *= 0.0001
        elif mode == "k":
            k_local *= 500000

    dP = r_local * P * (1 - P / K) - k_local * I * P
    dI = ((alpha * P) / (P + P0)) - delta * I

    return [dP, dI]

P0_init = 1e3
I0_init = 0.1
initial_state = [P0_init, I0_init]

t_span = (0, 144)
t_eval = np.linspace(t_span[0], t_span[1], 1000) # punkty do ewaluacji

solution = solve_ivp(lambda t, y: f(t, y, mode="none"), t_span, initial_state, t_eval=t_eval)
solution_r = solve_ivp(lambda t, y: f(t, y, mode="r"), t_span, initial_state, t_eval=t_eval)
solution_k = solve_ivp(lambda t, y: f(t, y, mode="k"), t_span, initial_state, t_eval=t_eval)

fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)


def plot_solution(ax, sol):
    ax.plot(sol.t, sol.y[0], label=f'P(t)')
    ax.plot(sol.t, sol.y[1], label=f'I(t)')
    ax.axvspan(12,72, alpha=0.1, label='dzialanie leku (12-72)')
    ax.set_ylabel('Value')
    ax.grid(True)
    ax.legend()

plot_solution(axes[0], solution)
axes[0].set_title("Bez leku")

plot_solution(axes[1], solution_r)
axes[1].set_title("Lek hamuje wirusa")

plot_solution(axes[2], solution_k)
axes[2].set_title("Lek pomaga zwalczac wirusa")

axes[2].set_xlabel("Czas [godziny]")

plt.suptitle("Porownanie: bez leku, z lekiem dla r oraz k")
plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()

def eradication_time(sol, cryterion=1.0):
    index_below_criterion = np.where(sol.y[0] < cryterion)[0]

    if len(index_below_criterion) > 0:
        idx = index_below_criterion[0]
        return sol.y[idx]
    else:
        return np.nan

time_without = eradication_time(solution)
time_medicine_r = eradication_time(solution_r)
time_medicine_k = eradication_time(solution_k)

print(f"Bez leku: {time_without:.2f} godzin")
print(f"Lek 'r' (r_local *= 0.0001): {time_medicine_r:.2f} godzin")
print(f"Lek 'k' (k_local *= 500000): {time_medicine_k:.2f} godzin")