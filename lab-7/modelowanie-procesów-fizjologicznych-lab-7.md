# Modelowanie zjawiska epidemii
Autor: Szymon Kubica
Data: 02.12.2025

## Zadanie 1: Implementacja modelu SIR oraz SEIR
Zaimplementowano oba modele, przy czym dokonano modyfikacji wartość parametru beta na 1 aby uzyskać widoczne rezultaty

<img width="833" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/746e465f-a903-4730-a281-a0e6f7a14ff9" />
<img width="833" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/2dece845-2135-4e10-b47e-9675ce03a558" />

## Zadanie 2: Redukcja parametru beta
W tym ćwiczeniu razem z redukcją parametru beta, zmieniono również czas po którym ma się zmieniać na 15 dzień ponieważ po 60 dniu epidemia już wygasa przez co zmiana parametru beta nic nie zmienia.
<img width="833" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/a9a8cdff-fec7-4e49-b608-9c0a827f4155" />
<img width="846" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/e7992605-eed2-4a2e-9822-21712017c34d" />

## Zadanie 3: Szacowanie parametru beta
Zaimplementowano wyszukiwanie po siatce z pewnymi modyfikacjami:
- dla SIR rozpatrywano przedział czasowy 0-1000 dni
- dla SEIR rozpatrywano 0-2000 dni

<img width="833" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/df17c60f-7789-4ab3-a1a7-61029a410433" />
<img width="833" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/acbef0c3-93f6-4fea-9cf6-e1063842135e" />

## Zadanie zaliczeniowe
Wczytano plik z rzeczywistymi danymi oraz zobrazowano te dane na wykresie.
<img width="846" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/40a6ebc8-be15-4056-9b52-62e1fc6988cb" />

Zaimplementowano nowy model SEIR ze zmieniającym się parametrem beta w czasie tak żeby choć trochę odwzorować dynamicznie zmieniającą się zaraźliwość choroby spowodowaną różnymi czynnikami (maseczki, lockdown, poluzowanie). 

<img width="846" height="547" alt="image" src="https://gist.github.com/user-attachments/assets/af81346d-345e-4730-bfde-ee3788894317" />

Dalsze modelowanie wykresu można byłoby zaimplementować używając metod scipy.optimize do znaleznie najlepszych parametrów co mogloby by się udać przy specifycznej implemetancji.

## Dlaczego opóźnienie interwencji o 1–2 tygodnie ma nieliniowy wpływ na Imax?
W fazie wzrostu liczba zakażonych podwaja się w stałych odstępach czasu, opóźnienie 2 tygodnie tak naprawdę kilka cykli podwojenia się liczby chorych więc interwacja w dniu X + 60 nie będzie już dla np. 100 chorych ale dla 5000.

## Jak, względem modelu SIR, zmienia się przebieg epidemii, gdy w modelu SEIR występuje długi okres inkubacji?
W modelu SIR epidemia wybucha gwałtownie, osiąga wysoki wynik i spada niemal natychmiast. W modelu SEIR przez wprowadzony zbiór inkubacji, epidemia rośnie wolniej ze względu na ten nowy zbiór który będzie opóźniał przemianę osób podatnych na chore