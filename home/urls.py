from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('admin-login/', views.admin, name="admin_login"),
    path('admin-login/signin/', views.handleSignin, name="handleSignin"),
]