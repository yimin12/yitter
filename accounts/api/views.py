from accounts.api.serializers import UserSerializer, SignupSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)

# Model View Set will inherit some method like list, delete....
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    # select * from user order by desc
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated)

class AccountViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        '''
        default username: admin, default password: admin
        '''
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors,
            }, status=400)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = django_authenticate(username=username, password=password)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "username and password does not match",
            }, status=400)
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data
        })

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        '''
        logout current user
        '''
        django_logout(request)
        return Response({"success": True})

    @action(methods=['POST'], detail=False)
    def signup(self, request):
        '''
        use username, email, password to signup
        write it in elegant way
        '''
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        user = serializer.save() # serialize the user and persist it
        django_login(request, user)
        return Response({
            'success': True,
            'user': UserSerializer(user).data,
        })

    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        '''
        check the login status and personal information
        '''
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)