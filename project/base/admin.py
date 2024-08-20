from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Lesson, CourseAcess

admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseAcess)
