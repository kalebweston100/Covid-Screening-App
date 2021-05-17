from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import datetime
from main import models
from main import serializers

#redirects user to login page
#if an error occurs
#403 or 404
def request_error(request, exception=None):
    return redirect('render_login')

#determines whether admin exists and has been verified
def isAdmin(admin=None):
    valid = False
    if admin and admin.verified:
        valid = True
    return valid

#renders admin page
#sends current company name 
#and redirects unauthorized users
@ensure_csrf_cookie
def renderPage(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if request.user.is_authenticated and isAdmin(admin=admin):
        company_name = admin.name
        return render(request, 'main/admin.html', {'name' : company_name})
    else:
        return redirect('render_login')


#logs user out
#checks to make sure that logout worked
#and returns error status if it didn't
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        logout(request)
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#receives a start and end date of the current company's Checks to be sent back
#if either the start or end date are not provided then return all that company's checks
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def displaySummary(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        data = serializers.summaryDateSerializer(data=request.data)
        if data.is_valid():
            company_id = admin.company_id
            start_date = data.validated_data['start_date']
            end_date = data.validated_data['end_date']
            checks = models.Check.objects.filter(company_id=company_id, completed=True)
            if start_date and end_date:
                checks = checks.filter(completed_time__range=[start_date, end_date])
            returnData = serializers.displayCheckSerializer(checks, many=True)
            return Response(returnData.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#displays non-personal questions for the answers page
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def displayQuestions(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        company_id = admin.company_id
        questions = models.Question.objects.filter(company_id=company_id, personal=False)
        returnData = serializers.displayQuestionSerializer(questions, many=True)
        return Response(returnData.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#displays the entries related to the question_number sent and the user's company_id
#uses bool_answer keyword in the return data so the javascript knows how to format it
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def displayAnswers(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        data = serializers.numberSerializer(data=request.data)
        if data.is_valid():
            company_id = admin.company_id
            question_number = data.validated_data['send_number']
            question = models.Question.objects.filter(company_id=company_id, question_number=question_number).first()
            if not question.personal:
                entries = models.Entry.objects.filter(company_id=company_id, question_number=question_number)
                returnData = serializers.displayEntrySerializer(entries, many=True)
                return Response(returnData.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)


#saves a new custom question
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def saveQuestion(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        data = serializers.createQuestionSerializer(data=request.data)
        if data.is_valid():
            company_id = admin.company_id
            data.save(company_id=company_id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#deletes the selected question
#takes sent question_number and validates that the question
#related to that number exists in the Company and deletes it
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def deleteQuestion(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        data = serializers.numberSerializer(data=request.data)
        if data.is_valid():
            question_number = data.validated_data['send_number']
            company_id = admin.company_id
            question = models.Question.objects.filter(company_id=company_id, question_number=question_number)
            if question.exists():
                delete = question.delete()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)


#displays all saved questions on the edit questions page
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def displayEditQuestions(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        company_id = admin.company_id
        questions = models.Question.objects.filter(company_id=company_id)
        returnData = serializers.displayQuestionSerializer(questions, many=True)
        return Response(returnData.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#adds all questions saved in the 
#DefaulQuestions table
##################################################decide if too much of a liability risk
'''
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def addDefault(request):
    user_id = request.user.id 
    if isAdmin(user_id=user_id):
        company_id = getCompanyId(user_id=user_id)
        if company_id:
            questions = models.DefaultQuestions.objects.all().values_list('content')
            for content in questions:
                save = content[0]
                new = models.Question.objects.create(company_id=company_id, content=save)
            return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)
'''

#displays all users registered with the admin's Company
#on the users page so they can be viewed and searched
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def displayUsers(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        data = serializers.searchSerializer(data=request.data)
        if data.is_valid():
            company_id = admin.company_id
            first_name = data.validated_data['first_name']
            last_name = data.validated_data['last_name']
            users = searchUsers(company_id, first_name, last_name)
            returnData = serializers.displayClientSerializer(users, many=True)
            return Response(returnData.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

#searches users based on sent first and last name
#only searches if one or both names are provided
#otherwise displays all registered users for the admin's Company
def searchUsers(company_id, first_name, last_name):
    clients = models.Client.objects.filter(company_id=company_id, active=True)
    if first_name:
        clients = clients.filter(first_name__iregex='^{}$'.format(first_name))
    if last_name:
        clients = clients.filter(last_name__iregex='^{}$'.format(last_name))
    return clients


#removes user account from admin page and prevents them from logging in
#by deleting User row but keeps client and sets active to False
#so the hashed email can be used for filtering
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def removeUser(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        data = serializers.numberSerializer(data=request.data)
        if data.is_valid():
            client_number = data.validated_data['send_number']
            company_id = admin.company_id
            client = models.Client.objects.filter(company_id=company_id, client_number=client_number).first()
            if client:
                client_id = client.user_id
                remove_user = User.objects.filter(id=client_id).delete()
                client.active = False
                client.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)


#displays account info
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def displayCompany(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        returnData = serializers.displayCompanySerializer(admin)
        return Response(returnData.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#resets the company key
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def resetKey(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        admin.save(reset_key=True)
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#changes the company password
#update method doesn't call save
#so model override doesn't effect update
'''
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def changePassword(request):
    user_id = request.user.id 
    company = models.Company.objects.filter(user_id=user_id).first()
    if company and company.verified:
        data = serializers.updatePasswordSerializer(data=request.data)
        if data.is_valid():
            password = data.validated_data['password']
            company_id = getCompanyId(user_id=user_id)
            if company_id:
                company = models.Company.objects.filter(company_id=company_id)
                company.update(password=password)
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)
'''

#changes company name
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def changeName(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        data = serializers.textSerializer(data=request.data)
        if data.is_valid():
            name = data.validated_data['send_text']
            admin.name = name
            admin.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#deactivates company so
#users cannot create accounts
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def deactivateCompany(request):
    user_id = request.user.id
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        admin.active = False
        admin.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#reactivates company so
#users can create accounts again
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def reactivateCompany(request):
    user_id = request.user.id 
    admin = models.Company.objects.filter(user_id=user_id).first()
    if isAdmin(admin=admin):
        admin.active = True
        admin.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


