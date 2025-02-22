from django import forms
from django.contrib.auth.forms import AuthenticationForm

ROLE_CHOICES = [
    ('student', 'Student'),
    ('dydaktyk', 'Dydaktyk'),
    ('administrator', 'Administrator'),
]

class CustomAuthenticationForm(AuthenticationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, initial='student')

    def confirm_login_allowed(self, user):
        selected_role = self.cleaned_data.get('role')
        if user.role != selected_role:
            raise forms.ValidationError("Nie masz uprawnień do logowania z wybraną rolą.", code='invalid_login') 