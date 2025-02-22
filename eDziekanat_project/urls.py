from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.forms import CustomAuthenticationForm
from users.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm, template_name='login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('', include('grades.urls')),
    path('', include('schedule.urls')),
    path('', include('dashboard.urls')),
]
