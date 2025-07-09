from django.contrib.auth import login
from django.contrib.auth.models import User
from userManagement.models import Student

from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework.generics import CreateAPIView
from knox.views import LoginView as KnoxLoginView

class KonxLoginUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            # 'id',
            'first_name',
            'last_name',
            'email',
            'student'
        )
        depth = 1
class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
class StudentSerialzer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = (
            'user',
            'phone_num'
        )
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        print(user_data)
        user = User.objects.create_user(**user_data)
        return Student.objects.create(user=user, **validated_data)
class SignUpView(CreateAPIView):
    serializer_class = StudentSerialzer
    permission_classes = (AllowAny,)

    # def post(self, request):
    #     print(request.data)
    #     first_name, *last_name = request.data['name'].split()
    #     user=User.objects.create_user(
    #         username=request.data['email'],
    #         email=request.data['email'],
    #         first_name=first_name,
    #         last_name=" ".join(last_name),
    #         password=request.data['password']
    #     )
    #     try:
    #         user.save()
    #         return Response("Created")
    #     except:
    #         return Response("Not Created")