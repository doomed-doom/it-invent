from django.apps import apps
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import NotFound, ValidationError
from assets.models import CustomAsset, CustomAssetDetails
from assets.serializers import (
    ComponentsSerializer,
    ConsumablesSerializer,
    CustomAssetDetailsSerializer,
    CustomAssetSerializer,
    EquipmentsSerializer,
    ProgramsSerializer,
    RepairsSerializer,
)
from core import settings
from .models import TransferRequest
from transfers.serializers import TransferRequestSerializer


class TransferRequestView(APIView):
    def get(self, request):
        user = request.user

        if user.Роль == "manager":
            transfer_requests = TransferRequest.objects.filter(
                Q(from_user__Организация=user.Организация)
                | Q(to_user__Организация=user.Организация)
            )
        elif user.Роль == "user":
            transfer_requests = TransferRequest.objects.filter(from_user=user)
        else:
            transfer_requests = TransferRequest.objects.all()

        asset_serializer_map = {
            "equipments": EquipmentsSerializer,
            "programs": ProgramsSerializer,
            "components": ComponentsSerializer,
            "consumables": ConsumablesSerializer,
            "repairs": RepairsSerializer,
            "customasset": CustomAssetSerializer,
        }

        serializer = TransferRequestSerializer(
            transfer_requests,
            many=True,
            context={"asset_serializer_map": asset_serializer_map},
        )

        for transfer_request in serializer.data:
            asset_type = transfer_request.get("asset_type")
            asset_id = transfer_request.get("asset_id")

            if asset_type == "customasset":
                custom_asset = CustomAsset.objects.filter(id=asset_id).first()
                if custom_asset:
                    custom_asset_details = CustomAssetDetails.objects.filter(
                        Актив=custom_asset
                    )
                    transfer_request["asset_detail"] = CustomAssetDetailsSerializer(
                        custom_asset_details, many=True
                    ).data
            else:
                content_type = ContentType.objects.get(model=asset_type)
                asset = content_type.get_object_for_this_type(id=asset_id)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        from_user = request.user
        to_user_id = request.data.get("to_user")
        asset_type = request.data.get("asset_type")
        asset_id = request.data.get("asset_id")

        if not to_user_id or not asset_type or not asset_id:
            raise ValidationError(
                "Обязательные параметры отсутствуют: to_user, asset_type, asset_id."
            )

        User = apps.get_model(settings.AUTH_USER_MODEL)
        to_user = User.objects.filter(id=to_user_id).first()
        if not to_user:
            raise ValidationError("Получатель не найден.")

        try:
            if asset_type not in [
                "equipments",
                "programs",
                "components",
                "consumables",
                "repairs",
            ]:
                content_type = ContentType.objects.get_for_model(CustomAsset)
                asset_by_name = CustomAsset.objects.get(Название=asset_type)

                if not asset_by_name:
                    raise NotFound(
                        f"Актив с id '{asset_id}' и названием '{asset_type}' не найден."
                    )
                else:
                    asset = asset_by_name.details.get(id=asset_id)

                    if not asset:
                        raise NotFound(f"Актив '{asset_by_name.Название}' не найдены.")

            else:
                content_type = ContentType.objects.get(model=asset_type)
                asset = content_type.get_object_for_this_type(id=asset_id)

        except ContentType.DoesNotExist:
            raise NotFound("Указанный тип актива не найден.")
        except CustomAssetDetails.DoesNotExist:
            raise NotFound("Указанный актив не найден.")
        except Exception as e:
            raise ValidationError(f"Ошибка при поиске актива: {str(e)}")

        if from_user.Роль == "user" and asset.Сотрудник_Логин != from_user.username:
            raise ValidationError("Вы не являетесь владельцем данного актива.")

        if from_user.Роль == "manager" and to_user.Организация != from_user.Организация:
            raise ValidationError(
                "Менеджеры могут передавать активы только внутри своей организации."
            )

        existing_request = TransferRequest.objects.filter(
            from_user=from_user,
            to_user=to_user,
            content_type=content_type,
            object_id=asset_id,
        ).first()

        if existing_request:
            raise ValidationError("Заявка на передачу этого актива уже существует.")

        status_value = (
            "approved" if from_user.Роль in ["manager", "admin"] else "pending"
        )

        try:
            transfer_request = TransferRequest.objects.create(
                from_user=from_user,
                to_user=to_user,
                content_type=content_type,
                object_id=asset_id,
                status=status_value,
            )

            if status_value == "approved":
                asset.Сотрудник_Логин = transfer_request.to_user.username
                asset.Сотрудник = f"{transfer_request.to_user.Фамилия} {transfer_request.to_user.Имя} {transfer_request.to_user.Отчество}".strip()
                asset.Сотрудник_Компания = transfer_request.to_user.Организация
                asset.Сотрудник_Подразделение = transfer_request.to_user.Подразделение
                asset.Сотрудник_Телефон = transfer_request.to_user.Телефон
                asset.Сотрудник_EMail = transfer_request.to_user.email
                asset.save()

            return Response(
                {
                    "status": "success",
                    "message": "Заявка создана",
                    "data": TransferRequestSerializer(transfer_request).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            raise ValidationError(f"Ошибка при создании заявки: {str(e)}")

    def put(self, request, pk):
        transfer_request = TransferRequest.objects.filter(id=pk).first()

        if not transfer_request:
            raise NotFound("Запрос на передачу не найден.")

        action = request.data.get("action")

        if action == "approve":
            transfer_request.approve(request.user)
        elif action == "reject":
            transfer_request.reject(request.user)
        else:
            raise ValidationError(
                "Некорректное действие. Должно быть 'approve' или 'reject'."
            )

        serializer = TransferRequestSerializer(transfer_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
