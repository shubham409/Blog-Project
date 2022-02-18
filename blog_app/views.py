from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.

from django.contrib.auth.models import User
from .models import (
    Post,
)
from .serializers import (
    UserSerializer,
    PostSerializer
    )
from rest_framework.views import APIView
from rest_framework.response import Response


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer   

class CustomAPIView(APIView):
    def post(self, request , format=None,**kwargs):
        return self.valid_user(request)

    def get(self,request , fromat=None, **kwargs):
            error = {'error' :'Only post request are allowed'}
            return Response(error)
    def valid_user(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(password)
        print(request.data)
        try :
            User.objects.create(username=username,password=password)
            success = {'success' :'Inserted Successfully '}
            return Response(success)    
        except Exception as e:
            print(e)
            error = {'error' :'Please Enter Valid user'}
            return Response(error)            
        
'''

may override these methods to make reqeusts 
    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
'''    