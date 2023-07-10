from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('ordering_service.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('silk/', include('silk.urls', namespace='silk')),
]
