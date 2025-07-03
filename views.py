from django.shortcuts import render
from django.db.models import query
from .models import polls
from .serializers import pollsSerializer
from .import serializers
from .import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.

@api_view(['GET','POST'])

def listpolls(request):
    query = polls.objects.all()

    serializer_class = pollsSerializer(query,many=True)
    context ={
        'serializer_class_data':serializer_class.data
    }
    return Response(serializer_class.data)

