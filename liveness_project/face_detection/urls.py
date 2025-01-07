from django.urls import path
from . import views
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('', redirect_to_login),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('detect/', views.detect, name='detect'),
    path('result/', views.result, name='result'),
    path('run-test/', views.run_test_script, name='run_test_script'),
]
