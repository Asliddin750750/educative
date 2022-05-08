from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'job')


class RegisterSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm', 'job')

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm = validated_data.pop('confirm')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        password = attrs.get('password')
        confirm = attrs.get('confirm')
        if password != confirm:
            raise ValidationError('Parollar bir xil bo\'lishi kerak')
        else:
            return attrs


class ConfirmTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('confirmed',)


# class TeacherSerializer(serializers.ModelSerializer):
#     rating = serializers.FloatField(default=0)
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'photo', 'rating')
