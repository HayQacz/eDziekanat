# Strona Edziekanatu

Strona Edziekanatu to aplikacja webowa stworzona w Django, która umożliwia studentom zarządzanie informacjami dotyczącymi ocen, rozkładem zajęć oraz ogłoszeniami. Projekt ten został zaprojektowany z myślą o usprawnieniu codziennej organizacji i komunikacji w środowisku akademickim.

## Spis treści

- [Funkcjonalności](#funkcjonalności)
  - [Zarządzanie ocenami](#zarządzanie-ocenami)
  - [Motyw graficzny](#motyw-graficzny)
  - [Plan zajęć](#plan-zajęć)
  - [Inne funkcjonalności](#inne-funkcjonalności)
- [Wymagania](#wymagania)
- [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
- [Struktura projektu](#struktura-projektu)
- [Technologie](#technologie)

## Funkcjonalności

### Zarządzanie ocenami

- **Dodawanie, edycja oraz usuwanie ocen cząstkowych:**  
  Umożliwia łatwe wprowadzanie i modyfikację ocen.
- **Automatyczne obliczanie oceny końcowej:**  
  Finalna ocena jest wyliczana z wag ocen cząstkowych. Jeśli ocena jest większa niż 2.0, naliczane są punkty ECTS za semestr.
- **Logika walidacji:**  
  Nie można dodać oceny w drugim lub trzecim terminie, jeśli nie zostały uzupełnione wcześniejsze.
- **Specjalne zasady dotyczące ocen:**  
  - Jeśli którakolwiek ocena cząstkowa wynosi 2.0, finalna ocena zostaje ustawiona na 2.0.  
  - Jeżeli któraś z ocen cząstkowych nie jest ustawiona (np. oznaczona jako "-----"), ocena końcowa nie jest obliczana.
- **Edycja ECTS oraz personalizacja interfejsu:**  
  Umożliwia ręczną korektę punktów ECTS oraz zmianę koloru wiersza dla danej oceny końcowej.

### Motyw graficzny

- **Responsywny interfejs:**  
  Bazuje na Bootstrap, co zapewnia poprawne wyświetlanie na urządzeniach mobilnych oraz desktopowych.
- **Przełącznik Dark/Light mode:**  
  Użytkownik może łatwo zmieniać motyw strony.
- **Dedykowane style dla ciemnego motywu.**

![Widok aplikacji - motyw](https://github.com/user-attachments/assets/0b934085-3b5d-474f-8f1f-bf43644b8043)
![Widok aplikacji - responsywność](https://github.com/user-attachments/assets/a7c6fc5f-21d6-44e9-a32b-e9038b2e30d0)
![Widok aplikacji - szczegóły](https://github.com/user-attachments/assets/a9eb7292-3042-4d6d-bd82-5a9b6331c406)

### Plan zajęć

- **Responsywny plan zajęć:**  
  Zapewnia przejrzysty widok aktualnego rozkładu zajęć.
- **Funkcjonalność grupowa:**  
  Użytkownik przypisany do danej grupy widzi dedykowany plan zajęć.
- **Dodawanie i usuwanie zajęć:**  
  Możliwość wprowadzania zajęć pojedynczo oraz zbiorowo, a także opcja zbiorowego usuwania.
- **Szczegółowy widok:**  
  Pozwala na przegląd, edycję i usuwanie zajęć dla poszczególnych dni.

![Plan zajęć - widok 1](https://github.com/user-attachments/assets/bfd7cd18-0e2f-4d6b-bb75-d721fbdec299)
![Plan zajęć - widok 2](https://github.com/user-attachments/assets/8e36a87a-d2f0-41b4-8ab5-b1f9230d9f49)
![Plan zajęć - widok 3](https://github.com/user-attachments/assets/273675f2-ae67-4822-a3c7-259a0021c7ac)

### Inne funkcjonalności

- **Logowanie:**  
  Zapewnia bezpieczny dostęp do systemu.
- **Strona główna:**  
  Wyświetla aktualności oraz inne istotne informacje (placeholder).
- **Ekran rozkładu zajęć:**  
  Funkcjonalność w fazie rozwoju – planowane rozszerzenie możliwości zarządzania harmonogramem.

## Wymagania

- **Python:** 3.8 lub nowszy
- **Django:** 4.x
- **Bootstrap:** 4 (wczytywany przez CDN)
- **Font Awesome:** (wczytywany przez CDN)
