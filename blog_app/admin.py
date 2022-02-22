from django.conf import settings
from django.contrib import admin
from numpy import imag
from .models import Post
# Register your models here.    
from django.utils.html import format_html
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # fields = ['user','title','content','creation_date_time','image','published']
    readonly_fields = ('creation_date_time','id',)
    list_display= ['user','title','content','creation_date_time','image_function','published']

    def image_function(self,obj):
        width =200
        height =200

        if(self.valid_or_not(obj)):
            return format_html('<img src="{}" alt="Not Provided" width="{}" height="{}">', obj.image.url,width,height)
        else:
            return format_html('<h1>No Image Provided</h1>')

    # if there will be url it would return True else retuen false
    def valid_or_not(self,obj):
        try:
             obj.image.url
             return True
        except:
            return False
    actions = ['make_published','make_unpblished']

    def make_published(self, request, queryset):
        queryset.update(published=True)

    def make_unpblished(self, request, queryset):
        queryset.update(published=False)

       
