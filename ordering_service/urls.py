from django.urls import path
from rest_framework.routers import DefaultRouter

from ordering_service.views import (
    ContactViewSet,
    ShopViewSet,
    CategoryViewSet,
    ProductViewSet,
    ProductInfoViewSet,
    GoodsImportAPIView,
    BasketViewSet,
    OrderView,
    PartnerOrdersSet,
)

router = DefaultRouter()
router.register(r'my_contact', ContactViewSet)
router.register('shops', ShopViewSet)
router.register('categories', CategoryViewSet)
router.register('product', ProductViewSet)
router.register('product_info', ProductInfoViewSet)
router.register(r'basket', BasketViewSet)
router.register('order/partner', PartnerOrdersSet)

urlpatterns = [
    path(
      'my_contact/<int:pk>/addressies/',
      ContactViewSet.as_view({'get': 'addressies'}),
      name='contact-addressies'
    ),
    path(
      'my_contact/<int:pk>/add_address/',
      ContactViewSet.as_view({'post': 'add_address'}),
      name='contact-add-address'
    ),
    path(
      'my_contact/<int:pk>/update_address/<int:address_pk>/',
      ContactViewSet.as_view({'put': 'update_address'}),
      name='contact-update-address'
    ),
    path(
      'my_contact/<int:pk>/delete_address/<int:address_pk>/',
      ContactViewSet.as_view({'delete': 'delete_address'}),
      name='contact-delete-address'
    ),
    path(
        'basket/<int:pk>/delete_product/<int:product_pk>/',
        BasketViewSet.as_view({'delete': 'delete_product'}),
        name='basket-delete-product'
    ),
    path(
      'basket/<int:pk>/update_product/<int:product_pk>/',
      BasketViewSet.as_view({'put': 'update_product'}),
      name='basket-update-product'
    ),
    path(
        'goods-import/',
        GoodsImportAPIView.as_view(),
        name='goods-import'
    ),
    path(
        'order/',
        OrderView.as_view(),
        name='order'
    ),
] + router.urls
