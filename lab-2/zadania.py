import numpy as np
import matplotlib.pyplot as plt

ETA = 3.5e-3 # Pa*s
MMHG = 133.322 # Pa/mmHg

class Vessel:
    """
    Klasa reprezentująca naczynie kwionosne.
    
    Parametry:
        L : float
            Dlugosc naczynia [m]
        r : float
            Promien naczynia [m]
        eta : float
            Lepkosc cieczy [Pa*s]
    """
    
    def __init__(self, L, r, eta=ETA):
        self.L = L
        self.r = r
        self.eta = eta
        self.R = self._calculate_resistance()
        
    def _calculate_resistance(self):
        """
        Oblicza opor hydrodynamiczny
        R = 8*n*L/(pi*r^4)
        """
        return (8*self.eta*self.L)/(np.pi*self.r**4)
    
    def update_radius(self, r_new):
        """Aktualizuje promien i przelicza opor"""
        self.r = r_new
        self.R = self._calculate_resistance()
        
    def update_viscosity(self, eta_new):
        """Aktualizuje lepkosc i przelicza opor"""
        self.eta = eta_new
        self.R = self._calculate_resistance()
        

def calculate_parallel_resistance(resistances):
    """Oblicza opor zastepczy dla naczyn polaczonych rownolegle"""
    return 1/np.sum(1/np.array(resistances))

def calculate_series_resistance(resistances):
    """Oblicza opor zastepczy dla naczyn polaczonych szeregowo"""
    return np.sum(resistances)

def build_vascular_network(eta=ETA):
    """Buduje siec naczyniiowa: aorta - 2 galezie - 4 tetniczki"""
    aorta = Vessel(L=0.3, r=0.012, eta=eta)
    branch1 = Vessel(L=0.2, r=0.006, eta=eta)
    branch2 = Vessel(L=0.2, r=0.006, eta=eta)
    term = [Vessel(L=0.02, r=0.0015, eta=eta) for _ in range(4)]
    
    return aorta, branch1, branch2, term

def calculate_network_resistance(aorta, branch1, branch2, term):
    """Oblicza calkowity opor sieci naczyniowej"""
    
    # Opor rownolegly tetniczek
    R_term1 = calculate_parallel_resistance([term[0].R, term[1].R])
    R_term2 = calculate_parallel_resistance([term[2].R, term[3].R])
    
    # Opor szeregowy kazdej sciezki 
    R_path1 = calculate_series_resistance([branch1.R, R_term1])
    R_path2 = calculate_series_resistance([branch2.R, R_term2])
    
    # Opor rownolegly obu sciezek
    R_parallel_paths = calculate_parallel_resistance([R_path1, R_path2])
    
    # Calkowity opor
    R_total = aorta.R + R_parallel_paths
    
    return R_total, R_term1, R_term2, R_path1, R_path2
    
def calculate_flows(aorta, branch1, branch2, term, P_in, P_out):
    """Oblicza przeplywy w poszczegolnych czesciach sieci"""
    
    R_total, R_term1, R_term2, R_path1, R_path2 = calculate_network_resistance(
        aorta, branch1, branch2, term    
    )
    
    # Calkowity przeplyw
    Q_total = (P_in - P_out)/R_total
    
    # Cisnienie po aorcie
    P_after_aorta = P_in - Q_total * aorta.R
    
    # Przeplywy w kazdej sciezce
    Q_path1 = (P_after_aorta - P_out) / R_path1
    Q_path2 = (P_after_aorta - P_out) / R_path2
    
    # Cisnienie po galeziach
    P_after_branch1 = P_after_aorta - Q_path1 * branch1.R
    P_after_branch2 = P_after_aorta - Q_path2 * branch2.R
    
    # Przeplywy w tetniczkach
    Q_term = [
        (P_after_branch1 - P_out) / term[0].R,
        (P_after_branch1 - P_out) / term[1].R,
        (P_after_branch2 - P_out) / term[2].R,
        (P_after_branch2 - P_out) / term[3].R
    ]
    
    return {
        'Q_total': Q_total,
        'Q_path1': Q_path1,
        'Q_path2': Q_path2,
        'Q_term': Q_term,
        'R_total': R_total
    }
    

def sensitivity_analysis_radius(aorta, branch1, branch2, term, P_in, P_out):
    """Analiza wrazliwosci na zmiane promienia tetniczek koncowych"""
    
    baseline = calculate_flows(aorta, branch1, branch2, term, P_in, P_out)
    results = {'baseline': baseline}
    
    for pct in [-0.1, 0.1]:
        term_modified = [Vessel(L=t.L, r=t.r * (1 + pct), eta=t.eta) for t in term]
        flows = calculate_flows(aorta, branch1, branch2, term_modified, P_in, P_out)
        results[f'{pct:+.0%}'] = flows
        
    return results

def compare_viscosity(P_int, P_out):
    """Porownanie perfuzji dla dwoch wartosci lepkosci"""
    
    aorta1, branch1_1, branch2_1, term1 = build_vascular_network(eta=3.5e-3)
    flows1 = calculate_flows(aorta1, branch1_1, branch2_1, term1, P_in, P_out)
    
    aorta2, branch1_2, branch2_2, term2 = build_vascular_network(eta=2.8e-3)
    flows2 = calculate_flows(aorta2, branch1_2, branch2_2, term2, P_in, P_out)
    
    return flows1, flows2
    
# ============= PROGRAM ===================

P_in = 100 * MMHG
P_out = 10 * MMHG

aorta, branch1, branch2, term = build_vascular_network()
flows = calculate_flows(aorta, branch1, branch2, term, P_in, P_out)

print(f"Opor aorty: {aorta.R:.2e} Pa·s/m³")
print(f"Opor galezi 1: {branch1.R:.2e} Pa·s/m³")
print(f"Opor galezi 2: {branch2.R:.2e} Pa·s/m³")
print(f"Opor tetniczki: {term[0].R:.2e} Pa·s/m³")
print(f"Calkowity przeplyw: {flows['Q_total']*1e6:.2f} ml/s")
print(f"Przeplyw sciezka 1: {flows['Q_path1']*1e6:.2f} ml/s")
print(f"Przeplyw sciezka 2: {flows['Q_path2']*1e6:.2f} ml/s")
for i, q in enumerate(flows['Q_term'], 1):
    print(f"Tetniczka {i}: {q*1e6:.2f} ml/s")

sens_results = sensitivity_analysis_radius(aorta, branch1, branch2, term, P_in, P_out)
baseline_Q = sens_results['baseline']['Q_total'] * 1e6
print(f"\nPrzeplyw bazowy: {baseline_Q:.2f} ml/s")
for key in ['-10%', '+10%']:
    Q = sens_results[key]['Q_total'] * 1e6
    change = ((Q - baseline_Q) / baseline_Q) * 100
    print(f"Zmiana promienia {key}: Q = {Q:.2f} ml/s (zmiana: {change:+.1f}%)")

flows_normal, flows_anemia = compare_viscosity(P_in, P_out)
print(f"\nη = 3.5 mPa*s: Q_total = {flows_normal['Q_total']*1e6:.2f} ml/s")
print(f"η = 2.8 mPa*s: Q_total = {flows_anemia['Q_total']*1e6:.2f} ml/s")
change = ((flows_anemia['Q_total'] - flows_normal['Q_total']) / flows_normal['Q_total']) * 100
print(f"Wzrost przeplywu: {change:+.1f}%")

# ==================== WIZUALIZACJE ====================

plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(15, 10))

# Analiza wrazliwosci na promien
ax1 = plt.subplot(2, 2, 1)
radius_changes = ['Bazowy', '-10%', '+10%']
Q_values = [
    sens_results['baseline']['Q_total'] * 1e6,
    sens_results['-10%']['Q_total'] * 1e6,
    sens_results['+10%']['Q_total'] * 1e6
]
colors = ['#2E86AB', '#A23B72', '#F18F01']
bars = ax1.bar(radius_changes, Q_values, color=colors, alpha=0.8, edgecolor='black')
ax1.set_ylabel('Przeplyw calkowity [ml/s]', fontsize=11)
ax1.set_title('Wplyw zmiany promienia tetniczek na przeplyw', fontsize=12, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, Q_values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{val:.1f}', ha='center', va='bottom', fontsize=10)

# Porownanie perfuzji dla roznych lepkosci
ax2 = plt.subplot(2, 2, 2)
x = np.arange(4)
width = 0.35
Q_normal = [q * 1e6 for q in flows_normal['Q_term']]
Q_anemia = [q * 1e6 for q in flows_anemia['Q_term']]

bars1 = ax2.bar(x - width/2, Q_normal, width, label='η = 3.5 mPa·s (norma)', 
                color='#2E86AB', alpha=0.8, edgecolor='black')
bars2 = ax2.bar(x + width/2, Q_anemia, width, label='η = 2.8 mPa·s (anemia)', 
                color='#F18F01', alpha=0.8, edgecolor='black')

ax2.set_xlabel('Numer tetniczki', fontsize=11)
ax2.set_ylabel('Przeplyw [ml/s]', fontsize=11)
ax2.set_title('Perfuzja tetniczek: norma vs anemia', fontsize=12, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(['T1', 'T2', 'T3', 'T4'])
ax2.legend(fontsize=9)
ax2.grid(axis='y', alpha=0.3)

# Rozklad oporow w sieci
ax3 = plt.subplot(2, 2, 3)
R_values = [aorta.R, branch1.R, term[0].R]
R_labels = ['Aorta', 'Galaz', 'Tetniczka']
colors_r = ['#C73E1D', '#6A994E', '#BC4B51']
bars_r = ax3.bar(R_labels, R_values, color=colors_r, alpha=0.8, edgecolor='black')
ax3.set_ylabel('Opor hydrodynamiczny [Pa·s/m³]', fontsize=11)
ax3.set_title('Rozklad oporow w poszczeglnych typach naczyn', fontsize=12, fontweight='bold')
ax3.set_yscale('log')
ax3.grid(axis='y', alpha=0.3, which='both')

ax4 = plt.subplot(2, 2, 4)
L_values = np.linspace(0.1, 0.5, 30)
Q_vals = []
R_vals = []

for L in L_values:
    branch_mod = Vessel(L=L, r=0.006, eta=ETA)
    flows_mod = calculate_flows(aorta, branch_mod, branch2, term, P_in, P_out)
    Q_vals.append(flows_mod['Q_path1'] * 1e6)
    R_vals.append(branch_mod.R / 1e9)

ax4_twin = ax4.twinx()
line1 = ax4.plot(L_values * 100, Q_vals, 'o-', color='#2E86AB', linewidth=2.5, 
                 markersize=5, label='Przeplyw')
line2 = ax4_twin.plot(L_values * 100, R_vals, 's-', color='#F18F01', linewidth=2.5, 
                      markersize=5, label='Opor')

ax4.axvline(x=20, color='red', linestyle='--', alpha=0.6, linewidth=1.5)
ax4.set_xlabel('Dlugość galezi [cm]', fontsize=11)
ax4.set_ylabel('Przeplyw [ml/s]', fontsize=11, color='#2E86AB')
ax4_twin.set_ylabel('Opor [10^9 Pa·s/m³]', fontsize=11, color='#F18F01')
ax4.set_title('Wplyw dlugosci galezi na przeplyw i opor', fontsize=12, fontweight='bold')
ax4.tick_params(axis='y', labelcolor='#2E86AB')
ax4_twin.tick_params(axis='y', labelcolor='#F18F01')
ax4.grid(True, alpha=0.3)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax4.legend(lines, labels, fontsize=9, loc='upper left')

plt.tight_layout()
plt.savefig('analiza_przeplywow.png', dpi=300, bbox_inches='tight')
plt.show()