import os
import csv
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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
from assets.serializers import (
    CustomAssetDetailsSerializer,
    CustomAssetSerializer,
    EquipmentsSerializer,
    ExportFileSerializer,
    ProgramsSerializer,
    ComponentsSerializer,
    ConsumablesSerializer,
    RepairsSerializer,
    MovementsSerializer,
)

model_mapping = {
    "equipments": Equipments,
    "movements": Movements,
    "repairs": Repairs,
    "components": Components,
    "consumables": Consumables,
    "programs": Programs,
    "exportfile": ExportFile,
}


# base view
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"detail": "Актив успешно добавлен."},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        if request.user.Роль != "admin":
            raise PermissionDenied("Вы не можете редактировать записи.")

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        message = (
            "Актив успешно обновлен."
            if not partial
            else "Частичное обновление выполнено."
        )

        return Response(
            {"detail": message, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        if request.user.Роль != "admin":
            raise PermissionDenied("Вы не можете удалять записи.")

        instance = self.get_object()
        instance.delete()

        return Response({"detail": "Объект удалён"}, status=status.HTTP_204_NO_CONTENT)


# standart assets
class EquipmentsViewSet(BaseViewSet):
    queryset = Equipments.objects.all()
    serializer_class = EquipmentsSerializer

    def get_queryset(self):
        user = self.request.user

        if user.Роль == "admin":
            return Equipments.objects.all()

        elif user.Роль == "manager":
            return Equipments.objects.filter(Сотрудник_Компания=user.Организация)

        else:
            return Equipments.objects.filter(Сотрудник_Логин=user.username)


class ProgramsViewSet(BaseViewSet):
    queryset = Programs.objects.all()
    serializer_class = ProgramsSerializer

    def get_queryset(self):
        user = self.request.user

        if user.Роль == "admin":
            return Programs.objects.all()

        elif user.Роль == "manager":
            return Programs.objects.filter(Сотрудник_Компания=user.Организация)

        else:
            return Programs.objects.filter(Сотрудник_Логин=user.username)


class ComponentsViewSet(BaseViewSet):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer

    def get_queryset(self):
        user = self.request.user

        if user.Роль == "admin":
            return Components.objects.all()

        elif user.Роль == "manager":
            return Components.objects.filter(Сотрудник_Компания=user.Организация)

        else:
            return Components.objects.filter(Сотрудник_Логин=user.username)


class ConsumablesViewSet(BaseViewSet):
    queryset = Consumables.objects.all()
    serializer_class = ConsumablesSerializer

    def get_queryset(self):
        user = self.request.user

        if user.Роль == "admin":
            return Consumables.objects.all()

        elif user.Роль == "manager":
            return Consumables.objects.filter(Сотрудник_Компания=user.Организация)

        else:
            return Consumables.objects.filter(Сотрудник_Логин=user.username)


class RepairsViewSet(BaseViewSet):
    queryset = Repairs.objects.all()
    serializer_class = RepairsSerializer

    def get_queryset(self):
        user = self.request.user

        if user.Роль == "admin":
            return Repairs.objects.all()

        elif user.Роль == "manager":
            return Repairs.objects.filter(Сотрудник_Компания=user.Организация)

        else:
            return Repairs.objects.filter(Сотрудник_Логин=user.username)


class MovementsViewSet(BaseViewSet):
    queryset = Movements.objects.all()
    serializer_class = MovementsSerializer

    # def get_queryset(self):
    #     user = self.request.user

    #     if user.Роль == "admin":
    #         return Movements.objects.all()

    #     # elif user.Роль == "manager":
    #     #     return Movements.objects.filter(Сотрудник_Организация=user.Организация)

    #     else:
    #         return Movements.objects.filter(Сотрудник_Логин=user.username)


# custom assets
class CustomAssetViewSet(BaseViewSet):
    queryset = CustomAsset.objects.all()
    serializer_class = CustomAssetSerializer


class CustomAssetDetailsViewSet(BaseViewSet):
    queryset = CustomAssetDetails.objects.all()
    serializer_class = CustomAssetDetailsSerializer

    def get_queryset(self):
        user = self.request.user

        if user.Роль == "admin":
            return CustomAssetDetails.objects.all()

        elif user.Роль == "manager":
            return CustomAssetDetails.objects.filter(
                Сотрудник_Компания=user.Организация
            )

        else:
            return CustomAssetDetails.objects.filter(Сотрудник_Логин=user.username)


# all assets
class AssetsListView(APIView):
    def get(self, request):
        user = self.request.user

        categories = {
            "equipments": (
                Equipments.objects.filter(Сотрудник_Логин=user.username)
                if user.Роль != "admin" and user.Роль != "manager"
                else (
                    Equipments.objects.filter(Сотрудник_Компания=user.Организация)
                    if user.Роль == "manager"
                    else Equipments.objects.all()
                )
            ),
            "programs": (
                Programs.objects.filter(Сотрудник_Логин=user.username)
                if user.Роль != "admin" and user.Роль != "manager"
                else (
                    Programs.objects.filter(Сотрудник_Компания=user.Организация)
                    if user.Роль == "manager"
                    else Programs.objects.all()
                )
            ),
            "components": (
                Components.objects.filter(Сотрудник_Логин=user.username)
                if user.Роль != "admin" and user.Роль != "manager"
                else (
                    Components.objects.filter(Сотрудник_Компания=user.Организация)
                    if user.Роль == "manager"
                    else Components.objects.all()
                )
            ),
            "consumables": (
                Consumables.objects.filter(Сотрудник_Логин=user.username)
                if user.Роль != "admin" and user.Роль != "manager"
                else (
                    Consumables.objects.filter(Сотрудник_Компания=user.Организация)
                    if user.Роль == "manager"
                    else Consumables.objects.all()
                )
            ),
            "repairs": (
                Repairs.objects.filter(Сотрудник_Логин=user.username)
                if user.Роль != "admin" and user.Роль != "manager"
                else (
                    Repairs.objects.filter(Сотрудник_Компания=user.Организация)
                    if user.Роль == "manager"
                    else Repairs.objects.all()
                )
            ),
            "movements": Movements.objects.all(),
        }

        data = {
            "equipments": EquipmentsSerializer(
                categories["equipments"], many=True
            ).data,
            "programs": ProgramsSerializer(categories["programs"], many=True).data,
            "components": ComponentsSerializer(
                categories["components"], many=True
            ).data,
            "consumables": ConsumablesSerializer(
                categories["consumables"], many=True
            ).data,
            "repairs": RepairsSerializer(categories["repairs"], many=True).data,
            "movements": MovementsSerializer(categories["movements"], many=True).data,
        }

        custom_assets_detail = (
            CustomAssetDetails.objects.filter(Сотрудник_Логин=user.username)
            if user.Роль != "admin" and user.Роль != "manager"
            else (
                CustomAssetDetails.objects.filter(Сотрудник_Компания=user.Организация)
                if user.Роль == "manager"
                else CustomAssetDetails.objects.all()
            )
        )

        custom_assets = CustomAsset.objects.filter(
            id__in=custom_assets_detail.values("Актив")
        )

        custom_assets_data = CustomAssetSerializer(custom_assets, many=True).data
        custom_assets_detail_data = CustomAssetDetailsSerializer(
            custom_assets_detail, many=True
        ).data

        for category in data.values():
            for item in category:
                for key, value in item.items():
                    if isinstance(value, str) and value == "":
                        item[key] = None

        for asset_data in custom_assets_data:
            asset_name = asset_data.get("Название")
            data[asset_name] = custom_assets_detail_data

        return Response(data, status=status.HTTP_200_OK)


# utils for convert and download .csv
def export_assets_to_csv(file_path, model_name):
    model = model_mapping.get(model_name.lower())

    if model:
        data = model.objects.all()
    else:
        custom_assets = CustomAsset.objects.filter(Название=model_name)
        if not custom_assets.exists():
            return f"'{model_name}' не существует."

        data = CustomAssetDetails.objects.filter(Актив__in=custom_assets)

    if not data.exists():
        pass

    # Определяем нужную модель для извлечения полей
    model_class = model if model else CustomAssetDetails
    field_names = [field.name for field in model_class._meta.fields]

    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(field_names)  # Запись заголовков
        writer.writerows([[getattr(item, field) for field in field_names] for item in data])  # Запись данных

    return file_path



def send_file_to_user(file_path, filename):
    if not os.path.exists(file_path):
        raise Http404("Файл не найден.")

    response = FileResponse(open(file_path, "rb"), as_attachment=True)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response["Content-Type"] = "text/csv"

    return response


# import database
class ExportDBView(APIView):
    def get(self, request, *args, **kwargs):
        model_name = request.GET.get("name")  # <-- Получаем параметр из GET-запроса
        
        if not model_name:
            return Response({"error": "Название актива не указано."}, status=400)

        file_path = os.path.join(settings.MEDIA_ROOT, "databases", f"{model_name}.csv")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        exported_file_path = export_assets_to_csv(file_path, model_name)

        if isinstance(exported_file_path, str) and exported_file_path.endswith(".csv"):
            try:
                return FileResponse(open(exported_file_path, "rb"), as_attachment=True, filename=f"{model_name}.csv")
            except FileNotFoundError:
                raise Http404("Файл не найден.")
        else:
            return Response({exported_file_path}, status=200)

# utlis for write to db from .csv
def import_csv_to_db(file_path, model_name, append=False):
    model = model_mapping.get(model_name.lower())

    if model:
        try:
            if not append:
                model.objects.all().delete()  # Удаление только если append=False

            with open(file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                instances = []

                for row in reader:
                    for field in row:
                        date_string = (
                            row[field].strip() if isinstance(row[field], str) else None
                        )

                        if "Дата" in field and isinstance(row[field], str):
                            row[field] = row[field] if row[field].strip() else None
                        else:
                            row[field] = None if date_string == "" else row[field]

                        if "Стоимость" in field or "Номер" in field:
                            if row[field] == "" or row[field] is None:
                                row[field] = None
                            else:
                                try:
                                    row[field] = float(row[field])
                                except ValueError:
                                    print(
                                        f"Ошибка формата числа в строке: {row}. Ожидается числовое значение."
                                    )
                                    row[field] = None
                    try:
                        instance = model(**row)
                        instances.append(instance)
                    except Exception as e:
                        print(
                            f"Ошибка при создании экземпляра модели: {str(e)} для строки: {row}"
                        )

                model.objects.bulk_create(instances)

            return f"Импорт данных в '{model_name}' завершен."

        except Exception as e:
            return f"Произошла ошибка при импорте данных: {str(e)}."

    else:
        asset_name = os.path.splitext(os.path.basename(file_path))[0]
        custom_asset, created = CustomAsset.objects.get_or_create(Название=asset_name)

        if created:
            print(f"Создан новый актив: {asset_name}")
        else:
            print(f"Найден существующий актив: {asset_name}")

        try:
            if not append:
                CustomAssetDetails.objects.filter(Актив=custom_asset).delete()

            with open(file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                instances = []

                for row in reader:
                    for field in row:
                        date_string = (
                            row[field].strip() if isinstance(row[field], str) else None
                        )

                        if "Дата" in field and isinstance(row[field], str):
                            row[field] = row[field] if row[field].strip() else None
                        else:
                            row[field] = None if date_string == "" else row[field]

                        if "Стоимость" in field or "Номер" in field:
                            if row[field] == "" or row[field] is None:
                                row[field] = None
                            else:
                                try:
                                    row[field] = float(row[field])
                                except ValueError:
                                    print(
                                        f"Ошибка формата числа в строке: {row}. Ожидается числовое значение."
                                    )
                                    row[field] = None

                    if "Не_Инвент" not in row or row["Не_Инвент"] in [None, ""]:
                        row["Не_Инвент"] = False

                    try:
                        asset_value = row.pop("Актив", None)
                        instance = CustomAssetDetails(Актив=custom_asset, **row)
                        instances.append(instance)
                    except Exception as e:
                        print(
                            f"Ошибка при создании экземпляра модели: {str(e)} для строки: {row}"
                        )

                CustomAssetDetails.objects.bulk_create(instances)

            return f"Импорт данных для актива '{asset_name}' завершен."

        except Exception as e:
            return f"Произошла ошибка при импорте данных: {str(e)}."


class ImportDBView(APIView):
    queryset = ExportFile.objects.all()
    serializer_class = ExportFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, *args, **kwargs):
        model_name = request.data.get("name")
        file = request.FILES.get("file")

        if not model_name:
            return Response(
                {"error": "Название модели не указано."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not file:
            return Response(
                {"error": "Файл не был загружен."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return self.perform_import(file, model_name)

    def perform_import(self, file, model_name):
        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", f"{model_name}.csv")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        imported_records = import_csv_to_db(file_path, model_name, append=True)  # Передаем флаг append=True

        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Ошибка при удалении файла: {str(e)}.")

        return Response(
            {"detail": f"{imported_records}"},
            status=status.HTTP_201_CREATED,
        )