from django_filters.rest_framework import DjangoFilterBackend
from ordering_service.permissions import IsShopOwner, IsOrderOwner
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from ordering_service.serializers import (
    ContactSerializer,
    AddressSerializer,
    ShopSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductInfoSerializer,
    OrderProductSerializer,
    OrderSerializer
)
from ordering_service.models import (
    Contact,
    Address,
    Shop,
    Category,
    Product,
    ProductInfo,
    OrderProduct,
    Order
)


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        shop = self.get_object()
        if shop.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем магазина!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем магазина!")
        super().perform_destroy(instance)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_destroy(instance)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save()

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_destroy(instance)


class ProductInfoViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'product__category': ['exact', ],
        'shop': ['exact', ],
        'price': ['exact', ],
    }
    search_fields = ['product', 'model', 'price']
    ordering_fields = ['product', 'model', 'price']
    permission_classes = [IsAuthenticatedOrReadOnly, IsShopOwner]

    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save()


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.type == 'buyer':
            queryset = Order.objects.filter(user=self.request.user)
        else:
            raise PermissionDenied("У вас недостаточно прав!")
        return queryset

    def perform_create(self, serializer):
        if self.request.user.type != 'buyer':
            raise PermissionDenied("У вас недостаточно прав!")
        else:
            order_products = serializer.validated_data.pop('order_products')
            contacts = serializer.validated_data.pop('contact')
            addresses = serializer.validated_data.pop('address')
            serializer.save(user=self.request.user)
            for order_product in order_products:
                OrderProduct.objects.create(order=serializer.instance, **order_product)

            for contact in contacts:
                contact['user'] = self.request.user
                Contact.objects.create(order=serializer.instance, **contact)

            for address in addresses:
                address['user'] = self.request.user
                Address.objects.create(order=serializer.instance, **address)

    def perform_update(self, serializer):
        order = self.get_object()
        if order.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем заказа!")
        else:
            order_products = serializer.validated_data.pop('order_products', None)
            contacts = serializer.validated_data.pop('contact', None)
            addresses = serializer.validated_data.pop('address', None)
            serializer.save()
            if order_products is not None:
                OrderProduct.objects.filter(order=serializer.instance).delete()
                for order_product in order_products:
                    OrderProduct.objects.create(order=serializer.instance, **order_product)

            if contacts is not None:
                Contact.objects.filter(order=serializer.instance).delete()
                for contact in contacts:
                    contact['user'] = self.request.user
                    Contact.objects.create(order=serializer.instance, **contact)

            if addresses is not None:
                Address.objects.filter(order=serializer.instance).delete()
                for address in addresses:
                    address['user'] = self.request.user
                    Address.objects.create(order=serializer.instance, **address)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем заказа!")
        else:
            OrderProduct.objects.filter(order=instance).delete()
            instance.delete()


class OrderProductViewSet(ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer
    permission_classes = [IsAuthenticated]

