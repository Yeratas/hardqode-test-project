from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
class User(AbstractUser):
    user_type_choices = (
        ('student','student'),
        ('instructor','instructor')
    )
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(max_length=100)
    user_type = models.CharField(max_length=20,choices=user_type_choices)
    balance = models.PositiveIntegerField(default=1000)
    
    def is_student(self):
        return self.user_type=='student'
    
    def is_instructor(self):
        return self.user_type=='instructor'
    
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now,editable=False)
    start_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)

        
    def __str__(self):
        return self.name
    
class CourseAcess(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='participants',blank=True)
    
class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    lesson_title = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    link = models.URLField()
    
    def __str__(self):
        return self.lesson_title
             
    
