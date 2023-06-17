from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import datetime


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['index', 'question', 'answer']
        widgets = {
            'index': forms.TextInput(attrs={'class': 'form-control'}),
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control'})
        }
