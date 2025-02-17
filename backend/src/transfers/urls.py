from django.urls import path
from .views import TransferRequestView

urlpatterns = [
    path(
        "",
        TransferRequestView.as_view(),
        name="transfer-request-list-create",
    ),
    path(
        "<int:pk>/",
        TransferRequestView.as_view(),
    ),
]
