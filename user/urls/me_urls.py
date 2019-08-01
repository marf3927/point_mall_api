from django.urls import path, include

from user import views


urlpatterns = [
    path('', views.MeView.as_view()),
    path('items/', views.MyItemsView.as_view()),
]
