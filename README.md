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
![image](https://github.com/user-attachments/assets/60c8c799-bb0b-422d-837f-e23c444ebbe6)
![image](https://github.com/user-attachments/assets/6ce4d21c-1be9-4a8a-946e-e39e9f0965fb)
![image](https://github.com/user-attachments/assets/cbb363d5-8c31-497f-91ed-587d0390ed6e)



- **Inne funkcjonalności:**
  - Strona logowania. 
  - Strona główna z aktualnościami (placeholder).
  - Ekran rozkładu zajęć (placeholder).

## Wymagania
- Python 3.8 lub nowszy
- Django 4.x
- Bootstrap 4 (wczytywany przez CDN)
- Font Awesome (wczytywany przez CDN)



