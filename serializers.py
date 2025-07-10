from rest_framework import serializers
from .models import polls

class pollsSerializer(serializers.ModelSerializer):
    class Meta:
       model = polls
       fields = '__all__'

class Serializer(serializers.ModelSerializer):
    class Meta:
       model = polls
       fields = '__all__'
