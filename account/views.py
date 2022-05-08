from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import User
from account.serializers import LoginSerializer, UserSerializer, RegisterSerializer, ConfirmTeacherSerializer
from config.permissions import IsSuperUser


class LoginView(APIView):
    """
    Tizimga kirish
    """
    permission_classes = [~IsAuthenticated]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data.get('username'),
                            password=serializer.validated_data.get('password'))

        if user is None:
            return Response('Foydalanuvchi mavjud emas', status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):
    """
    Ro'yxatdan o'tish
    """
    permission_classes = [~IsAuthenticated]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })


class ConfirmTeacherView(UpdateAPIView):
    """
    Teacherni tasdiqlash
    """
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = ConfirmTeacherSerializer

    def get_queryset(self):
        return User.objects.filter(job=1)


# class TeacherView(RetrieveAPIView):
#     serializer_class = TeacherSerializer
#
#     def get_queryset(self):
#         stars = Review.objects.filter(course__teacher_id=self.kwargs.get('pk')).aggregate(rating=Avg('stars'))
#         return User.objects.filter(job=1).annotate(rating=Value(stars.get('rating'), output_field=FloatField()))
