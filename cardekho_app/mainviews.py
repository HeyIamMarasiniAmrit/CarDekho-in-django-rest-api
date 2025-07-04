from django.shortcuts import get_object_or_404
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import AnonRateThrottle

from .models import car_list, Showroomlist, Review
from .api_file.serializers import carSerializers, ShowroomlistSerializer, ReviewSerializers
from .api_file.permission import AdminOrReadOnlyPermission
from .api_file.throttling import ReviewDetailThrottle, Reviewlistthrottle
from .api_file.pagination import Reviewlistpagination

# ----------------------------- Car Views -----------------------------

@api_view(['GET', 'POST'])
def car_list_view(request):
    if request.method == 'GET':
        cars = car_list.objects.all()
        serializer = carSerializers(cars, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = carSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def car_detail_view(request, pk):
    try:
        car = car_list.objects.get(pk=pk)
    except car_list.DoesNotExist:
        return Response({'error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = carSerializers(car)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = carSerializers(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------- Showroom Views ----------------------------

class ShowroomViewSet(viewsets.ModelViewSet):
    queryset = Showroomlist.objects.all()
    serializer_class = ShowroomlistSerializer


class ShowroomListCreate(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        showrooms = Showroomlist.objects.all()
        serializer = ShowroomlistSerializer(showrooms, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ShowroomlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowroomDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Showroomlist, pk=pk)

    def get(self, request, pk):
        showroom = self.get_object(pk)
        serializer = ShowroomlistSerializer(showroom)
        return Response(serializer.data)

    def put(self, request, pk):
        showroom = self.get_object(pk)
        serializer = ShowroomlistSerializer(showroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        showroom = self.get_object(pk)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------------------------- Review Views ----------------------------

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializers

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        car = get_object_or_404(car_list, pk=pk)
        user = self.request.user
        if Review.objects.filter(car=car, apiuser=user).exists():
            raise ValidationError("You have already reviewed this car.")
        serializer.save(car=car, apiuser=user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_scope = 'review_list_scope'
    throttle_classes = [Reviewlistthrottle, AnonRateThrottle]
    pagination_class = Reviewlistpagination

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [AdminOrReadOnlyPermission]
    throttle_scope = 'review_detail_scope'
    throttle_classes = [ReviewDetailThrottle, AnonRateThrottle]
