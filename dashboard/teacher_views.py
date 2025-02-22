from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from users.models import CustomUser

# Przykładowe przypisania dla dydaktyka
assignments = [
    {'id': 1, 'subject': 'Matematyka', 'group': '10', 'form': 'Wykład'},
    {'id': 2, 'subject': 'Fizyka', 'group': '11', 'form': 'Laboratoria'},
]

@login_required
def teacher_groups(request):
    # W realnej aplikacji pobieramy przypisania na podstawie request.user
    context = {'assignments': assignments}
    return render(request, 'teacher/teacher_groups.html', context)

@login_required
def teacher_group_detail(request, assignment_id):
    assignment = next((a for a in assignments if a['id'] == int(assignment_id)), None)
    if not assignment:
        from django.http import Http404
        raise Http404("Assignment not found")
    # Pobieramy uczniów należących do danej grupy (przyjmujemy, że pole semester_group przechowuje kod grupy)
    students = CustomUser.objects.filter(semester_group=assignment['group'])

    if request.method == 'POST':
        student_id = request.POST.get('save_student')
        student = get_object_or_404(CustomUser, id=student_id)
        grade1 = request.POST.get(f"grade_{student.id}_1", "").strip()
        grade2 = request.POST.get(f"grade_{student.id}_2", "").strip()
        grade3 = request.POST.get(f"grade_{student.id}_3", "").strip()
        errors = []

        if grade1 == "" and (grade2 or grade3):
            errors.append("Najpierw uzupełnij pierwszy termin.")
        if grade1 and (not grade2) and grade3:
            errors.append("Najpierw uzupełnij drugi termin, aby możliwe było wprowadzenie trzeciej oceny.")

        try:
            if grade1 and grade1 != "zal":
                grade1_val = float(grade1)
            else:
                grade1_val = None
        except ValueError:
            errors.append("Niepoprawna wartość dla pierwszego terminu.")

        if grade1_val is not None and grade1_val > 2.0:
            if grade2 or grade3:
                errors.append("Ocena z pierwszego terminu wskazuje brak możliwości wprowadzenia kolejnych ocen.")
        if grade1 == "zal":
            if grade2 or grade3:
                errors.append("Ocena 'zal' we wcześniejszym terminie uniemożliwia wprowadzenie kolejnych ocen.")

        try:
            if grade2 and grade2 != "zal":
                grade2_val = float(grade2)
            else:
                grade2_val = None
        except ValueError:
            errors.append("Niepoprawna wartość dla drugiego terminu.")

        if grade2_val is not None and grade2_val > 2.0:
            if grade3:
                errors.append("Ocena z drugiego terminu wskazuje brak możliwości wprowadzenia trzeciej oceny.")
        if grade2 == "zal":
            if grade3:
                errors.append("Ocena 'zal' w drugim terminie uniemożliwia wprowadzenie trzeciej oceny.")

        if errors:
            context = {
                'assignment': assignment,
                'students': students,
                'errors': errors,
            }
            return render(request, 'teacher/teacher_group_detail.html', context)
        else:
            # W rzeczywistej aplikacji zapisujemy oceny do bazy, tutaj symulujemy zapis
            context = {
                'assignment': assignment,
                'students': students,
                'success': f"Oceny dla ucznia {student.first_name} {student.last_name} zostały zapisane.",
            }
            return render(request, 'teacher/teacher_group_detail.html', context)

    context = {
        'assignment': assignment,
        'students': students,
    }
    return render(request, 'teacher/teacher_group_detail.html', context) 