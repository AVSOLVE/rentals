from django.urls import path
from .views import (
    RentalCreateView,
    RentalDeleteView,
    RentalListView,
    RentalEditView,
    CheckConflictView
)


app_name = "core"
urlpatterns = [
    path("", RentalListView.as_view(), name="rental_list"),
    path("rental/create/", RentalCreateView.as_view(), name="rental_create"),
    path("rental/<int:pk>/delete/", RentalDeleteView.as_view(), name="rental_delete"),
    path("rental/<int:pk>/edit/", RentalEditView.as_view(), name="rental_edit"),
    path('check-conflict/', CheckConflictView.as_view(), name='check_conflict'),
]
