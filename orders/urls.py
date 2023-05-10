from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ordering_service.views import (
    ContactViewSet,
    ShopViewSet,
    CategoryViewSet,
    ProductViewSet,
    ProductInfoViewSet,
)

# router = DefaultRouter()
# router.register(r'my_contact', ContactViewSet)
# router.register('shops', ShopViewSet)
# router.register('categories', CategoryViewSet)
# router.register('product', ProductViewSet)
# router.register('product_info', ProductInfoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('ordering_service.urls')),
]
