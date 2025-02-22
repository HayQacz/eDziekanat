from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from grades.models import FinalGrade, PartialGrade
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'role', 'index_number', 'semester', 'semester_group', 'study_major', 'teaching_groups']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Student Info'), {'fields': ('index_number', 'semester', 'semester_group'), 'classes': ('collapse',)}),
        (_('Dydaktyk Info'), {'fields': ('teaching_groups',), 'classes': ('collapse',)}),
        (_('Academic info'), {'fields': ('study_major',)}),
        (_('Permissions'), {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'role', 'first_name', 'last_name', 'email', 'password1', 'password2',
                       'index_number', 'semester', 'semester_group', 'teaching_groups', 'study_major',
                       'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FinalGrade)
admin.site.register(PartialGrade)