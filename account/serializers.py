from account.models import User
from rest_framework import serializers

from tutorial import errors


class AccountPersonalSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    id_card = serializers.CharField(write_only=True, required=False)
    real_name = serializers.CharField(write_only=True, required=False)
    cellphone = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'real_name', 'id_card', 'cellphone', 'email')

    def save(self):
        username = self.validated_data.get('username', None)
        password = self.validated_data.pop('password', None)
        id_card = self.validated_data.pop('id_card', '').upper()
        real_name = self.validated_data.get('real_name', '')
        cellphone = self.validated_data.get('cellphone', '')
        email = self.validated_data.pop('email', '')

        if User.objects.filter(username=username).exists():
            raise errors.raise_validation_error('已存在')