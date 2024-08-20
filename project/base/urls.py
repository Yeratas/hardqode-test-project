from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('user/<int:id>',views.user_view, name='user'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('add_course/', views.add_course,name='add_course'),
    path('add_lesson/<str:name>/', views.add_lesson,name='add_lesson'),
    path('course/<str:name>/', views.course_view, name ='course'),
]