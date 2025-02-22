from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from grades.models import FinalGrade, PartialGrade
from django.db.models import Sum
from grades.forms import PartialGradeForm, FinalGradeECTSForm, CombinedGradeForm, FinalGradeEditForm
from django.shortcuts import render, get_object_or_404, redirect

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