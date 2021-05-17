from django.urls import path
from verify import views

urlpatterns = [
    path('company/<str:url_string>/', views.displayVerifyCompany),
    path('company/<str:url_string>/complete/', views.verifyCompanyAccount),
    path('account/<str:url_string>/', views.displayVerifyAccount),
    path('account/<str:url_string>/complete/', views.verifyUserAccount)
]
