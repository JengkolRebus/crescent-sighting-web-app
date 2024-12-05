from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('detail/<int:index>/', views.detail_view, name='detail2'),
]