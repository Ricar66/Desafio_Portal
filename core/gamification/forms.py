from django import forms
from .models import Challenge
from .models import User
from django.contrib.auth.forms import UserCreationForm

class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'campaign', 'points', 'is_active', 'banner', 'evaluation_rules']

class AssignChallengeForm(forms.Form):
    challenge = forms.ModelChoiceField(queryset=Challenge.objects.all())
    user_cpf = forms.CharField(max_length=14, help_text="Insira o CPF do corretor")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active']

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
      
'type': 'date'}),
        label='Data de Nascimento'
    )
    city = forms.CharField(max_length=100, required=True, label='Cidade')
    state = forms.CharField(max_length=100, required=True, label='Estado')
    cep = forms.CharField(max_length=9, required=True, label='CEP')
    street = forms.CharField(max_length=200, required=True, label='Rua')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'birth_date', 'city', 'state', 'cep', 'street']