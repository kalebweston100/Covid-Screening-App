from rest_framework import serializers

class verifySerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()