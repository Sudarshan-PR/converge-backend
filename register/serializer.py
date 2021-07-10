from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, is_active=True):
        user = User.objects.create_user(
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            username=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            is_active=is_active
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')

class UserVerifySerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()