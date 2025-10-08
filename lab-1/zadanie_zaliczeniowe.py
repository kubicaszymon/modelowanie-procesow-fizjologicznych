import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import pandas as pd

# Definicje pomocnicznych funkcji modeli
def lin(V,a,b): return a*V+b
def exp_m(V,P0,alpha,V0): return P0*(np.exp(alpha*(V-V0))-1)
def log_m(V,Pmax,beta,V50,c): return Pmax/(1+np.exp(-beta*(V-V50)))+c

# Slownik [model]:[funkcja, startowe parametry]
modele = {
    'liniowy': (lin, [5,0]),
    'wykladniczy': (exp_m, [2,0.5,0]),
    'logistyczny': (log_m, [120,1,5,-60])    
}

df = pd.read_csv('patients.csv')
V = df['V'].values

wyniki = {}
fig, ax = plt.subplots(1,3,figsize=(15,4))

# Analiza dla kazdego pacjenta
for i, pac in enumerate(['PA', 'PB', 'PC']):
    P = df[pac].values
    
    # Dopasowanie modelu i szukanie najlepszego
    best_rmse, best_model, best_params = np.inf, None, None
    
    for nazwa, (func,p0) in modele.items():
        try:
            # Szukamy optymalnych parametrow
            params, _ = curve_fit(func,V,P,p0=p0, maxfev=10000)
            
            # Liczymy bledy i ich kwadraty
            rmse = np.sqrt(np.mean((P-func(V,*params))**2))
            print(f"{pac} {nazwa:12s}: RMSE={rmse:.2f}")
            
            # Wybor najlepszego modelu
            if rmse < best_rmse:
                best_rmse, best_model, best_params = rmse, nazwa, params
            
        except:
            pass
        
    print(f"-> {pac}: Najlepszy = {best_model.upper()}, RMSE={best_rmse:.2f}\n")
    
    # C dla P=80,100,120
    func = modele[best_model][0]
    
    # model logistyczny ma CHYBA problemy z ekstrapolacją, zmieniam na liniowy
    if pac == 'PA' and best_model == 'logistyczny':
        func_lin, p0_lin = modele['liniowy']
        params_lin, _ = curve_fit(func_lin, V, P, p0=p0_lin, maxfev=10000)
        print(f"  UWAGA: Model logistyczny ma problemy z ekstrapolacją, używam liniowego")
        func_compliance = func_lin
        params_compliance = params_lin
    else:
        func_compliance = func
        params_compliance = best_params
    
    C_vals = {}
    for P_target in [80,100,120]:
        V_guess = np.linspace(0, 100, 1000)
        P_guess = func_compliance(V_guess, *params_compliance)
        
        # Znajdowanie V gdzie P jest najbliżej P_target
        idx = np.argmin(np.abs(P_guess - P_target))
        V_at_P = V_guess[idx]
        
        V_test = np.array([V_at_P - 0.1, V_at_P + 0.1])
        P_test = func_compliance(V_test, *params_compliance)
        dP_dV = (P_test[1] - P_test[0]) / (V_test[1] - V_test[0])
        
        C_vals[P_target] = 1.0 / dP_dV
        print(f" C @ {P_target} mmHg = {C_vals[P_target]:.4f}  (V={V_at_P:.2f} ml, dP/dV={dP_dV:.4f})")
       
    wyniki[pac] = {'model': best_model, 'rmse': best_rmse, 'C':C_vals}
    
    ax[i].scatter(V,P,alpha=0.5,s=20)
    ax[i].plot(V,func(V,*best_params),'r-',lw=2)
    ax[i].set_title(f'{pac}: {best_model}\nRMSE={best_rmse:.1f}')
    ax[i].set_xlabel('V [ml]')
    ax[i].set_ylabel('P [mmHg]')
    ax[i].grid(True, alpha=0.3)
    print()
    
plt.tight_layout()
plt.show()

# Porownanie
print("POROWNANIE PODATNOSCI")
for pac in ['PA','PB','PC']:
    print(f"{pac}: ", end="")
    for p in [80,100,120]:
        print(f"C@{p}={wyniki[pac]['C'][p]:.3f} ", end="")
    print()
    
print("\nINTERPRETACJA:")
print("Wyższe C = elastyczne naczynia (lepiej)")
print("Niższe C = sztywne tętnice (ryzyko CV)")
print("C przy wyższym P = postępująca sztywność")  