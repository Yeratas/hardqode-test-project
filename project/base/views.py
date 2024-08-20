from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import User, Course, Lesson, CourseAcess
from .forms import RegistrationForm, CourseForm, LessonForm
from django.contrib import messages

# Create your views here.
def home_view(request):
    courses = Course.objects.all()
    context = {'courses':courses}
    return render(request,'home.html',context)

def user_view(request,id):
    user = User.objects.get(id=id)
    all_courses = Course.objects.all()
    username = user.username
    email = user.email
    user_type = user.user_type
    balance = user.balance
    all_access = CourseAcess.objects.filter(participants = user)
    course_access_list = []

    for course in all_courses:
        for access in all_access:
            if course.id == access.course_id:
                course_access_list.append(course.name)
    context = {
        'user':user,
        'username':username,
        'email':email,  
        'user_type':user_type,
        'balance':balance,
        'course_access_list':course_access_list
    }
    return render(request, 'user.html',context)

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Somthing went wrong')
    else:
        form = RegistrationForm()
    context = {'form':form}
    return render(request,'register.html',context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            raise ValueError(f"Username {username} doesn't exist")
        else:
            user = authenticate(username = username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def add_course(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.creator = request.user
            course.save()
            return redirect('home')
    context = {'form':form}
    
    return render(request,'course_form.html',context)

def course_view(request,name):
    course = get_object_or_404(Course, name=name)
    lessons = Lesson.objects.filter(course=course)
    
    # Get or create CourseAccess for the specific course
    course_access, created = CourseAcess.objects.get_or_create(course=course)
    participants = course_access.participants.all()
    
    if request.method == 'POST':
        user = request.user
        if user.balance >=course.price:
            user.balance -= course.price
            user.save()
            course_access.participants.add(user)
            messages.success(request,'you successfully enrolled')
            return redirect('course',name=course.name)
        else:
            messages.error(request,'Insufficient balance')
            return redirect('course',name=course.name)
    context = {
        'course': course,
        'lessons': lessons,
        'participants': participants}

    return render(request,'course_room.html',context)

def add_lesson(request,name):
    course = Course.objects.get(name=name)
    form = LessonForm()
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course',name = course.name)
    context = {'form':form}
    
    return render(request,'lesson_form.html',context)