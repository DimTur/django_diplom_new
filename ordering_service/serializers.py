from rest_framework import serializers

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
    Order, Parameter
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'contacts']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'contact']
        read_only_fields = ['contact']


class ContactSerializer(serializers.ModelSerializer):
    addressies = AddressSerializer(many=True)

    class Meta:
        model = Contact
        fields = ['id', 'user', 'phone', 'addressies']
        read_only_fields = ['user']

    def validate_addressies(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("У вас максимальное количество адресов. Удалите ненужный или "
                                              "отредактируйте существующий")
        return value

    def create(self, validated_data):
        addressies = validated_data.pop('addressies')
        contact = Contact.objects.create(**validated_data)

        for address in addressies:
            Address.objects.create(contact=contact, **address)

        return contact


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'user', 'name', 'state']
        read_only_fields = ['user']


class CategorySerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'shops']
        read_only_fields = ['user']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'name']


class ProductInfoParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer()

    class Meta:
        model = ProductInfoParameter
        fields = ['parameter', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    product_info_parameters = ProductInfoParameterSerializer(many=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'model', 'quantity', 'price', 'price_rrc', 'product_info_parameters']

    def create(self, validated_data):
        parameters_data = validated_data.pop('product_info_parameters')
        product_info = ProductInfo.objects.create(**validated_data)
        for parameter_data in parameters_data:
            parameter = parameter_data.pop('parameter')
            parameter_obj, _ = Parameter.objects.get_or_create(name=parameter['name'])
            ProductInfoParameter.objects.create(product_info=product_info, parameter=parameter_obj, **parameter_data)
        return product_info


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'products_info']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product_info', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)
    contact = ContactSerializer(required=False)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'contact', 'order_products', 'total_price']
        read_only_fields = ['user', 'contact']

    def get_total_price(self, obj):
        total = 0
        for order_product in obj.order_products.all():
            total += order_product.quantity * order_product.product_info.price
        return total

    def create(self, validated_data):
        products_data = validated_data.pop('order_products')
        user = self.context['request'].user
        validated_data['user'] = user
        validated_data['contact'] = Contact.objects.get(user=user)

        basket_order = Order.objects.filter(user=user, status='basket').first()

        if basket_order:
            basket = basket_order
            for product in products_data:
                OrderProduct.objects.update_or_create(
                    order=basket,
                    product_info=product['product_info'],
                    defaults={'order': basket, 'product_info': product['product_info'], 'quantity': product['quantity']}
                )

        else:
            basket = Order.objects.create(**validated_data)
            for product in products_data:
                OrderProduct.objects.create(order=basket, **product)

        return basket

    def update(self, instance, validated_data):
        products_data = validated_data.pop('order_products')
        basket, _ = Order.objects.get_or_create(**validated_data)

        for product in products_data:
            product_obj, _ = OrderProduct.objects.update_or_create(
                order=basket,
                product_info=product['product_info'],
                defaults={'order': basket, 'product_info': product['product_info'], 'quantity': product['quantity']}
            )
        return basket
