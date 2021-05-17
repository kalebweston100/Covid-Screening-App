from rest_framework import serializers
from main import models


#used to receive any number
class numberSerializer(serializers.Serializer):
    send_number = serializers.IntegerField()


#used to receive any text
class textSerializer(serializers.Serializer):
    send_text = serializers.CharField()


#used to receive any emails
class emailSerializer(serializers.Serializer):
    send_email = serializers.EmailField()


#used to receive the filter dates for the summary page
class summaryDateSerializer(serializers.Serializer):
    start_date = serializers.DateField(input_formats=['%Y-%m-%d'], default='')
    end_date = serializers.DateField(input_formats=['%Y-%m-%d'], default='')


#used to send Checks but excludes ids and numbers for security
#used to send data for summary page to process into a summary
class displayCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Check
        fields = ['completed_time', 'passed']


#displays non-personal questions for the answers page
#excludes all sensitive data
#used on answers page and edit questions page
class displayQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['question_number', 'content', 'bool_answer']


#used to send Entries for the answers page
#bool_answer tells the javascript whether to 
#provide a 'yes' and 'no' count instead of a text list
class displayEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Entry
        fields = ['content']

#sends data to create a new custom question from the questions page
class createQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = ['content', 'bool_answer', 'notify', 'personal']


#displays a client for the user page
class displayClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ['client_number', 'first_name', 'last_name']


#sends search data for the filtering users on the users page
class searchSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)

###################################decide what to display on account page
class displayCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = ['name', 'key', 'active']




