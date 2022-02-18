from dataclasses import fields
from rest_framework import serializers

from blog_app.models import Post
from django.contrib.auth.models import User

# Note that it must be serializers.ModelSerializer don't use any thing else.

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','user','title','content']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['date_joined','email','first_name','id','is_active','is_staff','is_superuser','last_login','last_name','password','username']
        # note following fields will be visible in request
        '''
            {
                "date_joined": null,
                "email": "",
                "first_name": "",
                "is_active": false,
                "is_staff": false,
                "is_superuser": false,
                "last_login": null,
                "last_name": "",
                "password": "",
                "username": ""
            }
        '''
        # we can leave default values for serializrion
        fields = ['password','username']
        



