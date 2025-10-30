from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt

def simulate(L, k_on=1.0, k_off=0.2, k_cat=0.5, kdegK=0.3, kact=0.8, kdegE=0.2, t_max=600):
    def f(t, y):
        R, K, E = y
        dR = k_on * L * (1 - R) - k_off * R
        dK = k_cat * R * (1 - K) - kdegK * K
        dE = kact * K * (1 - E) - kdegE * E
        return [dR, dK, dE]

    sol = solve_ivp(f, [0, t_max], [0, 0, 0], max_step=0.1, dense_output=True)
    t = np.linspace(0, t_max, int(t_max * 10))
    R, K, E = sol.sol(t)
    return t, R, K, E

def calculate_t_half(t, E):
    """Oblicza czas osiągnięcia E* = 0.5"""
    idx = np.where(E >= 0.5)[0]
    if len(idx) > 0:
        return t[idx[0]]
    else:
        return 999.9


def find_optimal_params(L, target_t_half=120, tolerance=5):
    """Znajduje optymalne parametry dla zadanego t_1/2"""
    best_params = None
    best_error = float('inf')

    for k_cat in np.linspace(0.01, 0.15, 30):
        for k_off in np.linspace(0.2, 1.0, 20):
            t, R, K, E = simulate(L, k_cat=k_cat, k_off=k_off, t_max=250)
            t_h = calculate_t_half(t, E)

            if t_h < 999:
                error = abs(t_h - target_t_half)
                if error < best_error:
                    best_error = error
                    best_params = {'k_cat': k_cat, 'k_off': k_off, 't_half': t_h}

                    if error < tolerance:
                        print(f"Znaleziono: k_cat={k_cat:.4f}, k_off={k_off:.3f}, t₁/₂={t_h:.1f}s")
                        return best_params

    if best_params and best_error < 20:
        k_cat_center = best_params['k_cat']
        k_off_center = best_params['k_off']

        for k_cat in np.linspace(max(0.01, k_cat_center - 0.02), k_cat_center + 0.02, 20):
            for k_off in np.linspace(max(0.2, k_off_center - 0.2), min(1.0, k_off_center + 0.2), 15):
                t, R, K, E = simulate(L, k_cat=k_cat, k_off=k_off, t_max=250)
                t_h = calculate_t_half(t, E)

                if t_h < 999:
                    error = abs(t_h - target_t_half)
                    if error < best_error:
                        best_error = error
                        best_params = {'k_cat': k_cat, 'k_off': k_off, 't_half': t_h}

    if best_params:
        print(
            f"Najlepsze: k_cat={best_params['k_cat']:.4f}, k_off={best_params['k_off']:.3f}, t₁/₂={best_params['t_half']:.1f}s (błąd: {best_error:.1f}s)")

    return best_params


print("ZADANIE 1")
print("=" * 50)

t, R, K, E = simulate(L=5)

plt.figure(figsize=(10, 6))
plt.plot(t, R, label='R* (Receptor)', linewidth=2)
plt.plot(t, K, label='K* (Kinaza)', linewidth=2)
plt.plot(t, E, label='E* (Efektor)', linewidth=2)
plt.xlabel('Czas [s]', fontsize=12)
plt.ylabel('Frakcja aktywna', fontsize=12)
plt.title('Aktywacja skladowych szlaku sygnalowego (L=5)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
print()

print("ZADANIE 2")
print("=" * 50)

plt.figure(figsize=(10, 6))

concentrations = [1, 5, 10]
colors = ['blue', 'green', 'red']

for L, color in zip(concentrations, colors):
    t, R, K, E = simulate(L)
    t_half = calculate_t_half(t, E)

    plt.plot(t, E, label=f'L={L} (t1/2={t_half:.1f}s)',
             linewidth=2, color=color)

    if t_half < 999:
        plt.plot(t_half, 0.5, 'o', color=color, markersize=8)

    print(f"L = {L}: t₁/₂ = {t_half:.2f} s")

plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3)
plt.xlabel('Czas [s]', fontsize=12)
plt.ylabel('E* (Frakcja aktywna efektora)', fontsize=12)
plt.title('Wplyw stężenia ligandu na aktywacje efektora', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print()

print("ZADANIE 3")
print("=" * 50)

plt.figure(figsize=(10, 6))

L = 10

# Bez inhibitora
t, R, K, E = simulate(L, k_cat=0.5)
t_half_normal = calculate_t_half(t, E)
plt.plot(t, E, label=f'Bez inhibitora (k_cat=0.5, t1/2={t_half_normal:.1f}s)',
         linewidth=2, color='blue')

# Z inhibitorem
t, R, K, E = simulate(L, k_cat=0.25)
t_half_inhibited = calculate_t_half(t, E)
plt.plot(t, E, label=f'Z inhibitorem (k_cat=0.25, t1/2={t_half_inhibited:.1f}s)',
         linewidth=2, color='red', linestyle='--')

plt.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, label='E* = 0.5')
plt.xlabel('Czas [s]', fontsize=12)
plt.ylabel('E* (Frakcja aktywna efektora)', fontsize=12)
plt.title(f'Dzialanie inhibitora na aktywacje efektora (L={L})', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"Bez inhibitora: t1/2 = {t_half_normal:.2f} s")
print(f"Z inhibitorem: t1/2 = {t_half_inhibited:.2f} s")
print(f"Wydluzenie o: {((t_half_inhibited / t_half_normal - 1) * 100):.1f}%")
print()

print("ZADANIE ZALICZENIOWE")
print("=" * 60)

# Automatyczne znajdowanie optymalnych parametrów
optimal = find_optimal_params(L=10, target_t_half=120, tolerance=5)

if optimal:
    print(f"k_cat = {optimal['k_cat']:.4f}")
    print(f"k_off = {optimal['k_off']:.4f}")
    print(f"t1/2 = {optimal['t_half']:.1f}s")
    k_cat_opt = optimal['k_cat']
    k_off_opt = optimal['k_off']

# Symulacje
t_opt, R_opt, K_opt, E_opt = simulate(L=10, k_cat=k_cat_opt, k_off=k_off_opt, t_max=300)
t_half_opt = calculate_t_half(t_opt, E_opt)

t_base, R_base, K_base, E_base = simulate(L=10)
t_half_base = calculate_t_half(t_base, E_base)

# Wykresy
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

ax1 = axes[0, 0]
ax1.plot(t_base, E_base, label=f'Bazowe (t₁/₂={t_half_base:.1f}s)', linewidth=2, color='blue')
ax1.plot(t_opt, E_opt, label=f'Zoptymalizowane (t₁/₂={t_half_opt:.1f}s)', linewidth=2, color='red')
ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(x=120, color='green', linestyle=':', alpha=0.5, label='Cel: 120s')
ax1.set_xlabel('Czas [s]', fontsize=11)
ax1.set_ylabel('E* (Efektor)', fontsize=11)
ax1.set_title('Porownanie: bazowe vs zoptymalizowane', fontsize=12)
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 300)

ax2 = axes[0, 1]
ax2.plot(t_opt, R_opt, label='R* (Receptor)', linewidth=2)
ax2.plot(t_opt, K_opt, label='K* (Kinaza)', linewidth=2)
ax2.plot(t_opt, E_opt, label='E* (Efektor)', linewidth=2)
ax2.axvline(x=t_half_opt, color='red', linestyle='--', alpha=0.5, label=f't1/2={t_half_opt:.1f}s')
ax2.axhline(y=0.5, color='gray', linestyle=':', alpha=0.3)
ax2.set_xlabel('Czas [s]', fontsize=11)
ax2.set_ylabel('Frakcja aktywna', fontsize=11)
ax2.set_title('Wszystkie skladowe', fontsize=12)
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

ax3 = axes[1, 0]
k_cat_values = np.linspace(0.01, 0.2, 30)
t_halfs_kcat = []

for k_cat in k_cat_values:
    t, R, K, E = simulate(L=10, k_cat=k_cat, k_off=k_off_opt, t_max=300)
    t_h = calculate_t_half(t, E)
    t_halfs_kcat.append(t_h if t_h < 999 else 300)

ax3.plot(k_cat_values, t_halfs_kcat, 'o-', linewidth=2, markersize=4, color='purple')
ax3.axhline(y=120, color='green', linestyle='--', alpha=0.5, label='Cel: 120s')
ax3.axvline(x=k_cat_opt, color='red', linestyle=':', alpha=0.5, label=f'k_cat={k_cat_opt:.3f}')
ax3.set_xlabel('k_cat [1/s]', fontsize=11)
ax3.set_ylabel('t1/2 [s]', fontsize=11)
ax3.set_title('Wplyw k_cat', fontsize=12)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)

ax4 = axes[1, 1]
k_off_values = np.linspace(0.1, 1.5, 30)
t_halfs_koff = []

for k_off in k_off_values:
    t, R, K, E = simulate(L=10, k_cat=k_cat_opt, k_off=k_off, t_max=300)
    t_h = calculate_t_half(t, E)
    t_halfs_koff.append(t_h if t_h < 999 else 300)

ax4.plot(k_off_values, t_halfs_koff, 's-', linewidth=2, markersize=4, color='orange')
ax4.axhline(y=120, color='green', linestyle='--', alpha=0.5, label='Cel: 120s')
ax4.axvline(x=k_off_opt, color='red', linestyle=':', alpha=0.5, label=f'k_off={k_off_opt:.3f}')
ax4.set_xlabel('k_off [1/s]', fontsize=11)
ax4.set_ylabel('t1/2 [s]', fontsize=11)
ax4.set_title('Wpływ k_off', fontsize=12)
ax4.legend(fontsize=9)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print()

print("PYTANIE 1")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

k_off_test = [0.1, 0.5, 2.0]
colors_q1 = ['blue', 'orange', 'red']

for k_off, color in zip(k_off_test, colors_q1):
    t, R, K, E = simulate(L=10, k_off=k_off, t_max=100)
    t_h = calculate_t_half(t, E)
    t_h_display = t_h if t_h < 999 else 100
    axes[0].plot(t, E, label=f'k_off={k_off} (t₁/₂={t_h_display:.1f}s)', linewidth=2, color=color)

axes[0].axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
axes[0].set_xlabel('Czas [s]', fontsize=11)
axes[0].set_ylabel('E* (Efektor)', fontsize=11)
axes[0].set_title('Wplyw k_off na E*', fontsize=12)
axes[0].legend(fontsize=9)
axes[0].grid(True, alpha=0.3)

for k_off, color in zip(k_off_test, colors_q1):
    t, R, K, E = simulate(L=10, k_off=k_off, t_max=50)
    axes[1].plot(t, R, label=f'k_off={k_off}', linewidth=2, color=color)

axes[1].set_xlabel('Czas [s]', fontsize=11)
axes[1].set_ylabel('R* (Receptor)', fontsize=11)
axes[1].set_title('Wplyw k_off na R*', fontsize=12)
axes[1].legend(fontsize=9)
axes[1].grid(True, alpha=0.3)

k_off_range = np.linspace(0.1, 3.0, 25)
t_halfs_q1 = []
R_steady = []

for k_off in k_off_range:
    t, R, K, E = simulate(L=10, k_off=k_off, t_max=100)
    t_h = calculate_t_half(t, E)
    t_halfs_q1.append(t_h if t_h < 999 else 100)
    R_steady.append(R[-1])

ax3_twin = axes[2].twinx()
line1 = axes[2].plot(k_off_range, t_halfs_q1, 'o-', linewidth=2, color='purple', label='t₁/₂')
line2 = ax3_twin.plot(k_off_range, R_steady, 's-', linewidth=2, color='green', alpha=0.7, label='R*)')

axes[2].set_xlabel('k_off [1/s]', fontsize=11)
axes[2].set_ylabel('t1/2 [s]', fontsize=11, color='purple')
ax3_twin.set_ylabel('R*', fontsize=11, color='green')
axes[2].set_title('t1/2 i R* vs k_off', fontsize=12)
axes[2].tick_params(axis='y', labelcolor='purple')
ax3_twin.tick_params(axis='y', labelcolor='green')
axes[2].grid(True, alpha=0.3)

lines = line1 + line2
labels = [l.get_label() for l in lines]
axes[2].legend(lines, labels, fontsize=9)

plt.tight_layout()
plt.show()

print(f"k_off=0.1: R*={R_steady[0]:.3f}, t1/2={t_halfs_q1[0]:.1f}s")
print(f"k_off=2.0: R*={R_steady[-1]:.3f}, t1/2={t_halfs_q1[-1]:.1f}s")
print()

print("PYTANIE 2")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

L_range = np.logspace(-0.5, 2, 30)

for k_off, color, label in [(0.2, 'blue', 'k_off=0.2 (niskie)'),
                            (0.5, 'orange', 'k_off=0.5 (średnie)'),
                            (2.0, 'red', 'k_off=2.0 (wysokie)')]:
    t_halfs_L = []
    for L in L_range:
        t, R, K, E = simulate(L=L, k_off=k_off, t_max=100)
        t_h = calculate_t_half(t, E)
        t_halfs_L.append(t_h if t_h < 999 else 100)

    axes[0, 0].plot(L_range, t_halfs_L, 'o-', linewidth=2, label=label, color=color, markersize=4)

axes[0, 0].set_xlabel('Stezenie ligandu L', fontsize=11)
axes[0, 0].set_ylabel('t1/2 [s]', fontsize=11)
axes[0, 0].set_title('Krzywa nasycenia: L -> t1/2', fontsize=12)
axes[0, 0].set_xscale('log')
axes[0, 0].legend(fontsize=9)
axes[0, 0].grid(True, alpha=0.3)

L_range_dense = np.logspace(-0.5, 2, 100)
for k_off, color in [(0.2, 'blue'), (0.5, 'orange'), (2.0, 'red')]:
    t_halfs_dense = []
    for L in L_range_dense:
        t, R, K, E = simulate(L=L, k_off=k_off, t_max=100)
        t_h = calculate_t_half(t, E)
        t_halfs_dense.append(t_h if t_h < 999 else 100)

    gradient = np.abs(np.gradient(t_halfs_dense, L_range_dense))
    axes[0, 1].plot(L_range_dense, gradient, linewidth=2, color=color)

axes[0, 1].set_xlabel('Stezenie ligandu L', fontsize=11)
axes[0, 1].set_ylabel('|dt1/2/dL| (wrazliwosc)', fontsize=11)
axes[0, 1].set_title('Wrazliwosc t1/2 na zmiany L', fontsize=12)
axes[0, 1].set_xscale('log')
axes[0, 1].set_yscale('log')
axes[0, 1].grid(True, alpha=0.3)

k_cat_range = np.logspace(-2, -0.3, 25)

for L, marker, color in [(1, 'o', 'blue'), (10, 's', 'red'), (20, '^', 'green')]:
    t_halfs_kcat_L = []
    for k_cat in k_cat_range:
        t, R, K, E = simulate(L=L, k_cat=k_cat, t_max=200)
        t_h = calculate_t_half(t, E)
        t_halfs_kcat_L.append(t_h if t_h < 999 else 200)

    axes[1, 0].plot(k_cat_range, t_halfs_kcat_L, marker=marker, linewidth=2,
                    label=f'L={L}', color=color, markersize=4)

axes[1, 0].set_xlabel('k_cat [1/s]', fontsize=11)
axes[1, 0].set_ylabel('t1/2 [s]', fontsize=11)
axes[1, 0].set_title('Efekt "waskiego gardla"', fontsize=12)
axes[1, 0].set_xscale('log')
axes[1, 0].set_yscale('log')
axes[1, 0].legend(fontsize=9)
axes[1, 0].grid(True, alpha=0.3)

L_range_sat = np.logspace(-0.5, 2, 30)
R_steady_list = []
E_steady_list = []

for L in L_range_sat:
    t, R, K, E = simulate(L=L, k_off=0.5, t_max=100)
    R_steady_list.append(R[-1])
    E_steady_list.append(E[-1])

ax4_twin = axes[1, 1].twinx()
line1 = axes[1, 1].plot(L_range_sat, R_steady_list, 'o-', linewidth=2, color='blue', label='R*)')
line2 = ax4_twin.plot(L_range_sat, E_steady_list, 's-', linewidth=2, color='green', alpha=0.7, label='E*)')

axes[1, 1].set_xlabel('Stezenie ligandu L', fontsize=11)
axes[1, 1].set_ylabel('R*', fontsize=11, color='blue')
ax4_twin.set_ylabel('E*', fontsize=11, color='green')
axes[1, 1].set_title('Wysycenie: R* i E* vs L', fontsize=12)
axes[1, 1].set_xscale('log')
axes[1, 1].tick_params(axis='y', labelcolor='blue')
ax4_twin.tick_params(axis='y', labelcolor='green')
axes[1, 1].grid(True, alpha=0.3)

lines = line1 + line2
labels = [l.get_label() for l in lines]
axes[1, 1].legend(lines, labels, fontsize=9, loc='center right')

plt.tight_layout()
plt.show()