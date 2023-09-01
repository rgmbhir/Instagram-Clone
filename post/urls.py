from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('newpost/', views.NewPost, name='newpost'),
    path('<uuid:post_id>/', views.Postdetails, name='postdetail'),
    path('<uuid:post_id>/like/', views.PostLikes, name='likes'),
    path('<uuid:post_id>/favourite/', views.Favourite, name='favourite'),
]

