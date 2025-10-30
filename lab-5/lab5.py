import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.linalg import eig

print("=" * 50)
print("COMPETITION MODEL")
print("=" * 50)

a, b, c, d = 1.0, 0.8, 1.0, 0.6


def f_competition(t, z):
    x, y = z
    return [x * (a - b * y), y * (-c + d * x)]

def jacobian_competition(x, y):
    return np.array([[a - b * y, -b * x],
                     [d * y, -c + d * x]])

points = [(0, 0), (a / b, 0), (0, c / d), (c / d, a / b)]
for i, (x, y) in enumerate(points, 1):
    J = jacobian_competition(x, y)
    eigenvalues = eig(J)[0]
    print(f"\nP{i} ({x:.3f}, {y:.3f}):")
    print(f"Wartosci: {eigenvalues[0]:.3f}, {eigenvalues[1]:.3f}")
    if all(np.real(ev) < 0 for ev in eigenvalues):
        print(f"STABILNE")
    else:
        print(f"NIESTABILNE")

fig, ax = plt.subplots(figsize=(10, 8))

for x0 in np.linspace(0.1, 2.0, 7):
    for y0 in np.linspace(0.1, 2.0, 7):
        sol = solve_ivp(f_competition, [0, 50], [x0, y0], max_step=0.1)
        ax.plot(sol.y[0], sol.y[1], alpha=0.6, linewidth=1)

for i, (x, y) in enumerate(points, 1):
    ax.plot(x, y, 'ro', markersize=10, label=f'P{i}' if i <= 4 else '')

ax.set_xlabel('Populacja x', fontsize=12)
ax.set_ylabel('Populacja y', fontsize=12)
ax.set_title('Lotka-Volterra Competition - portret fazowy', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

print("\n" + "=" * 50)
print("MODEL MUTUALNY")
print("=" * 50)

a_mut, b_mut, c_mut, d_mut = 1.0, 0.5, 1.0, 0.5

def f_mutualism(t, z):
    x, y = z
    return [x * (a_mut + b_mut * y), y * (c_mut + d_mut * x)]

def jacobian_mutualism(x, y):
    return np.array([[a_mut + b_mut * y, b_mut * x],
                     [d_mut * y, c_mut + d_mut * x]])


J = jacobian_mutualism(0, 0)
eigenvalues = eig(J)[0]
print(f"Wartosci wlasne: {eigenvalues[0]:.3f}, {eigenvalues[1]:.3f}")

fig, ax = plt.subplots(figsize=(10, 8))

for x0 in np.linspace(0.1, 1.0, 6):
    for y0 in np.linspace(0.1, 1.0, 6):
        sol = solve_ivp(f_mutualism, [0, 20], [x0, y0], max_step=0.1)
        ax.plot(sol.y[0], sol.y[1], alpha=0.6, linewidth=1)

ax.plot(0, 0, 'ro', markersize=10, label='P1 (0,0)')
ax.set_xlabel('Populacja X', fontsize=12)
ax.set_ylabel('Populacja Y', fontsize=12)
ax.set_title('Lotka-Volterra Mutualism - Portret fazowy', fontsize=14)
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

cases = [
    ("Bez koegzystencji", 0.3, 2.0),  # x < c/d
    ("Marginalna koegzystencja", 1.7, 1.2),
    ("W kierunku równowagi", 2.0, 0.8)  # x > c/d, y < a/b
]

for ax, (title, x0, y0) in zip(axes, cases):
    sol = solve_ivp(f_competition, [0, 100], [x0, y0], max_step=0.1)
    ax.plot(sol.y[0], sol.y[1], 'b-', linewidth=2, label='Trajektoria')
    ax.plot(x0, y0, 'go', markersize=10, label='Start')

    ax.axvline(c / d, color='r', linestyle='--', alpha=0.5, label=f'x=c/d={c / d:.2f}')
    ax.axhline(a / b, color='g', linestyle='--', alpha=0.5, label=f'y=a/b={a / b:.2f}')
    ax.fill_between([c / d, ax.get_xlim()[1]], 0, a / b, alpha=0.2, color='yellow', label='Region koegzystencji')

    for px, py in points:
        ax.plot(px, py, 'ro', markersize=8)

    ax.set_xlabel('Populacja X', fontsize=12)
    ax.set_ylabel('Populacja Y', fontsize=12)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

for ax, (title, x0, y0) in zip(axes, cases):
    sol = solve_ivp(f_competition, [0, 100], [x0, y0], max_step=0.1, dense_output=True)
    t = np.linspace(0, 100, 1000)
    y = sol.sol(t)

    ax.plot(t, y[0], label='Populacja x', linewidth=2)
    ax.plot(t, y[1], label='Populacja y', linewidth=2)
    ax.set_xlabel('Czas')
    ax.set_ylabel('Gęstość populacji')
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()

plt.tight_layout()
plt.show()

print("\n" + "=" * 50)
print("CONTROL QUESTIONS")
print("=" * 50)

print("\n1. Real part of eigenvalue interpretation:")
print("   - Real part < 0: trajectories converge to stationary point (stable)")
print("   - Real part > 0: trajectories diverge from stationary point (unstable)")
print("   - Mixed signs: saddle point (stable in one direction, unstable in another)")
print("   - Imaginary part indicates oscillations around the point")

print("\n2. Why competition leads to extinction:")
print("   - Both populations harm each other (negative interaction terms)")
print("   - If one population becomes larger, it suppresses the other")
print("   - The system often has stable points on axes (x,0) or (0,y)")
print("   - Starting conditions determine which population survives")
print("   - Interior equilibrium (if exists) is often unstable saddle point")
print("   - Winner depends on initial conditions and parameter ratios")

print("\nAnalysis complete! Check generated PNG files for visualizations.")