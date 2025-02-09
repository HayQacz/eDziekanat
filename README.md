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
![image](https://github.com/user-attachments/assets/0b934085-3b5d-474f-8f1f-bf43644b8043)
![image](https://github.com/user-attachments/assets/a7c6fc5f-21d6-44e9-a32b-e9038b2e30d0)
![image](https://github.com/user-attachments/assets/a9eb7292-3042-4d6d-bd82-5a9b6331c406)


-**Plan zajęć:**
  -W pełni responsywny plan zajęć. 
  -Funkcjonalność grupowa - użytkownik z przypisaną daną grupą będzie widział plan zajęć
  -Funkcja dodawania pojedynczo jak i zbiorowo zajęć. Dodana również została możliwość zbiorowego usuwania zajęć.
  -Możliwość wejścia w widok poszczególnych dni zajęć - możliwość edycji i usunięcia poszczególnych zajęć dla całej grupy. 
![image](https://github.com/user-attachments/assets/bfd7cd18-0e2f-4d6b-bb75-d721fbdec299)
![image](https://github.com/user-attachments/assets/8e36a87a-d2f0-41b4-8ab5-b1f9230d9f49)
![image](https://github.com/user-attachments/assets/273675f2-ae67-4822-a3c7-259a0021c7ac)


- **Inne funkcjonalności:**
  - Strona logowania. 
  - Strona główna z aktualnościami (placeholder).

## Wymagania
- Python 3.8 lub nowszy
- Django 4.x
- Bootstrap 4 (wczytywany przez CDN)
- Font Awesome (wczytywany przez CDN)



