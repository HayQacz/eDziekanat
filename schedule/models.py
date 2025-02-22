from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from grades.models import FinalGrade

LESSON_TYPE_CHOICES = [
    ('wyklad', 'Wykład'),
    ('laboratoria', 'Laboratoria'),
    ('audytoria', 'Audytoria'),
    ('kolokwium', 'Kolokwium'),
    ('kolokwium poprawkowe', 'Kolokwium poprawkowe'),
    ('zaliczenie', 'Zaliczenie'),
    ('zaliczenie poprawkowe', 'Zaliczenie poprawkowe'),
    ('odwolane', 'Odwołane'),
]

class Lesson(models.Model):
    final_grade = models.ForeignKey(FinalGrade, on_delete=models.CASCADE, help_text="Przedmiot (ocena) dla zajęć")
    date = models.DateField(help_text="Data zajęć")
    start_time = models.TimeField(help_text="Godzina rozpoczęcia")
    end_time = models.TimeField(help_text="Godzina zakończenia")
    lesson_type = models.CharField(max_length=30, choices=LESSON_TYPE_CHOICES, help_text="Forma zajęć")
    mandatory = models.BooleanField(default=True, help_text="Czy zajęcia są obowiązkowe")
    additional_info = models.TextField(blank=True, help_text="Dodatkowe informacje")
    group = models.CharField(max_length=2, help_text="Grupa, dwucyfrowy kod")
    room = models.CharField(
        max_length=3,
        help_text="Sala (3-cyfrowa)",
        validators=[RegexValidator(regex=r'^\d{3}$', message='Podaj 3-cyfrową salę')]
    )

    def __str__(self):
        return f"{self.final_grade.subject_name} - {self.get_lesson_type_display()} w dniu {self.date} ({self.start_time}-{self.end_time}) - Sala: {self.room}"
