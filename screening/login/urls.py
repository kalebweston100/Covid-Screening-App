from django.urls import path
from login import views

urlpatterns = [
    #main page render
    path('', views.renderPage, name='render_login'),

    #register page
    #registers Company and admin account
    path('register/', views.registerCompany),

    #user page
    #checks Company name of Company key
    path('check-key/', views.checkKey),
    #registers user account for Company
    path('create-user/', views.createUser),

    #login page
    #logs in user and sends to correct page
    path('login-user/', views.loginUser)
]
