from asyncio import current_task
from email.policy import default
from pyexpat import model
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
    
    published = models.BooleanField(default=False)
    image = models.ImageField(upload_to ='uploads/',blank=True,null=True,default='uploads/notfound.jpg')

    def __str__(self) -> str:
        return self.title +" posted by "+self.user.username

# ----------------------------------------------------------------------
#  types of inheritace in django

# proxy
class ProxyParent(models.Model):
    name = models.CharField(max_length=50)
    roll = models.CharField(max_length=10)


class ProxyChild(ProxyParent):
    class Meta:
        proxy=True
        ordering=['-name']


# multi table 

class MultiTableParent(models.Model):
    colg = models.CharField(max_length=50)
    location = models.CharField(max_length=10)

class MultiTableChild(MultiTableParent):
    name = models.CharField(max_length=50)
    roll = models.CharField(max_length=10)



# abstract

class AbstractParent(models.Model):
    name = models.CharField(max_length=50)
    roll = models.CharField(max_length=10)    
    class Meta:
        abstract=True

class AbstractChild(AbstractParent):
    branch = models.CharField(max_length=10)



class ProxyPost(Post):
    class Meta:
        proxy=True
        verbose_name = "ProxyPost"

class Singleton(models.Model):
    # key = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs) -> None:
        count_objects= Singleton.objects.count()
        # this will run when count_objects is non 0 and change the primary non unique which raise intrigrity error 
        if count_objects:
            current_key = Singleton.objects.first().pk
            print(current_key)
            self.pk= current_key
        super().save(*args, **kwargs)
    

    class Meta:
        verbose_name = "Singleton"
        verbose_name_plural = "Singletons"

    def __str__(self):
        return self.name


