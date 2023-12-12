from django.urls import path

from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path (f'store/<str:store_name>/', views.details, name='details'),
    path (f'login/', views.login, name="login"),
    path (f'register/', views.register, name="register"),
    
]
