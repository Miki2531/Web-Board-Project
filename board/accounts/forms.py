from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget= forms.EmailInput())
    class Meta:
        model =User
        fields = ('username', 'email', 'password1', 'password2')

        # widget = {
        #     'username': forms.TextInput(attrs={'class': 'form-control', 'palceholder': 'Enter  your username'}),
        #     'email': forms.EmailField(attrs={'class': 'form-control', 'palceholder': 'Enter your email'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control', 'palceholder': 'Enter your password'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control', 'palceholder': 'Enter your password'}),

        # }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})