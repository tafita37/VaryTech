from django.urls import path

from authentification.controllers.UserController import login_user, login_user_page, logout_url, register_user, register_user_page

urlpatterns = [
    path('register_page/', register_user_page, name='register_user_page'),
    path('login_page/', login_user_page, name='login_user_page'),
    path('register_user/', register_user, name='register_user'),
    path('login_user/', login_user, name='login_user'),
    path('logout/', logout_url, name='logout'),
]