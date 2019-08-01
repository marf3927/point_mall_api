from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = router.urls
