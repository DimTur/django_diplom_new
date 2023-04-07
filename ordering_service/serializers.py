from rest_framework import serializers

from ordering_service.models import CustomUser, Contact, Address, Shop, Category, Product, ProductInfo, \
    ProductInfoParameter, Parameter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'city', 'street', 'house',
                  'structure', 'building', 'apartment']

    def create(self, validated_data):
        user = validated_data['user']
        num_existing_addresses = Address.objects.filter(user=user).count()
        if num_existing_addresses >= 5:
            raise serializers.ValidationError("У вас максимальное количество адресов. Удалите ненужный или "
                                              "отредактируйте существующий")
        return super().create(validated_data)


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'user', 'phone', 'address']

    def create(self, validated_data):
        user = validated_data['user']
        num_existing_contacts = Address.objects.filter(user=user).count()
        if num_existing_contacts >= 1:
            raise serializers.ValidationError("У вас может быть только один номер телефона")
        return super().create(validated_data)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'shops']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'


class ProductInfoParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer

    class Meta:
        model = ProductInfoParameter
        fields = ['id', 'product_info', 'parameter', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    shop = ShopSerializer(many=True)
    product_info_parameters = ProductInfoParameterSerializer(many=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'shop', 'model', 'quantity', 'price', 'price_rrc', 'product_info_parameters']

