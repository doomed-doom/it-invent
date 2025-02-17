from django.db import models
from django.conf import settings
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from django.db import transaction
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from assets.models import CustomAsset, CustomAssetDetails


class TransferRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("approved", "Подтверждено"),
        ("rejected", "Отклонено"),
    ]

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transfer_requests_sent",
        verbose_name="Отправитель",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transfer_requests_received",
        verbose_name="Получатель",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, verbose_name="Тип актива"
    )
    object_id = models.PositiveIntegerField(verbose_name="ID актива")
    asset = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Запрос на передачу"
        verbose_name_plural = "Запросы на передачу"
        unique_together = (
            "from_user",
            "to_user",
            "content_type",
            "object_id",
        )

    def approve(self, approver):
        if approver.Роль == "user":
            raise PermissionDenied("У вас нет прав подтверждать запросы.")

        self.status = "approved"

        with transaction.atomic():
            if self.content_type.model == "customasset":
                custom_asset = CustomAsset.objects.filter(id=self.object_id).first()
                if custom_asset:
                    asset_detail = CustomAssetDetails.objects.filter(
                        Актив=custom_asset
                    ).first()
                    if asset_detail:
                        asset_detail.Сотрудник_Логин = self.to_user.username
                        asset_detail.Сотрудник = f"{self.to_user.Фамилия} {self.to_user.Имя} {self.to_user.Отчество}".strip()
                        asset_detail.Сотрудник_Компания = self.to_user.Организация
                        asset_detail.Сотрудник_Подразделение = (
                            self.to_user.Подразделение
                        )
                        asset_detail.Сотрудник_Телефон = self.to_user.Телефон
                        asset_detail.Сотрудник_ЭMail = self.to_user.email
                        asset_detail.save()
                    else:
                        raise ValidationError("Детали актива не найдены.")
                else:
                    raise NotFound("Актив не найден.")
            else:
                asset = self.asset
                asset.Сотрудник_Логин = self.to_user.username
                asset.Сотрудник = f"{self.to_user.Фамилия} {self.to_user.Имя} {self.to_user.Отчество}".strip()
                asset.Сотрудник_Компания = self.to_user.Организация
                asset.Сотрудник_Подразделение = self.to_user.Подразделение
                asset.Сотрудник_Телефон = self.to_user.Телефон
                asset.Сотрудник_EMail = self.to_user.email
                asset.save()

            self.save()

    def reject(self, approver):
        if approver.Роль == "user":
            raise PermissionDenied("У вас нет прав отклонять запросы.")

        self.status = "rejected"
        self.save()

    @classmethod
    def send_new_request(cls, from_user, to_user, content_type, object_id):
        if from_user == to_user:
            raise ValidationError("Невозможно отправить запрос самому себе.")

        previous_request = cls.objects.filter(
            from_user=from_user,
            to_user=to_user,
            content_type=content_type,
            object_id=object_id,
        ).first()

        if previous_request:
            if previous_request.status == "approved":
                raise ValidationError(
                    "Запрос уже подтвержден. Невозможно создать новый."
                )
            elif previous_request.status == "pending":
                raise ValidationError("Запрос на передачу уже ожидает подтверждения.")
            elif previous_request.status == "rejected":
                previous_request.status = "pending"
                previous_request.save()
                return previous_request
        else:
            return cls.objects.create(
                from_user=from_user,
                to_user=to_user,
                content_type=content_type,
                object_id=object_id,
                status="pending",
            )
