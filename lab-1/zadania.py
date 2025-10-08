import numpy as np
import matplotlib.pyplot as plt

# V = objetosc
# P = cisnienie
# C = podatnosc
# R = opor naczyniowy

V = np.linspace(0, 10, 500)
P_lin = 5*V + 0.0
P_exp = 2*np.exp(0.5*V) - 2
P_log = 120/(1+np.exp(-(V-5))) - 60

# P(V)
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
for P, label in [(P_lin,'liniowy'),(P_exp,'wykladniczy'),(P_log,'logistyczny')]:
    plt.plot(V,P,label=label)
    
plt.xlabel('V [arb]')
plt.ylabel('P [arb]')
plt.title('Zaleznosc P(V)')
plt.legend()
plt.grid(True, alpha=0.3)

# C(V)
plt.subplot(1,2,2)
for P,label in [(P_lin,'liniowy'),(P_exp,'wykladniczy'),(P_log,'logistyczny')]:
    C = np.gradient(V, P)
    plt.plot(V, C, label=label)
    
plt.xlabel('V [arb]')
plt.ylabel('C = dV/dP [arb]')
plt.title('Podatnosc C(V)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Rozkurcz Windkessela
R, C = 1.5, 1.0
t = np.linspace(0, 5, 500)
P0, Pd = 120, 70
P_t = Pd + (P0-Pd)*np.exp(-t/(R*C))

plt.figure()
plt.plot(t, P_t)
plt.xlabel('t [s]')
plt.ylabel('P [mmHg]')
plt.title('Rozkurcz – model Windkessela')
plt.grid(True, alpha=0.3)
plt.show()

# Pytanie kontrolne
plt.figure(figsize=(10,6))

Pi,Pd = 120,70
C = 1.0
t = np.linspace(0,5,500)

# Rozne wartosci R
for R in [0.5,1.5,3.0]:
    tau = R*C
    P_t = Pd+(Pi-Pd)*np.exp(-t/tau)
    plt.plot(t,P_t,label=f'R={R}, tau={tau:.1f}s', lw=2)
    print(f"R={R} - tau={R*C:.1f}s")
    
plt.axhline(Pi, color='gray', linestyle='--', alpha=0.5)
plt.axhline(Pd, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('Czas [s]')
plt.ylabel('Ciśnienie [mmHg]')
plt.title('Wpływ oporu R na spadek ciśnienia')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()








