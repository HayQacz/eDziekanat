from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FinalGrade, PartialGrade

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'index_number', 'semester', 'study_major']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('index_number', 'semester', 'study_major')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FinalGrade)
admin.site.register(PartialGrade)
