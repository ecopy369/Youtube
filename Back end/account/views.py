from rest_framework import generics
from .models import Account
from api.serializers import AccountSignUpSerializer, AccountLogInSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class AccountSignUpView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSignUpSerializer


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        login_value = request.data.get('login')
        # برای کاربران عادی اختیاری است
        username = request.data.get('username')
        password = request.data.get('password')

        if not login_value or not password:
            return Response({"error": "لطفا login و password را وارد کنید."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, login=login_value,
                            username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "اطلاعات ورود نادرست است."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        videos = Account.objects.all()
        Serializer = AccountLogInSerializer(instance=videos, many=True)
        return Response(Serializer.data)
