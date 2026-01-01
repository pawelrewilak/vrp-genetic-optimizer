# VRP Genetic Solver 🚚

Prosta aplikacja webowa do rozwiązywania problemu trasowania pojazdów z oknami czasowymi (VRPTW). Projekt wykorzystuje **algorytm genetyczny** do optymalizacji tras autobusów szkolnych, uwzględniając zyski, koszty paliwa i czas pracy kierowców.

## 📌 Co potrafi ten projekt?
* **Wizualizacja mapy:** Rysowanie tras i punktów (szkół) na canvasie HTML5.
* **Wykresy na żywo:** Podgląd, jak algorytm "uczy się" z każdym pokoleniem (wykorzystuje Chart.js).
* **Konfiguracja GA:** Możliwość zmiany wielkości populacji, liczby iteracji oraz metod mutacji (Swap, Inversion, Scramble) i krzyżowania.
* **Symulacja kosztów:** Realne przeliczanie odległości na mapie na czas i koszt paliwa.
* **Generator:** Szybkie losowanie punktów do testów.

## 🛠 Technologie
* **Backend:** Python 3 + Flask
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Algorytmy:** Własna implementacja algorytmu genetycznego (Python)

## 🚀 Jak uruchomić?

1. Sklonuj repozytorium:
   ```bash
   git clone [https://github.com/TWOJ-NICK/vrp-solver.git](https://github.com/TWOJ-NICK/vrp-solver.git)