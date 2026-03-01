from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Введите ваше имя'}),
            'email': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Введите ваш email'}),
            'message': forms.TextInput(attrs={'class': 'form-control',
                                              'placeholder': 'Введите ваше сообщение', 'rows': 5}),
        }
        labels = {
            'name': 'Имя',
            'email': 'Email',
            'message': 'Сообщение'
        }


