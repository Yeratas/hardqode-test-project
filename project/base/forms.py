from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Course, Lesson

from .models import User

class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(max_length=100)
    
    class Meta:
        model = User
        fields = ['username','email','user_type','password1','password2']
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already exists")
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Username {username} is already exists")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removing password-based authentication
        if 'usable_password' in self.fields:
            del self.fields['usable_password']
            
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name','description','start_date','price']
        
class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ['lesson_title','link']