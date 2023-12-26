from django.urls import path

from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path (f'store/<str:store_name>/', views.details, name='details'),
    path (f'login/', views.login_view, name="login"),
    path (f'register/', views.register, name="register"),
    path (f'logout/', views.logout_view, name="logout"),
    path (f'settings/', views.user_settings, name="settings"),
    path (f'<str:user_login>/', views.user_details, name="user_details"),
      
]
