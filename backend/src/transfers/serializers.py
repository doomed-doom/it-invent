from rest_framework import serializers
from .models import TransferRequest


class TransferRequestSerializer(serializers.ModelSerializer):
    asset_type = serializers.CharField(source="content_type.model", read_only=True)
    asset_id = serializers.IntegerField(source="object_id", read_only=True)
    asset_detail = serializers.SerializerMethodField()

    class Meta:
        model = TransferRequest
        fields = [
            "id",
            "from_user",
            "to_user",
            "status",
            "created_at",
            "updated_at",
            "asset_type",
            "asset_id",
            "asset_detail",
        ]

    def get_asset_detail(self, obj):
        if obj.asset:
            serializer_class = self.context.get("asset_serializer_map", {}).get(
                obj.content_type.model
            )
            if serializer_class:
                return serializer_class(obj.asset).data
        return None
