# Strona Edziekanatu

Strona Edziekanatu to aplikacja webowa stworzona w Django, umożliwiająca studentom zarządzanie informacjami dotyczącymi ocen, rozkładem zajęć oraz ogłoszeniami. Aplikacja zawiera m.in.:

- **Zarządzanie ocenami:** 
  - Dodawanie, edycja oraz usuwanie ocen cząstkowych.
  - Automatyczna funkcjonalność oceny końcowej - jest obliczana z wag ocen cząstkowych, kiedy ocena jest większa niż 2.0 to naliczane są punkty ECTS za semestr
  - Logika walidacji: nie można dodać oceny w drugim lub trzecim terminie, jeśli nie są uzupełnione wcześniejsze.
  - Specjalne zasady dotyczące ocen (np. jeśli którakolwiek ocena cząstkowa to 2.0, finalna ocena zostaje ustawiona na 2.0).
  - Jeżeli któraś z ocen cząstkowych nie jest ustawiona (-----), to ocena finalna nie jest naliczana.
  - Możliwość edycji ECTS za ocenę końcową, możliwość zmiany koloru wiersza dla danej oceny końcowej. 

- **Motyw graficzny:** 
  - Responsywny interfejs oparty o Bootstrap.
  - Przełącznik Dark/Light mode dostępny w pasku nawigacyjnym.
  - Dedykowane style dla ciemnego motywu.
    ![image](https://github.com/user-attachments/assets/3b17e801-ce38-4e60-8600-38ae220c715f)
    ![image](https://github.com/user-attachments/assets/bfab063c-c45c-48ff-b1b8-1c8841a9c4d6)
    ![image](https://github.com/user-attachments/assets/41eb6f16-b3b2-412b-bf61-9adc9eea6891)


- **Inne funkcjonalności:**
  - Strona logowania. 
  - Strona główna z aktualnościami (placeholder).
  - Ekran rozkładu zajęć (placeholder).

## Wymagania
- Python 3.8 lub nowszy
- Django 4.x
- Bootstrap 4 (wczytywany przez CDN)
- Font Awesome (wczytywany przez CDN)



