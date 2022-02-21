from wsgiref import validate
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
from .cutom_pagination import CustomLimitOffsetPagination
from rest_framework.authentication import(
    BasicAuthentication,

)
from rest_framework.permissions import(
    IsAuthenticated
)

'''
Removed because we are using api view so we don't need it 
'''
# class UserModelViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


'''
Return api response with pagination
'''
class PaginatedPostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class= CustomLimitOffsetPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

'''
Return api response without pagination
'''
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def validate_text(text):
        if(len(text)<=4):
            return False
        return True

    def create(self, request, *args, **kwargs):
        try:
            user_object = request.user
            title= request.data.get('title')
            title_validation_result = self.validate_text(title)
            content= request.data.get('content')
            content_validation_result = self.validate_text(content)
            if title_validation_result and content_validation_result:
                Post.objects.create(user=user_object,title=title,content=content )
                success = {'success' :'sucessfully created post in database'}
                return Response(success)
            else:
                error = {'error' :'Please Enter Title and Content with size greater than 4'}
                return Response(error)                
        except Exception as e:
            error = {'error' :str(e)}
            return Response(error)



    

'''
API for creating user using username and password with unique uername
'''
class UserCreationAPIView(APIView):
    def post(self, request , format=None,**kwargs):
        return self.valid_user(request)

    def get(self,request , fromat=None, **kwargs):
            error = {'error' :'Only post request are allowed'}
            return Response(error)
    def valid_user(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        try :
            User.objects.create(username=username,password=password)
            success = {'success' :'Inserted Successfully '}
            return Response(success)    
        except Exception as e:
            error = {'error' :str(e)}
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