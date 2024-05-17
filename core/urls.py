from django.urls import path, include
from .views import (
    ItemListView,
    RentalCreateView,
    RentalDeleteView,
    RentalListView,
    RentalEditView,
)


app_name = "core"
urlpatterns = [
    path("", RentalListView.as_view(), name="rental_list"),
    path("rental/create/", RentalCreateView.as_view(), name="rental_create"),
    path("rental/<int:pk>/delete/", RentalDeleteView.as_view(), name="rental_delete"),
    path("rental/<int:pk>/edit/", RentalEditView.as_view(), name="rental_edit"),
]
