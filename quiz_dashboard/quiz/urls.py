from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('request_quiz_access/<int:quiz_type_id>/', views.request_quiz_access, name='request_quiz_access'),
    path('manage_quiz_access/<int:access_id>/', views.manage_quiz_access, name='manage_quiz_access'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('quiz_types/', views.quiz_types, name='quiz_types'),
    path('quiz/<int:quiz_type_id>/<str:quiz_type_name>/', views.display_quiz, name='display_quiz'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]