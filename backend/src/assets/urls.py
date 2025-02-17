from django.urls import path
from .views import (
    CustomAssetViewSet,
    CustomAssetDetailsViewSet,
    EquipmentsViewSet,
    ExportDBView,
    ImportDBView,
    ProgramsViewSet,
    ComponentsViewSet,
    ConsumablesViewSet,
    RepairsViewSet,
    MovementsViewSet,
    AssetsListView,
)


urlpatterns = [
    path("", AssetsListView.as_view(), name="assets-list"),
    path(
        "equipments/",
        EquipmentsViewSet.as_view({"get": "list", "post": "create"}),
        name="equipment-list",
    ),
    path(
        "equipments/<int:pk>/",
        EquipmentsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="equipment-detail",
    ),
    path(
        "programs/",
        ProgramsViewSet.as_view({"get": "list", "post": "create"}),
        name="program-list",
    ),
    path(
        "programs/<int:pk>/",
        ProgramsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="program-list",
    ),
    path(
        "repairs/",
        RepairsViewSet.as_view({"get": "list", "post": "create"}),
        name="repair-list",
    ),
    path(
        "repairs/<int:pk>/",
        RepairsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="repair-list",
    ),
    path(
        "components/",
        ComponentsViewSet.as_view({"get": "list", "post": "create"}),
        name="component-list",
    ),
    path(
        "components/<int:pk>/",
        ComponentsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="component-list",
    ),
    path(
        "consumables/",
        ConsumablesViewSet.as_view({"get": "list", "post": "create"}),
        name="consumable-list",
    ),
    path(
        "consumables/<int:pk>/",
        ConsumablesViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="consumable-list",
    ),
    path(
        "movements/",
        MovementsViewSet.as_view({"get": "list", "post": "create"}),
        name="movement-list",
    ),
    path(
        "movements/<int:pk>/",
        MovementsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="movement-list",
    ),
    path(
        "custom/",
        CustomAssetViewSet.as_view({"get": "list", "post": "create"}),
        name="custom-asset",
    ),
    path(
        "custom/<int:pk>/",
        CustomAssetViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="custom-asset",
    ),
    path(
        "custom/<str:name>/",
        CustomAssetDetailsViewSet.as_view({"get": "list", "post": "create"}),
        name="custom-asset-list",
    ),
    path(
        "custom/<str:name>/<int:pk>/",
        CustomAssetDetailsViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="custom-asset-list",
    ),
    path(
        "import/",
        ImportDBView.as_view(),
        name="import_db",
    ),
    path(
        "export/",
        ExportDBView.as_view(),
        name="export_db",
    ),
]
