# Optymalizacja parametrów procesu dializy
Autor: Szymon Kubica
Data: 03.12.2025

## Zadanie 1,2,3:
Zaimplementowano podane w zadaniach wzory oraz na ich podstawie obliczono parametry Qb oraz Qd dla jak najmniejszego czasu
<img width="766" height="1121" alt="image" src="https://gist.github.com/user-attachments/assets/98e4e9c2-ef1a-4b08-8129-073db51e3dcb" />

# Zadanie zaliczeniowe
Dla modelu jednokompartowego wyznaczono zaleznosc objętnosci od czasu przy wyżej obliczonych optymalnych parametrach
<img width="872" height="552" alt="image" src="https://gist.github.com/user-attachments/assets/a9ae2c8e-6474-49ed-898a-424a3fb4fc39" />
Jak widać wynik jest funkcją liniową ze względu na parametr objętości który znajduję się w liczniku wzoru.

Zaimplementowano również model dwukompartowy dla którego również zoptymalizowano parametry Qb oraz Qd. 
Jako początkowe Cb wyznaczono wartość 100.0 a współczynnik k = 0.5. 
Funkcja optymalizacyjna została zaimplementowana w taki sposób, żeby znaleźć najlepsze parametry dla końcowego Cb = 20.0
<img width="289" height="89" alt="image" src="https://gist.github.com/user-attachments/assets/fb576205-d33c-49a2-9a76-00d24df7a7f9" />
<img width="850" height="525" alt="image" src="https://gist.github.com/user-attachments/assets/102ccd29-33b1-472d-97aa-ae49146d88eb" />

## Czemu zwiększanie Qd powyżej pewnej wartości przestaje istotnie skracać czas?
Ponieważ Qd w wzorze na Klirens jest mnożona przez stałą b która w przypadku ćwiczenia została wyznaczona na 0.2, przez co zwiększenie Qd nie odgrywa tak wielkiej roli.
Dodatkowo sam wyliczony Klirens występuje jest zawsze mnożony przez stężenie co tym bardziej od pewnych wartości minimalizuje wpływ.

## Jak uwzględnić ograniczenia hemodynamiczne pacjenta w modelu (np.górne granice Qb)?
Kiedy pacjent na np słabą przetokę można po prostu zmniejszyć zakres "bounds" dla Qb do 300 przez co algorytm nawet nie spróbuje przekroczyc tej liczby. 
Kolejnym sposobem jest implementacja funkcji kary która dla błędnego parametru zwróci kosmiczny wynik.

