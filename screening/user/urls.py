from django.urls import path
from user import views

urlpatterns = [
    path('', views.renderPage, name='render_user'),
    path('start/', views.startCheck),
    path('save-entry/', views.saveEntry),
    path('display-questions/', views.displayQuestions),
    path('complete/', views.completeCheck),
    path('logout/', views.logoutUser)
]
