from django.urls import path
from . import views



urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('direct/<username>/', views.Directs, name='direct'),
    path('send/', views.SendMessage, name='send-message'),
    path('search/', views.searchuser, name='search'),
    path('search/<username>', views.newMessage, name='new-message'),

]