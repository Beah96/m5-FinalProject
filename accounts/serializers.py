from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Account
        fields = [
            'id',
            'username',
            'email',
            'is_superuser',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {
                'validators': [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message='A user with that username already exists.'
                    )
                ]
            },
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message='user with this email already exists.'
                    )
                ]
            }
            
        }
    def create(self, validated_data : dict) -> Account:
        if validated_data['is_superuser'] == True:
            instance = Account.objects.create_superuser(**validated_data)
        else:
            instance = Account.objects.create_user(**validated_data)
        return instance
    
    