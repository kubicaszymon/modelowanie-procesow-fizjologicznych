# Podatność naczyń krwionośnych
**Autor:** Szymon Kubica **Data:** 08.10.2025

## 1. Cel
Wybór najlepszego modelu P-V dla pacjentów A,B,C oraz analiza podatności C przy ciśnieniach 80,100,120 mmHg.

## 2. Metoda

### Dopasowanie modeli
Dla każdego pacjenta dopasowano 3 modele (liniowy, wykładniczy, logistyczny) metodą najmniejszych kwadratów. Najlepszy model wybrano na podstawie RMSE.

```python
rmse = np.sqrt(np.mean((P-func(V,*params))**2))
```

### Obliczanie podatności C
```python
V_dense = np.linspace(V.min(),V.max(),1000)
P_dense = func(V_dense, *best_params)
dP_dV = np.gradient(P_dense,V_dense)
    
C_vals = {}
for P_target in [80,100,120]:
  idx = np.argmin(np.abs(P_dense-P_target))
  C_vals[P_target] = 1.0/dP_dV[idx]
```

### Uwaga dotycząca ekstrapolacji
**Problem z modelem logistycznym dla pacjenta A:** Model logistyczny dla PA miał najlepsze RMSE (0.7) w zakresie danych, ale wykazywał problemy z ekstrapolacją poza zakres pomiarów. W zakresie V=40-50 ml (gdzie szukamy P=80-120 mmHg) model dawał stałe wartości P≈22 mmHg, co prowadziło do dP/dV≈0 i błędnych wartości compliance (nieskończone). 

**Rozwiązanie:** Dla obliczenia compliance pacjenta A użyto modelu liniowego, który daje sensowne wartości P w zakresie ekstrapolacji, zachowując model logistyczny do analizy i wykresów w zakresie danych.

## 3. Wyniki

| Pacjent | Model | RMSE | C@80 | C@100 | C@120 |
|---------|-------|------|------|-------|-------|
| PA | Logistyczny* | 0.7 | 0.4785 | 0.4785 | 0.4785 |
| PB | Wykładniczy | 1.1 | 0.0335 | 0.0268 | 0.0223 |
| PC | Wykładniczy | 2.2 | 0.2405 | 0.2089 | 0.1848 |

*Model logistyczny używany do analizy, model liniowy do obliczenia compliance

## 4. Interpretacja kliniczna

### Pacjent A:
- **Model logistyczny** - typowa fizjologiczna charakterystyka
- **Wysokie C, stabilne** - elastyczne zdrowe naczynia
- **Niskie ryzyko CV**

### Pacjent B:
- **Model wykładniczy** - rosnąca sztywność
- **Średnie C, spadające** - możliwy proces starzenia naczyń
- **Umiarkowane ryzyko CV**

### Pacjent C:
- **Model wykładniczy** - bardzo stromne P(V)
- **Niskie C, gwałtowny spadek** - sztywne tętnice, możliwa miażdżyca
- **Wysokie ryzyko CV**

**Wniosek:** Im niższa podatność C i większy jej spadek przy wzroście P, tym gorsze rokowania.

## 5. Pytanie kontrolne

### Jak zmiana R wpływa na stałą zaniku ciśnienia w modelu Windkessela?

Wykonano symulacje (plik zadania.py na końcu) dla trzech wartości oporu przy stałej podatności C=1.0

```python
Pi,Pd = 120,70
C = 1.0
t = np.linspace(0,5,500)

# Różne wartości R
for R in [0.5,1.5,3.0]:
    tau = R*C
    P_t = Pd+(Pi-Pd)*np.exp(-t/tau)
```

**Wpływ oporu na spadek ciśnienia:**

Zwiększony opór R (np. w nadciśnieniu, zwężeniu naczyń) prowadzi do:
- Wydłużonego czasu powrotu do ciśnienia rozkurczowego,
- Zwiększonego obciążenia następczego lewej komory,
- Większego ryzyka niewydolności serca

Zmiana oporu R proporcjonalnie wpływa na tau, co bezpośrednio kontroluje dynamikę rozkurczu. Klinicznie, podwyższony opór wydłuża relaksację i zwiększa obciążenie serca.

