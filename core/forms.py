from django.forms import CheckboxSelectMultiple
from django import forms
from django.db.models import Sum
from .models import PartialGrade, FinalGrade, FORM_CHOICES, GRADE_CHOICES, Lesson,  LESSON_TYPE_CHOICES


class PartialGradeForm(forms.ModelForm):
    class Meta:
        model = PartialGrade
        fields = ['form', 'weight', 'attempt1', 'attempt2', 'attempt3']
        widgets = {
            'form': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'attempt1': forms.Select(attrs={'class': 'form-control'}),
            'attempt2': forms.Select(attrs={'class': 'form-control'}),
            'attempt3': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.final_grade = kwargs.pop('final_grade', None)
        super().__init__(*args, **kwargs)

        self.fields['attempt2'].required = False
        self.fields['attempt3'].required = False
        original_choices_2 = [choice for choice in self.fields['attempt2'].choices if choice[0] != '']
        original_choices_3 = [choice for choice in self.fields['attempt3'].choices if choice[0] != '']
        self.fields['attempt2'].choices = [('', '--------')] + original_choices_2
        self.fields['attempt3'].choices = [('', '--------')] + original_choices_3

    def clean(self):
        cleaned_data = super().clean()
        attempt1 = cleaned_data.get('attempt1')
        attempt2 = cleaned_data.get('attempt2')
        attempt3 = cleaned_data.get('attempt3')

        if attempt2 and attempt2 != '' and not (attempt1 and attempt1 != ''):
            self.add_error('attempt2', 'Nie można ustawić oceny w drugim terminie, jeśli pierwszy termin jest pusty.')
        if attempt3 and attempt3 != '' and not (attempt2 and attempt2 != ''):
            self.add_error('attempt3', 'Nie można ustawić oceny w trzecim terminie, jeśli drugi termin jest pusty.')

        if self.final_grade is not None:
            qs = PartialGrade.objects.filter(final_grade=self.final_grade)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            existing_sum = qs.aggregate(total=Sum('weight'))['total'] or 0.0
            try:
                new_weight = float(cleaned_data.get('weight', 0.0))
            except (ValueError, TypeError):
                new_weight = 0.0
            if existing_sum + new_weight > 1.0:
                self.add_error('weight',
                               'Suma wag ocen cząstkowych nie może być większa niż 1.0. Obecnie suma wynosi {:.2f}.'.format(
                                   existing_sum + new_weight))
        return cleaned_data


class FinalGradeECTSForm(forms.ModelForm):
    class Meta:
        model = FinalGrade
        fields = ['ects']
        widgets = {
            'ects': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CombinedGradeForm(forms.Form):
    subject_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nazwa przedmiotu"
    )
    ects = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="ECTS"
    )
    form = forms.ChoiceField(
        choices=FORM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Forma zajęć"
    )
    weight = forms.FloatField(
        initial=1.0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label="Waga oceny cząstkowej"
    )
    attempt1 = forms.ChoiceField(
        choices=GRADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Ocena (próba 1)"
    )
    attempt2 = forms.ChoiceField(
        choices=[('', '--------')] + GRADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Ocena (próba 2)",
        required=False
    )
    attempt3 = forms.ChoiceField(
        choices=[('', '--------')] + GRADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Ocena (próba 3)",
        required=False
    )


class FinalGradeEditForm(forms.ModelForm):
    partial_grades = forms.ModelMultipleChoiceField(
        queryset=PartialGrade.objects.none(),
        required=False,
        widget=CheckboxSelectMultiple,
        label="Przypisane oceny cząstkowe"
    )

    class Meta:
        model = FinalGrade
        fields = ['subject_name', 'ects', 'row_color']
        widgets = {
            'subject_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ects': forms.NumberInput(attrs={'class': 'form-control'}),
            'row_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FinalGradeEditForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['partial_grades'].queryset = PartialGrade.objects.filter(final_grade__user=user)
        if self.instance.pk:
            self.fields['partial_grades'].initial = self.instance.partialgrade_set.all()

    def save(self, commit=True):
        instance = super(FinalGradeEditForm, self).save(commit)
        selected = self.cleaned_data.get('partial_grades')
        if not selected:
            instance.delete()
        else:
            for pg in self.fields['partial_grades'].queryset:
                if pg in selected:
                    if pg.final_grade != instance:
                        pg.final_grade = instance
                        pg.save()
        return instance
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['final_grade', 'date', 'start_time', 'end_time', 'lesson_type', 'mandatory', 'additional_info', 'group']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['final_grade'].queryset = user.finalgrade_set.all()


class BulkLessonForm(forms.Form):
    final_grade = forms.ModelChoiceField(queryset=FinalGrade.objects.none(), label="Przedmiot")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data początkowa")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data końcowa")
    day_of_week = forms.ChoiceField(choices=[
        ('0', 'Poniedziałek'),
        ('1', 'Wtorek'),
        ('2', 'Środa'),
        ('3', 'Czwartek'),
        ('4', 'Piątek'),
        ('5', 'Sobota'),
        ('6', 'Niedziela'),
    ], label="Dzień tygodnia")
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Godzina rozpoczęcia")
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Godzina zakończenia")
    lesson_type = forms.ChoiceField(choices=LESSON_TYPE_CHOICES, label="Forma zajęć")
    mandatory = forms.BooleanField(initial=True, required=False, label="Obowiązkowe")
    additional_info = forms.CharField(widget=forms.Textarea, required=False, label="Dodatkowe informacje")
    group = forms.CharField(max_length=2, label="Grupa")
    every_two_weeks = forms.BooleanField(required=False, label="Co dwa tygodnie")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BulkLessonForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['final_grade'].queryset = user.finalgrade_set.all()

class BulkLessonDeleteForm(forms.Form):
    final_grade = forms.ModelChoiceField(queryset=FinalGrade.objects.none(), label="Przedmiot")
    lesson_type = forms.ChoiceField(choices=LESSON_TYPE_CHOICES, label="Forma zajęć")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data początkowa")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Data końcowa")
    day_of_week = forms.ChoiceField(choices=[
        ('0', 'Poniedziałek'),
        ('1', 'Wtorek'),
        ('2', 'Środa'),
        ('3', 'Czwartek'),
        ('4', 'Piątek'),
        ('5', 'Sobota'),
        ('6', 'Niedziela'),
    ], label="Dzień tygodnia")
    every_two_weeks = forms.BooleanField(required=False, label="Co dwa tygodnie")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BulkLessonDeleteForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['final_grade'].queryset = user.finalgrade_set.all()