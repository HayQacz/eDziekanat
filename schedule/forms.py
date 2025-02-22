from django import forms
from schedule.models import Lesson, LESSON_TYPE_CHOICES
from grades.models import FinalGrade


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['final_grade', 'date', 'start_time', 'end_time', 'lesson_type', 'mandatory', 'additional_info', 'group', 'room']
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
    room = forms.CharField(max_length=3, label="Sala")
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
