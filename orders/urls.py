from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ordering_service.views import (
    ContactViewSet,
    AddressViewSet,
    ShopViewSet,
    CategoryViewSet,
    ProductViewSet,
    ProductInfoViewSet,
    OrderViewSet,
    OrderProductViewSet
)

router = DefaultRouter()
router.register('my_contact', ContactViewSet)
router.register('address', AddressViewSet)
router.register('shops', ShopViewSet)
router.register('categories', CategoryViewSet)
router.register('product', ProductViewSet)
router.register('product_info', ProductInfoViewSet)
router.register('orders', OrderViewSet)
router.register('order_product', OrderProductViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
] + router.urls
