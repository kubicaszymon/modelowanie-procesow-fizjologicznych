import numpy as np
import matplotlib.pyplot as plt

# Parametry
L, N = 300e-6, 300 
x = np.linspace(0, L, N)
dx = L / (N - 1)
target_x = 100e-6
idx = np.argmin(np.abs(x - target_x))
k = 2.068e-3  # Indeks 264068

print("=" * 60)
print(f"L = {L*1e6:.0f} um, N = {N} punktow")
print(f"k = {k:.4e} 1/s")
print(f"x = {target_x*1e6:.0f} um")
print("=" * 60)

results = []

for D in [1.5e-9, 2.0e-9, 2.5e-9]:
    # Warunek stabilnosci
    dt_max = (dx**2) / (2 * D)
    dt = 0.4 * dt_max
    
    print(f"\n--- D = {D:.2e} m2/s ---")
    print(f"dt_max = {dt_max:.4e} s, dt = {dt:.4e} s")
    
    # Stan ustalony)
    lambda_param = np.sqrt(k / D)
    phi_steady = np.cosh(lambda_param * (L - x)) / np.cosh(lambda_param * L)
    phi_steady_target = phi_steady[idx]
    threshold = 0.95 * phi_steady_target
    
    print(f"Stan ustalony w x={target_x*1e6:.0f}um: {phi_steady_target:.4f}")
    print(f"Prog 95%: {threshold:.4f}")
    
    # Inicjalizacja
    phi = np.zeros(N)
    reached = None
    t_history = []
    phi_history = []
    
    # Petla czasowa
    for n in range(500000):
        if n % 1000 == 0:
            t_history.append(n * dt)
            phi_history.append(phi[idx])
            
        # Schemat roznic skonczonych
        phi_new = phi.copy()
        for i in range(1, N-1):
            d2phi_dx2 = (phi[i+1] - 2*phi[i] + phi[i-1]) / (dx**2)
            phi_new[i] = phi[i] + dt * (D * d2phi_dx2 - k * phi[i])
        
        phi = phi_new
        phi[0] = 1.0         # Dirichlet
        phi[-1] = phi[-2]    # Neumann
        
        # 95%
        if reached is None and phi[idx] >= threshold:
            reached = n * dt
            print(f"Osiagnieto 95% w t = {reached:.3f} s")
            break
            
    if reached is None:
        print(f"Nie osiagnieto 95%")
        
    results.append({
        'D': D,
        't_95': reached,
        't_history': t_history,
        'phi_history': phi_history,
        'threshold': threshold
    })

# PODSUMOWANIE
print("\n" + "=" * 60)

fastest_D = None
fastest_time = float('inf')

for res in results:
    if res['t_95'] is not None:
        print(f"D = {res['D']:.1e} m²/s -> t_95% = {res['t_95']:.3f} s")
        if res['t_95'] < fastest_time:
            fastest_time = res['t_95']
            fastest_D = res['D']

if fastest_D is not None:
    print(f"\nTkanka z D = {fastest_D:.1e} m²/s dotlenia sie najszybciej")
    print(f"Czas: t_95% = {fastest_time:.3f} s")

print("=" * 60)

# WYKRESY
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Wykres 1: Ewolucja stezenia w czasie
for res in results:
    ax1.plot(res['t_history'], res['phi_history'],
             label=f"D = {res['D']:.1e} m²/s", linewidth=2.5)
    if res['t_95'] is not None:
        ax1.axvline(res['t_95'], linestyle='--', alpha=0.6, linewidth=2)
    ax1.axhline(res['threshold'], linestyle=':', alpha=0.5, linewidth=1.5)

ax1.set_xlabel('Czas [s]', fontsize=13, fontweight='bold')
ax1.set_ylabel('Stezenie φ [-]', fontsize=13, fontweight='bold')
ax1.set_title(f'Ewolucja stezenia w x = {target_x*1e6:.0f} μm', 
              fontsize=14, fontweight='bold')
ax1.legend(fontsize=11, loc='lower right')
ax1.grid(True, alpha=0.3)

# Wykres 2: Porownanie czasow t_95%
D_vals = [res['D'] * 1e9 for res in results if res['t_95'] is not None]
t_vals = [res['t_95'] for res in results if res['t_95'] is not None]

if len(D_vals) > 0:
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    bars = ax2.bar(range(len(D_vals)), t_vals, 
                   color=colors[:len(D_vals)], 
                   edgecolor='black', linewidth=2, width=0.6)
    ax2.set_xticks(range(len(D_vals)))
    ax2.set_xticklabels([f"{d:.1f}" for d in D_vals], fontsize=12)
    ax2.set_xlabel('D [×10⁻⁹ m²/s]', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Czas t$_{95\\%}$ [s]', fontsize=13, fontweight='bold')
    ax2.set_title('Porownanie czasow osiagniecia 95%', 
                  fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Wartosci na slupkach
    for i, (d, t) in enumerate(zip(D_vals, t_vals)):
        ax2.text(i, t + 1, f'{t:.2f} s', 
                ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()