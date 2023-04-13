from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ordering_service.models import (
    CustomUser,
    Contact,
    Address,
    Shop,
    Category,
    Product,
    ProductInfo,
    ProductInfoParameter,
    OrderProduct,
    Order
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'contact']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'user', 'city', 'street', 'house', 'structure', 'building', 'apartment']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = validated_data['user']
        num_existing_addresses = Address.objects.filter(user=user).count()
        if num_existing_addresses >= 5:
            raise serializers.ValidationError("У вас максимальное количество адресов. Удалите ненужный или "
                                              "отредактируйте существующий")
        return super().create(validated_data)


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    address = AddressSerializer(required=False)

    class Meta:
        model = Contact
        fields = ['id', 'user', 'phone', 'address']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = validated_data['user']
        num_existing_contacts = Address.objects.filter(user=user).count()
        if num_existing_contacts >= 1:
            raise serializers.ValidationError("У вас может быть только один номер телефона")
        return super().create(validated_data)


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ['id', 'user', 'name']
        read_only_fields = ['user']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'shops']
        read_only_fields = ['user']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category']


class ProductInfoParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductInfoParameter
        fields = ['parameter', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True, many=True)
    # shop = serializers.StringRelatedField()
    # product_info_parameters = ProductInfoParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'model', 'quantity', 'price', 'price_rrc', 'product_info_parameters']


class OrderProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product_info', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    contact = ContactSerializer(many=True)
    address = AddressSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'contact', 'address', 'order_products']
        read_only_fields = ['user']
