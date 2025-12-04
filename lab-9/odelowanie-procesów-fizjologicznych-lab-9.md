#  Analiza farmakokinetyki leków
Autor: Szymon Kubica
Data: 04.12.2025

## Zadanie 1 
Dla podania doustnego zostały wygenerowane zaszumione dane według instrukcji i parametrów z listy
<img width="844" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/7caea57d-8a4f-43f6-aede-173d5bce1d18" />

## Zadanie 2
Następnie do zaszumionych danych zostały dopasowane przybliżone parametry w celu usunięcia szumu
```
Fitted params: [7.94915366e-01 3.16937266e+02 7.60470089e-01 3.11538369e-01
 1.08227968e+01]
 ```
 <img width="844" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/d9855d35-451f-40e5-adf5-e9e4d41ef0d8" />


## Zadanie 3
Dla danych z poprzednich zadań obliczono Tmax, Cmax, T1/2 oraz AUC
| Parametr   | Wartość |
|--------|-----|
| Cmax  | 12.577419548413802 | 
| Tmax    | 1.92964824120603 | 
| T1/2  | 5.6383588168707 | 
| AUC  | 75.07863184222386 |

# Zadanie zaliczeniowe
Zaimplementowano modele dla wlewu stałego oraz podawaniu bolusem co 8h przez 72h ibuprofenu. Dla wariantu z wlewem wartość R0 została dobrana eksperymentalnie jako 133 mg/h
<img width="841" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/15199f91-3a67-4cd6-9f42-a8d9123e86e3" />

oraz policzono dla obu parametry Tmax, Cmax, T1/2 oraz AUC.

| Parametr | Wartość dla bolusa     | Wartość dla wlewu      |
|---------:|-----------------------:|-----------------------:|
| Cmax     | 34.64752745322006      | 34.05017920457243      |
| Tmax     | 72.0                   | 72.0                   |
| T1/2     | 1.9538478509815418     | —                      |
| AUC      | 912.6168775995634      | 2341.77326342194       |


Dla bolusa wartość T1/2 wypisano pierwszy raz w którym stężenie osiąga ten poziom natomiast wartość ta będzie osiągana cyklicznie co około 8h.
Dla wlewu wartość T1/2 nie występuje z racji tego że scenariusz nie przewiduje końca wlewu.

Parametr toksyczności dla bolusa jest mniejszy przez 72h natomiast bardzo szybko może dojść do górnej granicy toksyczności co może być niebezpieczne. Z drugiej strony szybko też spada co może grozić ryzykiem braku działania leku jeśli wykres szybo wejdzie w dolną granice leku.
W przypadku wlewu toksyczność będzie rosła powoli co eliminuje ryzyko nieumyślnego zatrucia na początku ale niesie za to ryzyko długotrwałego zatrucia w przypadku pomyłki w obliczeniach i braku kontroli. Jeśli dawka leku jest dobrze dobrana pod względem toksyczności wtedy wlew wydaje się być bezpiecznym i idealnym sposobem utrzymania docelowwej dawki leku przez dłuższy okres.

Metodę podawania bolusem powinniśmy stosować w momencie wymaganego szybkiego wzrostu stężenie. Przykładem może być morfina po wypadku lub adrenalina w przypadku zatrzymania akcji serca
Wlew stały powinniśmy wybrać gdy chcemy osiągnąć stały poziom stężenia danego leku przez dłuższy czas a lek sam w sobie ma krótki czas działania np. dopamina, niektóre antybiotyki czy w chemioterapi.

## Dlaczego przy ka ≈ k dopasowanie staje się niestabilne?
Pod względem matematycznym gdy ka będzie bliskie k lub po prostu równe, będziemy wtedy dzielić przez zero co jest koszmarne.
Pod względem algorytmicznym, w metodzie curve_fit algorytm szuka spadu z najmniejszym błędem. W momencie gdy te 2 parametry są sobie bliskie algorytm przestanie znajdować "wgłębienia" ponieważ ich po prostu nie ma i algorytm głupieje.

## Co się zmienia na wykresie, gdy biodostępność F < 1. Co się zmienia, gdy F jest zmienna osobniczo? Jakie czynniki mogą wpływać na sobniczą zmienność F?
Gdy F < 1 spadnie wysokość piku stężenia leku we krwi a ekspozycja na lek jest zmniejsza. Gdy F będzie zmienną osobniczą terapia może dla niektórych pacjentów zadziałać bo stężenie będzie w porządku a dla niektórych nie.
Na osobniczą zmienność F może wpływać:
- wątroba która może "zniszczyć" trochę leku,
- chore jelita mogą zmniejszać wchłanianie,
- wiek i stan zdrowia.
