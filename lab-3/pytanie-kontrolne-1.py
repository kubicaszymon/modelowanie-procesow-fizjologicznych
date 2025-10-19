import numpy as np
import matplotlib.pyplot as plt

k = 2.068e-3
D = 2.0e-9  # Wybieramy jeden D dla testu
L = 300e-6
target_x = 100e-6

print("=" * 70)
print("PYTANIE KONTROLNE 1: TEST STABILNOSCI NUMERYCZNEJ")
print("=" * 70)

results = []

# N=300 (bazowy)
# N=600 (dx o polowe mniejsze)
for N in [300, 600]:
    print(f"\n{'='*70}")
    print(f"TEST DLA N = {N} punktow")
    print(f"{'='*70}")
    
    x = np.linspace(0, L, N)
    dx = L / (N - 1)
    idx = np.argmin(np.abs(x - target_x))
    
    print(f"dx = {dx*1e6:.4f} um")
    
    # Oblicz dt_max
    dt_max = (dx**2) / (2 * D)
    print(f"dt_max (warunek stabilnosci) = {dt_max*1e6:.4f} us")
    
    # Stabilny (40% dt_max)
    print("\ndt = 40% dt_max")
    dt_stable = 0.4 * dt_max
    print(f"dt = {dt_stable*1e6:.4f} us")
    
    phi = np.zeros(N)
    t_hist = []
    phi_hist = []
    
    for n in range(20000):
        if n % 200 == 0:
            t_hist.append(n * dt_stable)
            phi_hist.append(phi[idx])
        
        phi_new = phi.copy()
        for i in range(1, N-1):
            laplacian = (phi[i+1] - 2*phi[i] + phi[i-1]) / (dx**2)
            phi_new[i] = phi[i] + dt_stable * (D * laplacian - k * phi[i])
        
        phi = phi_new
        phi[0] = 1.0
        phi[-1] = phi[-2]
    
    print(f"Wartosc koncowa: phi[{idx}] = {phi[idx]:.4f}")
    
    stable_result = {
        't': t_hist.copy(),
        'phi': phi_hist.copy()
    }
    
    # Niestabilny (120% dt_max)
    print("\ndt = 120% dt_max")
    dt_unstable = 1.2 * dt_max
    print(f"dt = {dt_unstable*1e6:.4f} us")
    
    phi = np.zeros(N)
    t_hist = []
    phi_hist = []
    
    for n in range(20000):
        if n % 200 == 0:
            t_hist.append(n * dt_unstable)
            phi_hist.append(phi[idx])
        
        phi_new = phi.copy()
        for i in range(1, N-1):
            laplacian = (phi[i+1] - 2*phi[i] + phi[i-1]) / (dx**2)
            phi_new[i] = phi[i] + dt_unstable * (D * laplacian - k * phi[i])
        
        phi = phi_new
        phi[0] = 1.0
        phi[-1] = phi[-2]
        
        # Sprawdz czy nie wybuchlo
        if np.any(np.abs(phi) > 10):
            while len(t_hist) < 100:
                t_hist.append(n * dt_unstable)
                phi_hist.append(np.nan)
            break
    
    print(f"Wartosc koncowa: phi[{idx}] = {phi[idx]:.4f}")
    
    unstable_result = {
        't': t_hist.copy(),
        'phi': phi_hist.copy()
    }
    
    results.append({
        'N': N,
        'dx': dx,
        'dt_max': dt_max,
        'stable': stable_result,
        'unstable': unstable_result
    })

# WYKRES
fig, ax = plt.subplots(1, 1, figsize=(10, 7))

N_vals = [res['N'] for res in results]
dx_vals = [res['dx']*1e6 for res in results]
dt_max_vals = [res['dt_max']*1e6 for res in results]

# Slupki
bars = ax.bar([0, 1], dt_max_vals, color=['#2E86AB', '#A23B72'], 
              width=0.5, edgecolor='black', linewidth=2)

# Etykiety osi X
ax.set_xticks([0, 1])
ax.set_xticklabels([f'N = {n}\nΔx = {dx:.3f} μm' for n, dx in zip(N_vals, dx_vals)],
                   fontsize=13, fontweight='bold')

# Oś Y
ax.set_ylabel('delta_t$_{max}$ [μs]', fontsize=14, fontweight='bold')
ax.set_title('Wplyw zmniejszenia delta_x o połowe na warunek stabilnosci', 
            fontsize=15, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='y', linestyle='--')

# Wartości na słupkach
for i, val in enumerate(dt_max_vals):
    ax.text(i, val + 8, f'{val:.2f} μs', 
           ha='center', va='bottom', fontsize=13, fontweight='bold')

# Oblicz stosunek
ratio = dt_max_vals[0] / dt_max_vals[1]

# Ramka z wynikiem
textstr = f'Stosunek: {ratio:.2f}×\n(teoria: 4×)\n\nΔt$_{{max}}$ ∝ (Δx)²'
props = dict(boxstyle='round', facecolor='yellow', alpha=0.8, edgecolor='black', linewidth=2)
ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=13,
       verticalalignment='top', horizontalalignment='right', bbox=props, fontweight='bold')

# Dodatkowa adnotacja
ax.text(0.02, 0.97, 'Warunek stabilności:\nΔt ≤ (Δx)²/(2D)', 
       transform=ax.transAxes, fontsize=11,
       verticalalignment='top', horizontalalignment='left',
       bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7, edgecolor='black'))

plt.tight_layout()
plt.show()