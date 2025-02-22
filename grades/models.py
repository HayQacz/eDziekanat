from django.db import models
from users.models import CustomUser

GRADE_CHOICES = [
    ('', '-----'),
    ('2.0', '2.0'),
    ('3.0', '3.0'),
    ('3.5', '3.5'),
    ('4.0', '4.0'),
    ('4.5', '4.5'),
    ('5.0', '5.0'),
    ('zal', 'zal'),
]

FORM_CHOICES = [
    ('audytoria', 'Audytoria'),
    ('laboratoria', 'Laboratoria'),
    ('wyklad', 'Wykład'),
]

class FinalGrade(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=200)
    ects = models.FloatField(help_text="Podaj ECTS przedmiotu przy tworzeniu pierwszej oceny cząstkowej")
    final_value = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES,
        blank=True,
        help_text="Wartość wyliczana na podstawie ocen cząstkowych"
    )
    row_color = models.CharField(
        max_length=20,
        default='',
        help_text="Kolor wiersza w formacie hex (np. #ffffff)",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.subject_name

    def max_ects(self):
        return self.ects

    def update_final_value(self):
        partials = self.partialgrade_set.all()
        if not partials.exists():
            self.final_value = ''
            self.save()
            return

        latest_grade = None
        latest_attempt = None
        latest_pg = None

        for pg in partials:
            if pg.attempt3:
                latest_grade = pg.attempt3
                latest_attempt = 'attempt3'
                latest_pg = pg
            elif pg.attempt2:
                latest_grade = pg.attempt2
                latest_attempt = 'attempt2'
                latest_pg = pg
            elif pg.attempt1:
                latest_grade = pg.attempt1
                latest_attempt = 'attempt1'
                latest_pg = pg

            if latest_grade == 'zal':
                self.final_value = 'zal'
                self.save()
                return

        if not latest_grade:
            self.final_value = ''
            self.save()
            return

        if latest_grade == '2.0' or (
                latest_attempt == 'attempt2' and not partials.filter(attempt3__isnull=False).exists()
        ) or (
                latest_attempt == 'attempt1' and not partials.filter(attempt2__isnull=False).exists()
        ):
            self.final_value = '2.0'
            self.save()
            return

        valid_partials = [pg for pg in partials if (pg.attempt1 or pg.attempt2 or pg.attempt3)]

        total_weight_sum = sum(pg.weight for pg in valid_partials)
        if abs(total_weight_sum - 1.0) > 0.001:
            self.final_value = ''
            self.save()
            return

        total_weight = 0.0
        weighted_sum = 0.0
        for pg in valid_partials:
            grade_value = None
            if pg.attempt3 and pg == latest_pg:
                grade_value = pg.attempt3
            elif pg.attempt2 and pg == latest_pg:
                grade_value = pg.attempt2
            elif pg.attempt1 and pg == latest_pg:
                grade_value = pg.attempt1

            if grade_value and grade_value != 'zal':
                try:
                    numeric_grade = float(grade_value)
                except ValueError:
                    numeric_grade = 0.0
                weighted_sum += numeric_grade * pg.weight
                total_weight += pg.weight

        if total_weight > 0:
            avg = weighted_sum / total_weight
            rounded_avg = round(avg * 2) / 2
            if rounded_avg < 2.0:
                rounded_avg = 2.0
            elif rounded_avg > 5.0:
                rounded_avg = 5.0
            self.final_value = f"{rounded_avg:.1f}"
        else:
            self.final_value = ''

        self.save()


class PartialGrade(models.Model):
    final_grade = models.ForeignKey(FinalGrade, on_delete=models.CASCADE)
    form = models.CharField(max_length=20, choices=FORM_CHOICES)
    weight = models.FloatField(default=1.0, help_text="Waga oceny cząstkowej")
    attempt1 = models.CharField(max_length=10, choices=GRADE_CHOICES, blank=True)
    attempt2 = models.CharField(max_length=10, choices=GRADE_CHOICES, blank=True)
    attempt3 = models.CharField(max_length=10, choices=GRADE_CHOICES, blank=True)

    class Meta:
        unique_together = ('final_grade', 'form')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.final_grade.update_final_value()

    def delete(self, *args, **kwargs):
        final = self.final_grade
        super().delete(*args, **kwargs)
        if final.partialgrade_set.exists():
            final.update_final_value()
        else:
            final.delete()

    def __str__(self):
        return f"{self.get_form_display()} - Waga: {self.weight}"