from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .models import (
    CustomAsset,
    CustomAssetDetails,
    Equipments,
    ExportFile,
    Programs,
    Components,
    Consumables,
    Repairs,
    Movements,
)


# base serializers
class BaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = self.context["request"].user

        if user.Роль == "user":
            raise PermissionDenied("Вы не можете создавать записи.")

        return super().create(validated_data)

    def validate_Дополнительные_Поля(self, value):
        user = self.context["request"].user

        if user.Роль != "admin":
            raise PermissionDenied("Вы не можете изменять дополнительные поля.")

        return value


# standart assets
class EquipmentsSerializer(BaseSerializer):
    class Meta:
        model = Equipments
        fields = "__all__"


class ProgramsSerializer(BaseSerializer):
    class Meta:
        model = Programs
        fields = "__all__"


class ComponentsSerializer(BaseSerializer):
    class Meta:
        model = Components
        fields = "__all__"


class ConsumablesSerializer(BaseSerializer):
    class Meta:
        model = Consumables
        fields = "__all__"


class RepairsSerializer(BaseSerializer):
    class Meta:
        model = Repairs
        fields = "__all__"


class MovementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movements
        fields = "__all__"


# custom assets
class CustomAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAsset
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user

        if user.Роль != "admin":
            raise PermissionDenied("Вы не можете создавать записи.")

        return super().create(validated_data)


class CustomAssetDetailsSerializer(BaseSerializer):
    class Meta:
        model = CustomAssetDetails
        fields = "__all__"


class ExportFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportFile
        fields = "__all__"
