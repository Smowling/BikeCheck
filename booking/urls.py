from django.urls import path

from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path (f'store/<str:store_name>/', views.details, name='details'),
    path (f'login/', views.login_view, name="login"),
    path (f'register/', views.register, name="register"),
    path (f'logout/', views.logout_view, name="logout"),
    path (f'<str:user_login>/add_address/', views.add_address, name="add_address"),
    path (f'account/', views.account, name="account"),
    path (f'<str:user_login>/bikedelete/<int:id>/', views.bikedelete, name="bikedelete"),
    path (f'<str:user_login>/user_details_add_address', views.user_details_add_address, name="user_add_address"),
    path (f'<str:user_login>/adressdelete/<int:id>/', views.adressdelete, name="adressdelete"),
    
      
]
