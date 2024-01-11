from django.urls import path

from . import views

urlpatterns = [
    path ('', views.index, name='index'),
    path (f'store/<str:store_name>/', views.details, name='details'),
    path (f'login/', views.login_view, name="login"),
    path (f'register/', views.register, name="register"),
    path (f'logout/', views.logout_view, name="logout"),
    path (f'account/', views.account, name="account"),
    path (f'account/add_address/', views.add_address, name="add_address"),
    path (f'account/add_bike/', views.add_bike, name="add_bike"),
    path (f'account/edit_address/<int:id>', views.edit_address, name="edit_address"),
    path (f'account/edit_bike/<int:id>', views.edit_bike, name="edit_bike"),
    path (f'account/bikedelete/<int:id>/', views.bikedelete, name="bikedelete"),
    path (f'account/addressdelete/<int:id>/', views.addressdelete, name="addressdelete"),
    path (f'account/address/', views.account_address, name="account_address"),
    path (f'account/bike/', views.account_bike, name="account_bike"),
    path (f'account/favourite', views.account_favourite, name="account_favourite"),
    path (f'account/visits', views.account_visits, name="account_visits"),
          
]
