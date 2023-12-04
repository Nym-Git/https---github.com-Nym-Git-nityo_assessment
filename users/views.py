from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import user_passes_test
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .models import *

  
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)

  return {
    'access_token': str(refresh.access_token)
  }


@csrf_exempt
@permission_classes([AllowAny])
@api_view(['POST'])
def user_register(request):
  if request.method == 'POST':
    user_name = request.data.get('username')
    password = request.data.get('password')

    if user_name is None or password is None:
        return Response({'error': 'Please enter both username and password'},status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(user_name=user_name)
        return Response({'error': 'Username already exists'},status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        pass
    except Exception as e:
        return Response(
            {
                'error': str(e),
                "message": "Something went wrong connect to 'Admin'",
                "development_message": "Developer :) Check with migration files or data table duplicacy Issue"},status=status.HTTP_400_BAD_REQUEST)

    if int(len(password.replace(" ", ""))) <= 3:
      return Response({"message": "Password length should be grater then three"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      token = get_tokens_for_user(User.objects.create_user(user_name=user_name, password=password, is_active=True))
      return Response(token, content_type="appliaction/json", status=status.HTTP_200_OK)
    except Exception as e:
      print(e)
      return Response({"message": "Something went wrong while registering connect to 'Admin'", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
@user_passes_test(lambda u: not u.is_authenticated)
def login(request):
  if request.method == 'POST':
      user_name = request.data.get("username")
      password = request.data.get("password")

      if user_name is None or password is None:
        return Response({'error': 'Please enter both, email and password'},status=status.HTTP_400_BAD_REQUEST)
      
      try:
        user = User.objects.get(user_name=user_name)
      except User.DoesNotExist:
        return Response({'error': 'Username not found'},status=status.HTTP_404_NOT_FOUND)
      
      if check_password(password, user.password):
        token = get_tokens_for_user(user)
        return Response(token, content_type="appliaction/json", status=status.HTTP_200_OK)
      
      else:
        return Response({"error": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
      