from rest_framework import serializers
from .models import polls

class pollsSerializer(serializers.ModelSerializer):
    class Meta:
       model = polls
       fields = '__all__'