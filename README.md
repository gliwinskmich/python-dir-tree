# Analiza struktury katalogu

Skrypt do wyświetlania struktury katalogów w formie drzewa z informacjami o rozmiarach plików oraz statystykami rozszerzeń.

## Opis
Skrypt rekurencyjnie przeszukuje wskazany katalog, wyświetlając jego strukturę w formie drzewa. Dla każdego podkatalogu pokazuje całkowity rozmiar, a dla każdego pliku - jego indywidualny rozmiar. Na końcu generuje statystyki dotyczące liczby plików według rozszerzeń.

## Funkcje
1. Wyświetlanie struktury katalogów w formie drzewa
2. Obliczanie i wyświetlanie rozmiarów:
3. Całkowity rozmiar każdego podkatalogu
4. Rozmiar każdego pliku
5. Automatyczne formatowanie rozmiarów (B, KB, MB, GB, TB, PB)
6. Grupowanie plików według rozszerzeń
7. Obsługa błędów dostępu do plików
8. Sortowanie elementów (katalogi najpierw, potem pliki)
9. Obsługa dowiązań symbolicznych (pomijane)

## Wymagania
Python 3.6 lub nowszy

## Użycie

Podstawowe użycie
```bash
python dirtree.py [ścieżka]
```
## Przykłady użycia i wyniku

Wyświetlenie struktury bieżącego katalogu:

```bash
python dirtree.py
```

Wyświetlenie struktury wskazanego katalogu:

```bash
python dirtree.py /home/user/temp
```

Wyświetlenie struktury katalogu z Windows:

```bash
python dirtree.py "C:\Users\NazwaUżytkownika\Documents"
```

Przykładowy wynik

```bash
$ python3 dirtree.py /home/user/Katalog

------------------------------------------------------------
Struktura katalogu: /home/user/Katalog
------------------------------------------------------------
Katalog (1.24 MB)
├── [DIR] Cyberbezpieczeństwo (1.10 MB)
│   ├── Cyber_1.pdf (403.78 KB)
│   ├── Cyber_2.pdf (244.91 KB)
│   ├── Cyber_3.pdf (241.17 KB)
│   └── Cyber_4.pdf (236.44 KB)
└── [DIR] Temp (145.62 KB)
    ├── spaCy.ipynb (54.95 KB)
    ├── spy.py (4.60 KB)
    ├── Untitled.ipynb (81.67 KB)
    ├── Untitled1.ipynb (72.00 B)
    ├── Untitled2.ipynb (72.00 B)
    └── Untitled3.ipynb (4.26 KB)

---------------------------------------------
Pliki wg. kategorii w całej strukturze:
---------------------------------------------
  .ipynb               : 10
  .pdf                 : 8
  .py                  : 2

```
