from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from main import models
from user import serializers

#######################################################
#some views would be more efficient if they got the
#Client row and got client.company_id instead
#of calling isClient and then getCompanyId because
#that calls two SQL queries instead of one
#######################################################
#could use user_string to story company_id of a client
#to reduce the number of SQL queries and improve efficiency
########################################################

#determines if user_id has a verified Client account
def isClient(client=None):
    valid = False
    if client and client.verified:
        valid = True
    return valid

def getUserString(user_id=None):
    string_row = models.ClientString.objects.filter(user_id=user_id).first()
    user_string = string_row.user_string
    return user_string

###################################################put set_expiry on every view so it will log user out after inactivity
#render user page
@ensure_csrf_cookie
def renderPage(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        client = models.Client.objects.filter(user_id=user_id).first()
        if isClient(client=client):
            #set session to expire after 5 minutes 
            #to lower chance of session hijacking
            request.session.set_expiry(300)
            company_id = client.company_id
            company_name = models.Company.objects.filter(company_id=company_id).first().name
            return render(request, 'user/user.html', {'name' : company_name})  
    return redirect('render_login')


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    logout(request)
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def startCheck(request):
    user_id = request.user.id 
    client = models.Client.objects.filter(user_id=user_id).first()
    if isClient(client=client):
        company_id = client.company_id
        check = models.Check(company_id=company_id)
        check.save(set_number=True)
        user_string = getUserString(user_id=user_id)
        #cache.set(user_string, check.check_number)
        request.session[user_string] = check.check_number
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def completeCheck(request):
    user_id = request.user.id 
    client = models.Client.objects.filter(user_id=user_id).first()
    if isClient(client=client):
        data = serializers.completeCheckSerializer(data=request.data)
        if data.is_valid():
            user_string = getUserString(user_id=user_id)
            #check_number = cache.get(user_string)
            check_number = request.session[user_string]
            if check_number:
                #cache.delete(user_string)
                del request.session[user_string]
                company_id = client.company_id
                check = models.Check.objects.filter(company_id=company_id, check_number=check_number).first()
                check.completed = True
                check.completed_time = data.validated_data['completed_time']

                passed = determinePass(company_id, check_number)
                if passed:
                    check.passed = True
                    returnData = serializers.returnCheckSerializer(passed=True)
                else:
                    returnData = serializers.returnCheckSerializer(passed=False)
                check.save()
                return Response(returnData.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


#checks entries to determine if user passed check
def determinePass(company_id, check_number):
    passed = False
    entries = models.Entry.objects.filter(company_id=company_id, check_number=check_number, notify=True, content='yes')
    if not entries.exists():
        passed = True
    return passed


@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def saveEntry(request):
    user_id = request.user.id
    client = models.Client.objects.filter(user_id=user_id).first()
    if isClient(client=client):
        data = serializers.saveEntrySerializer(data=request.data)
        if data.is_valid():
            company_id = client.company_id
            question_number = data.validated_data['question_number']
            question = models.Question.objects.filter(company_id=company_id, question_number=question_number).first()
            user_string = getUserString(user_id=user_id)
            check_number = request.session[user_string]
            #check_number = cache.get(user_string)
            check = models.Check.objects.filter(company_id=company_id, check_number=check_number).first()
            if question and check:
                personal = question.personal
                data.validated_data['company_id'] = company_id
                data.validated_data['check_number'] = check_number
                data.validated_data['notify'] = question.notify
                entry = models.Entry(**data.validated_data)
                entry.save(personal=personal)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
        

@api_view(['POST'])
@renderer_classes([JSONRenderer])
@permission_classes([IsAuthenticated])
def displayQuestions(request):
    user_id = request.user.id
    client = models.Client.objects.filter(user_id=user_id).first()
    if isClient(client=client):
        company_id = client.company_id
        questions = models.Question.objects.filter(company_id=company_id)
        returnData = serializers.displayQuestionSerializer(questions, many=True)
        return Response(returnData.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



