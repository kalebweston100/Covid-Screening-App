from rest_framework import serializers
from main import models
from main.shortcuts import getCompanyId

#sends time that a Check is completed
class completeCheckSerializer(serializers.Serializer):
    completed_time = serializers.DateTimeField(input_formats=['%m/%d/%Y, %I:%M:%S %p'])


#returns the safety outcome of a Check's Entry values
class returnCheckSerializer(serializers.Serializer):
    passed = serializers.BooleanField()

    def __init__(self, *args, **kwargs):
        passed = kwargs.pop('passed', None)
        super().__init__(*args, **kwargs)
        self.fields['passed'].initial = passed


#saves an Entry's data
class saveEntrySerializer(serializers.Serializer):
    question_number = serializers.IntegerField()
    content = serializers.CharField()


#displays a Question for the Client to answer
class displayQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = ['question_number', 'content', 'bool_answer']
        
        
#returns the error data if there is an error
class returnErrorSerializer(serializers.Serializer):
    error_message = serializers.CharField()

    def __init__(self, *args, **kwargs):
        error_message = kwargs.pop('error_message', None)
        super().__init__(*args, **kwargs)
        self.fields['error_message'].initial = error_message