import random
import math

from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializer import UserRegisterSerializer, UserVerifySerializer

from django.core.mail import EmailMessage

from .models import UserVerifyToken
from home.models import Profile

User = get_user_model()

# Generate Random OTP
def generateOTP() :
 
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be chaged
   # by changing value in range
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create(is_active=False)
            
            if not user:
                return Response({'Error': "User registration was not successful"}, status=status.HTTP_400_BAD_REQUEST)

            if user:
                otp = generateOTP()
                data = serializer.data
                
                try:
                    email = EmailMessage("Converge Registration Verification", f"Your OTP for registration is {otp} .", to=[f'{user.email}'])
                    email.send()

                    user_verify = UserVerifyToken(user=user, pincode=otp)
                    user_verify.save()
                    data['msg'] = f'OTP has been sent to {data["email"]}'

                except Exception as e:
                    # Delete user created
                    user.delete()

                    return Response(f'{str(e)}', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response(data, status=status.HTTP_201_CREATED)
            
            return Ressponse({'Error': "Something is wrong in the server. Please try again"}, status=status.HTTP_502_BAD_GATEWAY)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class UserVerifyView(APIView):
    def post(self, request):
        otp_serializer = UserVerifySerializer(data=request.data)
        if otp_serializer.is_valid():
            data = otp_serializer.data
            try:
                user = User.objects.get(email=data['email'])
                verify_user = UserVerifyToken.objects.get(user=user)

                if data['otp'] == verify_user.pincode:
                    user.is_active = True
                    user.save()

                    # Delete token
                    verify_user.delete()

                    return Response({"msg": "Successfully registered"}, status=status.HTTP_200_OK)
                
                else:
                    return Response({"msg": "Wrong token"}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response(otp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)