from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token  # Correct import
from user_app.api.serializers import Registerserializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@authentication_classes({TokenAuthentication})
def logout_view(request):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            Token.objects.filter(user=user).delete()  # Delete user's token
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def registration_view(request):
    
    if request.method == 'POST':
        
        serializer = Registerserializer(data=request.data)
        
         refresh = RefreshToken.for_user(user)
        
        data ['token'] = {
             'refresh': str(refresh),
        'access': str(refresh.access_token),
        }
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)  # Generate token
            return Response({
                "message": "Registration successful",
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
