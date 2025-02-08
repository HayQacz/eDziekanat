# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),
    path('grades/', views.grades, name='grades'),
    path('update_color/', views.update_color, name='update_color'),
    path('grades/add/<int:final_grade_id>/', views.add_partial_grade, name='add_partial_grade'),
    path('grades/edit/<int:partial_id>/', views.edit_partial_grade, name='edit_partial_grade'),
    path('grades/delete/<int:partial_id>/', views.delete_partial_grade, name='delete_partial_grade'),
    path('grades/set_ects/<int:final_grade_id>/', views.set_ects, name='set_ects'),
    path('grades/edit_final/<int:final_grade_id>/', views.edit_final_grade, name='edit_final_grade'),
    path('grades/add_combined_grade/', views.add_combined_grade, name='add_combined_grade'),
]
