from django.urls import path
from forms.views import (
    InventoryLabelPdfView,
    EquipmentReportView,
    BrokenEquipmentReportView,
    TemporaryEquipmentReportView,
)

urlpatterns = [
    path("invent/", InventoryLabelPdfView.as_view(), name="forms-invent"),
    path("reception/", EquipmentReportView.as_view(), name="forms-reception"),
    path(
        "reception/broken/",
        BrokenEquipmentReportView.as_view(),
        name="forms-reception-broken",
    ),
    path(
        "reception/temp/",
        TemporaryEquipmentReportView.as_view(),
        name="forms-reception-temp",
    ),
]
