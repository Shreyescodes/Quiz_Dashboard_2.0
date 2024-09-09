from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import QuizFile, QuizType, QuizQuestion

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.ModelForm):
    quiz_type_name = forms.CharField(max_length=100, help_text="Enter the name of the quiz type")

    class Meta:
        model = QuizFile
        fields = ['file', 'quiz_type_name']

class QuizTypeForm(forms.ModelForm):
    class Meta:
        model = QuizType
        fields = ['name', 'description']

class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ['question', 'option_1', 'option_2', 'option_3', 'option_4', 'correct_answer']