
from django.contrib import admin
from django.urls import path, include
from point_mall import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('users/', include('user.urls.user_urls')),
    path('items/', include('item.urls.item_urls')),
    path('me/', include('user.urls.me_urls')),
    path('media/uploads/item_images/<str:file_name>', views.image_view),
    path('categories/', include('item.urls.category_urls')),
]
