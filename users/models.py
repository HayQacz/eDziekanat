from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    index_number = models.CharField(max_length=7, unique=True, help_text="np. AB12345")
    semester = models.PositiveIntegerField(default=1, help_text="Aktualny semestr (np. 1, 2, 3, ...)")
    study_major = models.CharField(max_length=100, help_text="Kierunek studiów")
    semester_group = models.CharField(max_length=2, help_text="Dwucyfrowy kod grupy (np. 10, 21)")

    @property
    def total_ects(self):
        total = 0
        for fg in self.finalgrade_set.all():
            if fg.final_value and fg.final_value not in ('', 'zal'):
                try:
                    if float(fg.final_value) > 2.0:
                        total += fg.ects
                except ValueError:
                    pass
        return total

    @property
    def max_possible_ects(self):
        return sum(fg.ects for fg in self.finalgrade_set.all())

    def __str__(self):
        return f"{self.username} ({self.index_number}) - Semestr: {self.semester}, Grupa: {self.semester_group}"
