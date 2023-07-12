import yaml
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from ordering_service.permissions import IsShopOwner
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from ordering_service.serializers import (
    ContactSerializer,
    ShopSerializer,
    CategorySerializer,
    ProductSerializer,
    ProductInfoSerializer,
    OrderSerializer,
    AddressSerializer,
    OrderProductSerializer,
    OrderNewSerializer
)
from ordering_service.models import (
    Contact,
    Address,
    Shop,
    Category,
    Product,
    ProductInfo,
    OrderProduct,
    Order,
    Parameter,
    ProductInfoParameter
)

from .tasks import send_status_change_email


class AddressViewSet(ModelViewSet):
    """
    Работа с адресами пользователя
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


class ContactViewSet(ModelViewSet):
    """
    Работа с контактами пользователя
    """
    queryset = Contact.objects.all().select_related('user')
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    """
    Получить весь список контактов пользователя
    """
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    """
    Добавление контакта/ов пользователя
    """
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    """
    Обновление контакта/ов пользователя
    """
    def perform_update(self, serializer):
        contact = self.get_object()
        if contact.user != self.request.user:
            raise PermissionDenied("Вы не можете редактировать чужие данные")
        super().perform_update(serializer)

    """
    Удаление контакта/ов пользователя
    """
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужие данные!")
        super().perform_destroy(instance)

    """
    Получение списка адресов контакта пользователя
    """
    @action(detail=False)
    def addressies(self, request, pk=None):
        contact = self.get_object()
        serializer = AddressSerializer(contact.addressies.all(), many=True)
        return Response(serializer.data)

    """
    Добавление нового адреса к контакту пользователя
    """
    @action(detail=True, methods=['post'])
    def add_address(self, request, pk=None):
        contact = self.get_object()

        if contact.addressies.count() >= 5:
            raise serializers.ValidationError("У вас максимальное количество адресов. Удалите ненужный или"
                                              "отредактируйте существующий")

        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(contact=contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Обновление адреса
    """
    @action(detail=True, methods=['put'])
    def update_address(self, request, pk=None, address_pk=None):
        contact = self.get_object()
        address = get_object_or_404(Address, pk=address_pk, contact=contact)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Удаление адреса
    """
    @action(detail=True, methods=['delete'])
    def delete_address(self, request, pk=None, address_pk=None):
        contact = self.get_object()
        address = get_object_or_404(Address, pk=address_pk, contact=contact)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopViewSet(ModelViewSet):
    """
    Работа с магазином
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    """
    Добавление магазина
    """
    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save(user=self.request.user)

    """
    Обновление данных магазина
    """
    def perform_update(self, serializer):
        shop = self.get_object()
        if shop.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем магазина!")
        super().perform_update(serializer)

    """
    Удаление магазина
    """
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем магазина!")
        super().perform_destroy(instance)


class CategoryViewSet(ModelViewSet):
    """
    Работа с категориями
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    """
    Добавление категории
    """
    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save(user=self.request.user)

    """
    Обновление данных категории
    """
    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_update(serializer)

    """
    Удаление категории
    """
    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_destroy(instance)


class ProductViewSet(ModelViewSet):
    """
    Работа с продуктом (товаром)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    """
    Создание продукта (товара)
    """
    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save()

    """
    Обновление информации о продукте (товаре)
    """
    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_update(serializer)

    """
    Удаление продукта (товара)
    """
    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied("У вас недостаточно прав!")
        super().perform_destroy(instance)


class ProductInfoViewSet(ModelViewSet):
    """
    Работа с карточкой товара
    """
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'product__category': ['exact', ],
        'shop': ['exact', ],
        'price': ['exact', ],
    }
    search_fields = ['product__name', 'model', 'price']
    ordering_fields = ['product__name', 'model', 'price']
    permission_classes = [IsAuthenticatedOrReadOnly, IsShopOwner]

    """
    Создание карточки продукта (товара)
    """
    def perform_create(self, serializer):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save()


class GoodsImportAPIView(APIView):
    """
    Импорт товаров из файла
    """
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.type != 'shop':
            return Response({'status': False, 'message': 'Только авторизованные поставщики могут импортировать товары.'},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            data = yaml.load(request.FILES['file'].read(), Loader=yaml.FullLoader)

            shop, created = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)

            categories = {}
            for category_data in data['categories']:
                category, created = Category.objects.get_or_create(name=category_data['name'], user_id=request.user.id)
                categories[category_data['id']] = category
                shop.categories.add(category)

            products = {}
            for product_data in data['goods']:
                category = categories[product_data['category']]
                product, created = Product.objects.get_or_create(name=product_data['name'], category=category)
                products[product_data['id']] = product
                category.products.add(product)

                product_info, created = ProductInfo.objects.get_or_create(
                    product=product,
                    shop=shop,
                    model=product_data['model'],
                    quantity=product_data['quantity'],
                    price=product_data['price'],
                    price_rrc=product_data['price_rrc']
                )

                for param_name, param_value in product_data['parameters'].items():
                    parameter, created = Parameter.objects.get_or_create(name=param_name)
                    ProductInfoParameter.objects.create(
                        product_info=product_info,
                        parameter=parameter,
                        value=param_value
                    )

            return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BasketViewSet(ModelViewSet):
    """
    Работа с корзиной
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    """
    Просмотр корзины пользователя
    """
    def get_queryset(self):
        if self.request.user.type == 'buyer':
            queryset = Order.objects.filter(user=self.request.user, status='basket')
        else:
            raise PermissionDenied("У вас недостаточно прав!")
        return queryset

    """
    Создание корзины пользователя
    """
    def perform_create(self, serializer):
        if self.request.user.type != 'buyer':
            raise PermissionDenied("У вас недостаточно прав!")
        serializer.save()

    """
    Полное обновление корзины пользователя
    """
    def perform_update(self, serializer):
        order = self.get_object()
        if order.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем заказа!")

    """
    Частичное обновление корзины пользователя
    """
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    """
    Удаление всей корзины пользователя
    """
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Вы не являетесь владельцем заказа!")
        super().perform_destroy(instance)

    """
    Удаление товара из корзины пользователя
    """
    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None, product_pk=None):
        order = self.get_object()
        product = get_object_or_404(OrderProduct, pk=product_pk, order=order)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    """
    Обновление товара в корзине пользователя
    """
    @action(detail=True, methods=['put'])
    def update_product(self, request, pk=None, product_pk=None):
        order = self.get_object()
        product = get_object_or_404(OrderProduct, pk=product_pk, order=order)
        serializer = OrderProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    """
    Работа с заказами
    """
    serializer_class = OrderNewSerializer
    permission_classes = [IsAuthenticated]

    """
    Получения списков заказов пользователя
    """
    def get(self, request):
        orders = Order.objects.filter(user=request.user).exclude(status='basket')
        serializer = OrderNewSerializer(orders, many=True)
        return Response(serializer.data)

    """
    Создание заказа пользователя из товаров в корзине
    """
    def post(self, request):
        order_id = request.data.get('order_id')
        contact_id = request.data.get('contact_id')
        if not order_id or not contact_id:
            return Response ({'error': 'Необходимо передать id заказа и id контакта'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id, user=request.user)
            contact = Contact.objects.get(id=contact_id)
        except (Order.DoesNotExist, Contact.DoesNotExist):
            return Response({'error': 'Заказ или контакт не найдены'}, status=status.HTTP_404_NOT_FOUND)

        order.contact = contact
        order.status = 'new'
        order.created_at = timezone.now()
        order.save()

        return Response({'message': 'Заказ успешно обновлен'}, status=status.HTTP_200_OK)


class PartnerOrdersSet(ModelViewSet):
    """
    Получение заказов поставщиков
    """
    queryset = Order.objects.all()
    serializer_class = OrderNewSerializer
    permission_classes = [IsAuthenticated]

    """
    Получение списка заказов, оформленных у поставщика
    """
    def get(self, request):
        if self.request.user.type != 'shop':
            raise PermissionDenied("У вас недостаточно прав!")
        else:
            orders = Order.objects.filter(order_products__product_info__shop__user_id=request.user.id
                                          ).exclude(status='basket').distinct()
            serializer = OrderNewSerializer(orders, many=True)
            return Response(serializer.data)

    """
    Функция для редактирования заказа поставщиком.
    Также использует celery для отправки email с изменением статуса заказа на почту покупателю.
    """
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        current_status = instance.status
        new_status = request.data.get('status')
        if new_status and new_status != current_status:
            recipient_email = instance.user.email
            send_status_change_email.delay(current_status, new_status, recipient_email)

        serializer.save()
        return Response(serializer.data)
