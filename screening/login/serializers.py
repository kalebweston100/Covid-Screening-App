from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from rest_framework import serializers
from main import models


#receieves login data from user
class loginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


#returns whether the user is an admin or not to redirect 
#them to the correct page
class returnAdminCheck(serializers.Serializer):
    admin = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        isAdmin = kwargs.pop('isAdmin', None)
        super().__init__(*args, **kwargs)
        self.fields['admin'].initial = isAdmin
        

#registers a Company
#uses an email field to validate email data but saves as hashed in a TextField
class registerSerializer(serializers.ModelSerializer):
    validate_email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = models.Company
        fields = ['name', 'email', 'validate_email', 'key', 'username', 'password']

    def validate(self, data):
        key = get_random_string(length=models.Company.length)
        data['key'] = key
        data['email'] = data.pop('validate_email', None)
        return data

    def save(self, *args, **kwargs):
        self.validated_data['user_id'] = kwargs.pop('user_id')
        company = models.Company(**self.validated_data)
        company.save(initial=True)
        return company


#receives key send from frontend to check the status of
class checkKeySerializer(serializers.Serializer):
    key = serializers.CharField()


#creates a Client row
#validates email same as registerCompany
class createClientSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    validate_email = serializers.EmailField()
    key = serializers.CharField()

    class Meta:
        model = models.Client
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'validate_email', 'key']

    #keep to verify that company is valid
    #in case hacker bypasses key page
    def validate(self, data):
        #email won't be included in validated_data
        #because it's blank 
        data['email'] = data.pop('validate_email', None)
        company = models.Company.objects.filter(key=data['key']).first()
        if company and company.verified and company.active:
            return data
        else:
            raise serializers.ValidationError()
        
    def save(self, *args, **kwargs):
        key = self.validated_data.pop('key', None)
        company = models.Company.objects.filter(key=key).first()
        self.validated_data['company_id'] = company.company_id
        self.validated_data['user_id'] = kwargs.pop('user_id', None)
        client = models.Client(**self.validated_data)
        client.save(create_client=True)
        return client


#returns the error data if there is an error
class returnErrorSerializer(serializers.Serializer):
    error_message = serializers.CharField()

    def __init__(self, *args, **kwargs):
        error_message = kwargs.pop('error_message', None)
        super().__init__(*args, **kwargs)
        self.fields['error_message'].initial = error_message


#returns the data from the check key query
class returnCheckKeySerializer(serializers.Serializer):
    name = serializers.CharField()
    message = serializers.CharField()

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        message = kwargs.pop('message', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].initial = name
        self.fields['message'].initial = message
