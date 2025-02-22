from django.urls import path
from schedule import views
from schedule.views import schedule_week, schedule_day, LessonCreateView, LessonUpdateView, LessonDeleteView

urlpatterns = [
    path('schedule/week/', schedule_week, name='schedule_week'),
    path('schedule/day/<str:day>/', schedule_day, name='schedule_day'),
    path('schedule/lesson/add/', LessonCreateView.as_view(), name='lesson_add'),
    path('schedule/lesson/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    path('schedule/lesson/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('bulk/lesson/add/', views.bulk_lesson_add, name='bulk_lesson_add'),
    path('bulk/lesson/delete/', views.bulk_lesson_delete, name='bulk_lesson_delete'),
]
