from profiles_api import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset') #hello-viewset is the url for accessing viewSet fuunctions
router.register('profile',views.UserProfileViewSet)
urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('', include(router.urls)), #Automatically create url patterns for all functions defined in ViewSet class in view.py
]
