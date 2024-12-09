from django.shortcuts import render
from .models import car_list
from django.http import JsonResponse
from .api_file.serializers import carSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view()
def car_list_view(request):
    car = car_list.objects.all()
    serializer = carSerializers(car, many=True)
    return Response(serializer.data)


@api_view()
def car_detail_view(request,pk):
    car = car_list.objects.get(pk=pk)
    serializer = carSerializers(car)
    return Response(serializer.data)