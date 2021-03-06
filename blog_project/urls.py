"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter

from blog_app.views import(
    # UserModelViewSet,
    # PostModelViewSet,
    UserCreationAPIView,
    PaginatedPostModelViewSet,
    ListPost,
    CreatePost,
    PaginatedPosts,
    DeletePost,
    UpdatePost,
    CountPublishedAndNot,
    AllQuery,

)
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
# router.register('users',UserModelViewSet,basename='users')
# router.register('all',PostModelViewSet,basename='posts')
# router.register('paginated',PaginatedPostModelViewSet,basename='paginated')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    # path('user/',UserCreationAPIView.as_view()),
    path('create/',CreatePost.as_view()),
    path('listall/',ListPost.as_view()),
    path('list/<str:username>',ListPost.as_view()),

    # ------------------------------------------------
    path('paginatedposts/',PaginatedPosts.as_view()),
    path('paginatedposts/<int:pk>',PaginatedPosts.as_view()),
    # -------------------------------------------------------
    path('delete/',DeletePost.as_view()),
    path('delete/<int:id>',DeletePost.as_view()), 

    # ---------------------------------------------------
    path('update/',UpdatePost.as_view()),
    path('update/<int:id>',UpdatePost.as_view()),    
    path('countpublished/',CountPublishedAndNot.as_view()),
    path('query/',AllQuery.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
usethis so that we can access url with the url pointing to mediaroot folder

The MEDIA_ROOT is the path on the filesystem to the directory containing your static media.

The MEDIA_URL is the URL that makes the static media accessible over HTTP.
'''