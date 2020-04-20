from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
    path('login', views.getLogin, name="login"),
    path('logout', views.getlogout, name="logout"),
    path('register',views.getRegister,name="register"),
]