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
from .custom_pagination import CustomPagination
from rest_framework.authentication import(
    BasicAuthentication,

)
from rest_framework.permissions import(
    IsAuthenticated
)
from .serializers import PostListAllSerializer
from .custom_pagination import CustomPagination
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
    pagination_class= CustomPagination
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

'''
Return api response without pagination
'''
# class PostModelViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     @staticmethod
#     def validate_text(text):
#         if(len(text)<=4):
#             return False
#         return True
#     def create(self, request, *args, **kwargs):
#         try:
#             user_object = request.user
#             title= request.data.get('title')
#             title_validation_result = self.validate_text(title)
#             content= request.data.get('content')
#             content_validation_result = self.validate_text(content)
#             if title_validation_result and content_validation_result:
#                 Post.objects.create(user=user_object,title=title,content=content )
#                 success = {'success' :'sucessfully created post in database'}
#                 return Response(success)
#             else:
#                 error = {'error' :'Please Enter Title and Content with size greater than 4'}
#                 return Response(error)                
#         except Exception as e:
#             error = {'error' :str(e)}
#             return Response(error)


class CreatePost(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    @staticmethod
    def validate_text(text):
        if(len(text)<=4):
            return False
        return True
    def post(self, request, *args, **kwargs):
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

    def get(self, request, *args, **kwargs):
            error = {'error' :'Get method is not supported for creating use post method'}
            return Response(error)



class ListPost(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query=None
        # difference between post and data
        print(request.POST)
        print(request.data)
        username_from_get = kwargs.get('username')
        username_from_header = request.data.get('username')
        if(username_from_get!=None or username_from_header):
            try:
                username = username_from_get if (username_from_get!=None) else username_from_header
                # get user having username = username
                user= User.objects.get(username=username)
                # we get user now get all the post having user = user
                query = Post.objects.filter(user=user)
                serialized_response = PostListAllSerializer(query, many=True)
                return Response(serialized_response.data)
            except Exception as e:
                error = {'error' :str(e)}
                return Response(error)                
        query = Post.objects.all()
        try:
            
            serialized_response = PostListAllSerializer(query, many=True)
            return Response(serialized_response.data)
                           
        except Exception as e:
            error = {'error' :str(e)}
            return Response(error)
    def post(self, request, *args, **kwargs):
            error = {'error' :'Post method is not supported for getting all use get method instead'}
            return Response(error)        



class PaginatedPosts(APIView , CustomPagination):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # This method or pagination not work in apiview
    # pagination_class = CustomPagination
    @staticmethod
    def validate_text(text):
        if(len(text)<=4):
            return False
        return True

    def get(self, request, *args, **kwargs):
        query=None
        authorid = kwargs.get('pk')
        if(authorid!=None):
            try:
                # get user having id = authorid
                user= User.objects.get(id=authorid)
                # we get user now get all the post having user = user
                query = Post.objects.filter(user=user)

                # for making query paginated 
                paginated_query = self.paginate_queryset(query,request,view=self)
                serialized_response = PostListAllSerializer(paginated_query, many=True)
                return self.get_paginated_response(serialized_response.data)
            except Exception as e:
                error = {'error' :str(e)}
                return Response(error)                
        try:
            query = Post.objects.all()
            # for making query paginated 
            paginated_query = self.paginate_queryset(query,request,view=self)            
            serialized_response = PostListAllSerializer(paginated_query, many=True)
            return self.get_paginated_response(serialized_response.data)               
        except Exception as e:
            error = {'error' :str(e)}
            return Response(error)
    def post(self, request, *args, **kwargs):
            error = {'error' :'Post method is not supported for getting all use get method instead'}
            return Response(error)        
 
class DeletePost(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            id_from_get = kwargs.get('id')
            id_from_body = request.data.get('id')            
            if id_from_body!=None or id_from_get!=None:
                post_id = id_from_body if id_from_body!=None else id_from_get
                
                # we will only delete post if post belong to this user only else throw error post not exist
                current_user_object = request.user

                # fetching all the post made by this user only
                post =Post.objects.filter(user=current_user_object).get(id=post_id)
                post.delete()
                success = {'success' :'sucessfully deleted post from the database'}
                return Response(success)
            else:
                error= {'error': 'Please Provide id of your post which you want to delete. '}
                return Response(error)
        except Exception as e:
            error = {'error' :str(e)}
            return Response(error)   

class UpdatePost(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            id_from_get = kwargs.get('id')
            id_from_body = request.data.get('id')            
            if id_from_body!=None or id_from_get!=None:
                post_id = id_from_body if id_from_body!=None else id_from_get
                
                # we will only delete post if post belong to this user only else throw error post not exist
                current_user_object = request.user

                # fetching all the post made by this user only
                post = Post.objects.filter(user = current_user_object).get(id = post_id)
                
                title = request.data.get('title')
                if title != None:
                    post.title = title
                content = request.data.get('content')
                if content != None :
                    post.content = content
                
                # so that save method is called only when needed
                if title is not None or content is not None:
                    post.save()

                success = {'success' :'sucessfully updated post in the database'}
                return Response(success)
            else:
                error= {'error': 'Please Provide id of your post which you want to update. '}
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

class CountPublishedAndNot(APIView):
    def get(self,request,format=None,*args, **kwargs):
        published= Post.objects.filter(published=True).count()
        non_published= Post.objects.filter(published=False).count()
        dct ={
            "published":published,
            "non published":non_published
        }
        return Response(dct)

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