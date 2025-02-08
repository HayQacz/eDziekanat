from django.urls import path
from . import views
from .views import schedule_week, schedule_day, LessonCreateView, LessonUpdateView, LessonDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/week/', schedule_week, name='schedule_week'),
    path('schedule/day/<str:day>/', schedule_day, name='schedule_day'),
    path('schedule/lesson/add/', LessonCreateView.as_view(), name='lesson_add'),
    path('schedule/lesson/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    path('schedule/lesson/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('grades/', views.grades, name='grades'),
    path('update_color/', views.update_color, name='update_color'),
    path('grades/add/<int:final_grade_id>/', views.add_partial_grade, name='add_partial_grade'),
    path('grades/edit/<int:partial_id>/', views.edit_partial_grade, name='edit_partial_grade'),
    path('grades/delete/<int:partial_id>/', views.delete_partial_grade, name='delete_partial_grade'),
    path('grades/set_ects/<int:final_grade_id>/', views.set_ects, name='set_ects'),
    path('grades/edit_final/<int:final_grade_id>/', views.edit_final_grade, name='edit_final_grade'),
    path('grades/add_combined_grade/', views.add_combined_grade, name='add_combined_grade'),
    path('bulk/lesson/add/', views.bulk_lesson_add, name='bulk_lesson_add'),
    path('bulk/lesson/delete/', views.bulk_lesson_delete, name='bulk_lesson_delete'),
]
