from rest_framework import serializers

from ordering_service.models import CustomUser, Contact, Address


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
