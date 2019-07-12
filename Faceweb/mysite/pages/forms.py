from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student
from .models import Teacher


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='User Name')
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('user name or password entered incorrectly')
        return super(LoginForm, self).clean()





class SingUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2',)


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [

            'classroom',
            'age',
            'birth_date',


        ]

class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = [

            'classroom',
            'age',
        ]