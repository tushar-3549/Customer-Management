from django.urls import path

from .views import (
    CustomerListCreateAPIView,
    CustomerRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path(
        "customers/",
        CustomerListCreateAPIView.as_view(),
        name="customer-list-create",
    ),
    path(
        "customers/<int:pk>/",
        CustomerRetrieveUpdateDeleteAPIView.as_view(),
        name="customer-detail",
    ),
]