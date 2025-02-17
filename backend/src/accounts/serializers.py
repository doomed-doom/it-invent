from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "Имя",
            "Фамилия",
            "Отчество",
            "Роль",
            "Организация",
            "Подразделение",
            "Телефон",
            "date_joined",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password",
            "email",
            "Имя",
            "Фамилия",
            "Отчество",
            "Роль",
            "Организация",
            "Подразделение",
            "Телефон",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "Имя",
            "Фамилия",
            "Отчество",
            "Роль",
            "Организация",
            "Подразделение",
            "Телефон",
        ]
        extra_kwargs = {"password": {"write_only": True}}
