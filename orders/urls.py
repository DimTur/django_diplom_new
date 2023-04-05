from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ordering_service.views import ContactViewSet, AddressViewSet

router = DefaultRouter()
router.register('my_contact', ContactViewSet)
router.register('my_contact/address', AddressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
] + router.urls
