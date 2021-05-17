from django.urls import path
from main import views

urlpatterns = [
    #main page render
    path('', views.renderPage, name='render_admin'),

    #summary page
    path('retrieve-summary/', views.displaySummary),

    #answers page
    path('display-questions/', views.displayQuestions),
    path('display-answers/', views.displayAnswers),

    #questions page
    path('save-question/', views.saveQuestion),
    path('delete-question/', views.deleteQuestion),
    path('display-edit-questions/', views.displayEditQuestions),
    #path('add-default/', views.addDefault),

    #users page
    path('display-users/', views.displayUsers),
    path('remove-user/', views.removeUser),
    
    #account page
    path('display-company/', views.displayCompany),
    path('reset-key/', views.resetKey),
    #path('change-password/', views.changePassword),
    #path('change-email/', views.changeEmail),
    path('change-name/', views.changeName),
    path('deactivate/', views.deactivateCompany),
    path('reactivate/', views.reactivateCompany),

    #logs user out of admin page
    path('logout/', views.logoutUser)
]
