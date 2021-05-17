from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework import status
from main import models
from login import serializers
from login.mail import checkEmail, verifyCompanyEmail, verifyAccountEmail


#renders the login page
@ensure_csrf_cookie
def renderPage(request):
    return render(request, 'login/login.html')


#registers a Company and admin to access that Company's data
#from answers to Checks by users associated with that account
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def registerCompany(request):
    data = serializers.registerSerializer(data=request.data)
    if data.is_valid():
        email = data.validated_data['email']
        hash_email = make_password(email, salt='salt')
        previous = models.Company.objects.filter(email=hash_email)
        if not previous.exists():
            username = data.validated_data.pop('username', None)
            password = data.validated_data.pop('password', None)
            test = User.objects.filter(username=username)
            if test.exists():
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                if checkEmail(email):
                    user = User.objects.create_user(username=username, password=password)
                    company = data.save(user_id=user.id)
                    verify = models.VerifyAccount.objects.create(user_id=user.id)
                    verifyCompanyEmail(email, verify, company)
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            errorData = serializers.returnErrorSerializer(error_message='previous')
    else:
        errorData = serializers.returnErrorSerializer(error_message='invalid')
    return Response(errorData.data, status=status.HTTP_400_BAD_REQUEST)


#allows the user to check that the key they enter
#is valid and belongs to the correct company
#provides more detailed error messages about key failure
#than register user view
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def checkKey(request):
    data = serializers.checkKeySerializer(data=request.data)
    if data.is_valid():
        key = data.validated_data['key']
        company = models.Company.objects.filter(key=key).first()
        if company:
            name = company.name
            if not company.active:
                returnData = serializers.returnCheckKeySerializer(name=name, message='inactive')
            elif not company.verified:
                returnData = serializers.returnCheckKeySerializer(name=name, message='unverified')
            else:
                returnData = serializers.returnCheckKeySerializer(name=name, message='valid')
            return Response(returnData.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND) 
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


#creates a user account for the Company that
#is associated with the Company key entered
#serializer checks for the company being verified and active
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def createUser(request):
    data = serializers.createClientSerializer(data=request.data)
    if data.is_valid():
        username = data.validated_data.pop('username', None)
        password = data.validated_data.pop('password', None)
        test = User.objects.filter(username=username)
        if test.exists():
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            email = data.validated_data['email']
            hash_email = make_password(email, salt='salt')
            unverified = models.Client.objects.filter(email=hash_email, verified=False)
            if not unverified.exists():
                key = data.validated_data['key']
                company_id = models.Company.objects.filter(key=key).first().company_id
                client = models.Client.objects.filter(email=hash_email, company_id=company_id)
                if not client.exists():
                    validEmail = checkEmail(email)
                    if validEmail:
                        user = User.objects.create_user(username=username, password=password)
                        client = data.save(user_id=user.id)
                        verify = models.VerifyAccount.objects.create(user_id=user.id)
                        verifyAccountEmail(email, verify)
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                else:
                    errorData = serializers.returnErrorSerializer(error_message='client_exists')
            else:
                errorData = serializers.returnErrorSerializer(error_message='unverified')
    else:
        errorData = serializers.returnErrorSerializer(error_message='invalid')
    return Response(errorData.data, status=status.HTTP_400_BAD_REQUEST)
    


#logs in a user and depending on whether they have
#an admin or employee account, sends them to the correct page
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def loginUser(request):
    data = serializers.loginSerializer(data=request.data)
    if data.is_valid():
        username = data.validated_data['username']
        password = data.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            client = models.Client.objects.filter(user_id=user.id).first()
            if client and client.verified and client.active:
                company = models.Company.objects.filter(company_id=client.company_id).first()
                if company and company.active:
                    login(request, user) 
                    returnData = serializers.returnAdminCheck(isAdmin=False)
                    return Response(returnData.data)
                else:
                    errorData = serializers.returnErrorSerializer(error_message='inactive')
            admin = models.Company.objects.filter(user_id=user.id).first()
            if admin and admin.verified:
                login(request, user)
                returnData = serializers.returnAdminCheck(isAdmin=True)
                return Response(returnData.data)
            if not errorData:
                errorData = serializers.returnErrorSerializer(error_message='unverified')
            return Response(errorData.data, status=status.HTTP_409_CONFLICT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST) 


