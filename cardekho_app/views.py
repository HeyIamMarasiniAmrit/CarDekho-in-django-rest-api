from urllib import request

import status as status
from django.shortcuts import render
from .models import car_list
from django.http import JsonResponse
from .api_file.serializers import carSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET', 'POST'])
def car_list_view(request):
    if request.method == 'GET':
      car = car_list.objects.all()
      serializer = carSerializers(car, many=True)
      return Response(serializer.data)

    if request.method == 'POST':
        serializer = carSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE'])
def car_detail_view(request,pk):
    if request.method == 'GET':
        try:
          car = car_list.objects.get(pk=pk)
        except:
            return Response({'Error':'car not found'}, status= status.HTTP_404_NOT_FOUND)
        serializer = carSerializers(car)
        return Response(serializer.data)

    if request.method == 'PUT':
        car = car_list.objects.get(pk=pk)
        serializer = carSerializers(car,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
          return Response(serializer.errors,status=status.HTTP_400_BAD_RESQUEST)

    if request.method == 'DELETE':
        car = car_list.objects.get(pk=pk)
        car.delete()
        return Response (status= status.HTTP_204_NO_CONTENT)
