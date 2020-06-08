from django.urls import path
from django.http import StreamingHttpResponse
from . import views
from camera_app.views import VideoCamera, gen

urlpatterns = [
  path('', views.index, name='index'),
  path('livefeed/', views.livefeed, name='livefeed') 
]