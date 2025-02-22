from django.urls import path
from dashboard import views
from . import teacher_views


urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/groups/', teacher_views.teacher_groups, name='teacher_groups'),
    path('teacher/group/<int:assignment_id>/', teacher_views.teacher_group_detail, name='teacher_group_detail'),
]