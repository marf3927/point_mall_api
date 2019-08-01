from rest_framework.routers import DefaultRouter
from django.urls import path, include

from item import views

router = DefaultRouter()
router.register('', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
