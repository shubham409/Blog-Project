from django.conf import settings
from django.contrib import admin
from numpy import imag
from .models import (
    Post,

    ProxyParent,
    ProxyChild,

    MultiTableParent,
    MultiTableChild,

    AbstractParent,
    AbstractChild,
    ProxyPost,
    )
# Register your models here.    
from django.utils.html import format_html
from django.contrib.auth.models import User



class DateFilter(admin.SimpleListFilter):
    # title for the name of the filter to display on the screen
    title = "Date Wise Filter"  
    
    # we can put anything here
    parameter_name = "anything"  

    def lookups(self, request, model_admin):
        return [
            # ('value_to_match','value to display on screen')
            ("older_on_top", "Older post on top"),
            ("recent_on_top", "Recent post on top"),
        ]

    def queryset(self, request, queryset):
        # return respose on the basis of what is pressed
        if self.value() == "older_on_top":
            return queryset.order_by('creation_date_time')
        if self.value() == "recent_on_top":
            return queryset.order_by('-creation_date_time')

class PublishFilter(admin.SimpleListFilter):
    # title for the name of the filter to display on the screen
    title = "Filter Published Or Not"  
    
    # we can put anything here
    parameter_name = "anything"  

    def lookups(self, request, model_admin):
        return [
            # ('value_to_match','value to display on screen')
            ("published", "Published"),
            ("non_published", "Non published"),
        ]

    def queryset(self, request, queryset):
        # return respose on the basis of what is pressed
        if self.value() == "published":
            return queryset.filter(published=True)
        if self.value() == "non_published":
            return queryset.filter(published=False)


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

    list_filter = (DateFilter,PublishFilter,)


    # to show search field the admin page
    search_fields = ('user',)
    # it gives query set and a boolean whether it contains duplicated or not
    def get_search_results(self, request, queryset, search_term):
        try:
            user=User.objects.get(username=search_term)
            queryset.filter(user=user)
        except:

            return queryset.none(), False
        return queryset.filter(user=user),True


# abstract
# Error cant be registered 
# @admin.register(AbstractParent)
# class AbstractParent(admin.ModelAdmin):
#     list_display= ['name','roll']

@admin.register(AbstractChild)
class AbstractChild(admin.ModelAdmin):
    list_display= ['branch']

# MultiTable
@admin.register(MultiTableParent)
class AbstractParent(admin.ModelAdmin):
    list_display= ['colg','location']

@admin.register(MultiTableChild)
class AbstractChild(admin.ModelAdmin):
    list_display= ['name','roll']

# Proxy
@admin.register(ProxyParent)
class AbstractParent(admin.ModelAdmin):
    list_display= ['name','roll']

@admin.register(ProxyChild)
class AbstractChild(admin.ModelAdmin):
    list_display= ['name','roll']

@admin.register(ProxyPost)
class ProxyPostAdmin(admin.ModelAdmin ):
    list_display= ['name','roll']
    change_list_template=''
