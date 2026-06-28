from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if not self.user:
                raise forms.ValidationError('Invalid username or password.')
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
