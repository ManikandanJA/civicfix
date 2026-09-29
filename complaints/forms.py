from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Complaint


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category', 'location', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Streetlight not working'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Area / street name'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'resolution_photo']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'resolution_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
