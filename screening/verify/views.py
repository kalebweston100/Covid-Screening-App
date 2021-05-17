from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from main import models
from verify import serializers


#displays register page
#for user to verify that they
#registered a company
################################hash company_id???
################################shows name so option to say
#that is not your company???
@ensure_csrf_cookie
def displayVerifyCompany(request, url_string):
    verify = models.VerifyAccount.objects.filter(url_string=url_string, active=True).first()
    if verify:
        return render(request, 'verify/register.html')
    else:
        return redirect('render_login')


#verifies that you created a company account
#if you enter the correct password and key
#changes company to verified and verify to not active
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def verifyCompanyAccount(request, url_string): 
    verify = models.VerifyAccount.objects.filter(url_string=url_string, active=True)
    if verify.exists():
        data = serializers.verifySerializer(data=request.data)
        if data.is_valid():
            username = data.validated_data['username']
            password = data.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                current = verify.filter(user_id=user.id)
                company = models.Company.objects.filter(user_id=user.id)
                if current.exists() and company.exists():
                    verify.update(active=False)
                    company.update(verified=True)
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)
    #forbidden if the link is no longer active
    #or the user enters a different company's 
    #username and password

#displays verify page if url_string is stored
#in Verify model
@ensure_csrf_cookie
def displayVerifyAccount(request, url_string):
    verify = models.VerifyAccount.objects.filter(url_string=url_string, active=True)
    if verify.exists():
        return render(request, 'verify/verify.html')
    else:
        return redirect('render_login')

#changes verified to True after user who recieves
#email after registering clicks on link to verify
#page and logs in to prove that they created
#the account
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def verifyUserAccount(request, url_string):
    verify = models.VerifyAccount.objects.filter(url_string=url_string, active=True)
    if verify.exists():
        data = serializers.verifySerializer(data=request.data)
        if data.is_valid():
            username = data.validated_data['username']
            password = data.validated_data['password']
            user = authenticate(username=username, password=password)
            #make sure that there is a user account
            if user is not None:
                #makes sure that the current url belongs to the user info
                current = verify.filter(user_id=user.id)
                #makes sure there is a Client row associated with user_id
                client = models.Client.objects.filter(user_id=user.id)
                if current.exists() and client.exists():
                    verify.update(active=False)
                    client.update(verified=True)
                    return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_403_FORBIDDEN)
