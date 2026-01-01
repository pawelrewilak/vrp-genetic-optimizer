# Cleaning Service VRP Optimizer 🧹

Aplikacja webowa do optymalizacji pracy ekip sprzątających (problem VRPTW). Projekt wykorzystuje **algorytm genetyczny**, aby zmaksymalizować zysk firmy.

Program pomaga podjąć decyzję: **ile ekip zatrudnić danego dnia i jak ułożyć im trasę**, aby przychód ze zleceń był jak najwyższy po odjęciu kosztów (dniówki pracowników, paliwo).

## 📌 Co robi ten projekt?
* **Optymalizacja Zysku:** Funkcja celu to `Przychód - (Koszt Ekip + Paliwo)`. Algorytm sam decyduje, czy opłaca się wysłać auto do dalekiego klienta.
* **Wizualizacja mapy:** Rysowanie tras poszczególnych ekip na canvasie HTML5.
* **Realne koszty:** Przeliczanie odległości na mapie na czas pracy i zużycie paliwa.
* **Wykresy na żywo:** Podgląd ewolucji rozwiązania i wzrostu zysku w czasie rzeczywistym.
* **Konfiguracja:** Możliwość zmiany parametrów algorytmu (mutacje, krzyżowanie) oraz kosztów zatrudnienia.

## 🛠 Technologie
* **Backend:** Python 3 + Flask
* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Algorytmy:** Własna implementacja algorytmu genetycznego (Python)

## 🚀 Jak uruchomić?

1. Sklonuj repozytorium:
   ```bash
   git clone [https://github.com/TWOJ-NICK/cleaning-vrp.git](https://github.com/TWOJ-NICK/cleaning-vrp.git)