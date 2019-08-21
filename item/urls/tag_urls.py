from django.urls import path

from item import views



urlpatterns = [
    path('<str:tag>/items/', views.TagItems.as_view()),
]
