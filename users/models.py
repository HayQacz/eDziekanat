from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

ROLE_CHOICES = [
    ('student', 'Student'),
    ('dydaktyk', 'Dydaktyk'),
    ('administrator', 'Administrator'),
]

class CustomUser(AbstractUser):
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='student', blank=True, null=True)

    # Pola studenckie
    index_number = models.CharField(max_length=7, unique=True, help_text="np. AB12345", blank=True, null=True)
    semester = models.PositiveIntegerField(default=1, help_text="Aktualny semestr (np. 1, 2, 3, ...)", blank=True, null=True)
    semester_group = models.CharField(max_length=2, help_text="Dwucyfrowy kod grupy (np. 10, 21)", blank=True, null=True)

    # Pole dla dydaktyka
    teaching_groups = models.CharField(max_length=255, blank=True, null=True, help_text="Lista grup, w których nauczasz (oddzielone przecinkami)")

    study_major = models.CharField(max_length=100, help_text="Kierunek studiów")

    def clean(self):
        super().clean()
        if self.role == 'student':
            if not self.index_number:
                raise ValidationError({'index_number': 'Numer indeksu jest wymagany dla studenta.'})
            if self.semester is None:
                raise ValidationError({'semester': 'Semestr jest wymagany dla studenta.'})
            if not self.semester_group:
                raise ValidationError({'semester_group': 'Grupa jest wymagana dla studenta.'})

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
        if self.role == 'student':
            return f"{self.username} ({self.index_number}) - Semestr: {self.semester}, Grupa: {self.semester_group}"
        elif self.role == 'dydaktyk':
            return f"{self.username} (Dydaktyk) - Grupy: {self.teaching_groups}"
        else:
            return f"{self.username} (Administrator)"
