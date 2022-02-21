from turtle import title
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    # for fetching unique post
    id = models.AutoField(primary_key=True)
    # for fetching post related to particular user
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    content = models.TextField()
    creation_date_time = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.title +" posted by "+self.user.username
