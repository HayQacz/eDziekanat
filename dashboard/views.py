from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    news = [
        {'title': 'Aktualność 1', 'content': 'Treść aktualności 1...'},
        {'title': 'Aktualność 2', 'content': 'Treść aktualności 2...'},
    ]
    return render(request, 'home.html', {'news': news})