from django import forms
from django.contrib.auth.models import User
from .models import Team, TeamMembership

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password should be at least 8 characters long.")
        return password

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'manager', 'company']

class TeamMembershipForm(forms.ModelForm):
    class Meta:
        model = TeamMembership
        fields = ['user', 'role', 'team']