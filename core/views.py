import datetime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import FinalGrade, PartialGrade, Lesson
from django.db.models import Sum
from .forms import PartialGradeForm, FinalGradeECTSForm, CombinedGradeForm, FinalGradeEditForm, LessonForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

@login_required
def home(request):
    news = [
        {'title': 'Aktualność 1', 'content': 'Treść aktualności 1...'},
        {'title': 'Aktualność 2', 'content': 'Treść aktualności 2...'},
    ]
    return render(request, 'home.html', {'news': news})

@login_required
def schedule(request):
    return render(request, 'schedule.html')


@login_required
def grades(request):
    final_grades = FinalGrade.objects.filter(user=request.user)
    simple_grades = []
    weighted_sum = 0
    ects_sum = 0
    for fg in final_grades:
        fg.weight_sum = fg.partialgrade_set.aggregate(total=Sum('weight'))['total'] or 0.0

        try:
            if fg.final_value != 'zal':
                grade_value = float(fg.final_value)
            else:
                grade_value = 0
        except ValueError:
            grade_value = 0
        if grade_value > 2.0:
            simple_grades.append(grade_value)
            weighted_sum += grade_value * fg.ects
            ects_sum += fg.ects
    simple_avg = sum(simple_grades) / len(simple_grades) if simple_grades else 0
    weighted_avg = weighted_sum / ects_sum if ects_sum else 0
    context = {
        'final_grades': final_grades,
        'simple_avg': round(simple_avg, 2),
        'weighted_avg': round(weighted_avg, 2),
    }
    return render(request, 'grades.html', context)

@login_required
def update_color(request):
    if request.method == 'POST':
        final_grade_id = request.POST.get('final_grade_id')
        color = request.POST.get('color')
        final_grade = get_object_or_404(FinalGrade, id=final_grade_id, user=request.user)
        final_grade.row_color = color
        final_grade.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_partial_grade(request, final_grade_id):
    final_grade = get_object_or_404(FinalGrade, id=final_grade_id, user=request.user)
    if request.method == 'POST':
        form = PartialGradeForm(request.POST, final_grade=final_grade)
        if form.is_valid():
            new_form = form.cleaned_data['form']
            if final_grade.partialgrade_set.filter(form=new_form).exists():
                form.add_error('form', 'Ocena z tą formą już istnieje dla tego przedmiotu.')
                return render(request, 'add_partial_grade.html', {'form': form, 'final_grade': final_grade})
            partial = form.save(commit=False)
            partial.final_grade = final_grade
            partial.save()
            return redirect('grades')
    else:
        form = PartialGradeForm(final_grade=final_grade)
    return render(request, 'add_partial_grade.html', {'form': form, 'final_grade': final_grade})

@login_required
def edit_partial_grade(request, partial_id):
    partial = get_object_or_404(PartialGrade, id=partial_id, final_grade__user=request.user)
    if request.method == 'POST':
        form = PartialGradeForm(request.POST, instance=partial, final_grade=partial.final_grade)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = PartialGradeForm(instance=partial, final_grade=partial.final_grade)
    return render(request, 'edit_partial_grade.html', {'form': form, 'partial': partial})

@login_required
def delete_partial_grade(request, partial_id):
    partial = get_object_or_404(PartialGrade, id=partial_id, final_grade__user=request.user)
    partial.delete()
    return redirect('grades')

@login_required
def set_ects(request, final_grade_id):
    final_grade = get_object_or_404(FinalGrade, id=final_grade_id, user=request.user)
    if request.method == 'POST':
        form = FinalGradeECTSForm(request.POST, instance=final_grade)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = FinalGradeECTSForm(instance=final_grade)
    return render(request, 'edit_ects.html', {'form': form, 'final_grade': final_grade})

@login_required
def edit_final_grade(request, final_grade_id):
    final_grade = get_object_or_404(FinalGrade, id=final_grade_id, user=request.user)
    if request.method == 'POST':
        form = FinalGradeEditForm(request.POST, instance=final_grade, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('grades')
    else:
        form = FinalGradeEditForm(instance=final_grade, user=request.user)
    return render(request, 'edit_final_grade.html', {'form': form, 'final_grade': final_grade})

@login_required
def add_combined_grade(request):
    if request.method == 'POST':
        form = CombinedGradeForm(request.POST)
        if form.is_valid():
            final_grade = FinalGrade.objects.create(
                user=request.user,
                subject_name=form.cleaned_data['subject_name'],
                ects=form.cleaned_data['ects'],
                final_value=''
            )
            PartialGrade.objects.create(
                final_grade=final_grade,
                form=form.cleaned_data['form'],
                weight=form.cleaned_data['weight'],
                attempt1=form.cleaned_data['attempt1'],
                attempt2=form.cleaned_data['attempt2'],
                attempt3=form.cleaned_data['attempt3'],
            )
            return redirect('grades')
    else:
        form = CombinedGradeForm()
    return render(request, 'add_combined_grade.html', {'form': form})
def custom_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Nie udało się zalogować, błędny indeks lub hasło."
    return render(request, 'login.html', {'error_message': error_message})
def schedule_week(request):
    # Pobranie daty z parametrów GET lub użycie dzisiejszej daty
    date_str = request.GET.get('date')
    if date_str:
        try:
            current_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            current_date = datetime.date.today()
    else:
        current_date = datetime.date.today()

    # Obliczenie poniedziałku bieżącego tygodnia
    start_of_week = current_date - datetime.timedelta(days=current_date.weekday())
    week_dates = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

    # Filtrowanie zajęć na podstawie grupy użytkownika
    lessons = Lesson.objects.filter(group=request.user.semester_group)
    # Grupujemy zajęcia według dnia tygodnia (0: Poniedziałek, … 6: Niedziela)
    lessons_by_day = {i: [] for i in range(7)}
    for lesson in lessons:
        lessons_by_day[lesson.day_of_week].append(lesson)

    context = {
        'week_dates': week_dates,
        'lessons_by_day': lessons_by_day,
        'start_of_week': start_of_week,
        'end_of_week': start_of_week + datetime.timedelta(days=6),
        'previous_week': start_of_week - datetime.timedelta(days=7),
        'next_week': start_of_week + datetime.timedelta(days=7),
    }
    return render(request, 'schedule_week.html', context)

def schedule_day(request, day):
    # 'day' w formacie YYYY-MM-DD
    try:
        day_date = datetime.datetime.strptime(day, '%Y-%m-%d').date()
    except ValueError:
        day_date = datetime.date.today()
    weekday = day_date.weekday()  # 0: Poniedziałek, ... 6: Niedziela

    lessons = Lesson.objects.filter(group=request.user.semester_group, day_of_week=weekday)
    context = {
        'day_date': day_date,
        'lessons': lessons,
    }
    return render(request, 'schedule_day.html', context)

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'schedule_form.html'
    success_url = reverse_lazy('schedule_week')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'schedule_form.html'
    success_url = reverse_lazy('schedule_week')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = 'schedule_confirm_delete.html'
    success_url = reverse_lazy('schedule_week')