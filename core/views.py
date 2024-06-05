from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View, generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from core.form import RentalForm
from .models import Item, Rental
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from datetime import timedelta


@login_required
def rent_item(request, item_id: int) -> Any:
    item = get_object_or_404(Item, pk=item_id)
    rental = Rental(item=item, client=request.user)
    rental.save()

    item.available = False
    item.save()

    return redirect("items_list")


class ItemListView(generic.ListView):
    model = Item
    template_name = "items_list.html"
    context_object_name = "items"

    def get_queryset(self) -> QuerySet[Any]:
        return Item.objects.all().order_by("name")


class ItemCreateView(generic.CreateView):
    model = Item
    fields = ["name", "available"]
    template_name = "item_form.html"
    success_url = "/"


class RentalListView(generic.ListView):
    model = Rental
    template_name = "rental_list.html"
    context_object_name = "rentals"

    def get_queryset(self) -> QuerySet[Any]:
        today = timezone.now().date()
        return Rental.objects.filter(date__gte=today).order_by(
            "date", "period", "period_time"
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        context["today"] = today
        context["tomorrow"] = today + timezone.timedelta(days=1)
        context["today_rentals"] = Rental.objects.filter(date=today).count()
        context["total_rentals"] = Rental.objects.filter(date__gte=today).count()
        context["top_3_users"] = User.objects.annotate(
            rental_count=Count("rental")
        ).order_by("-rental_count")[:3]
        return context


class RentalCreateView(LoginRequiredMixin, generic.CreateView):
    model = Rental
    form_class = RentalForm
    template_name = "rental_form.html"
    success_url = reverse_lazy("core:rental_list")

    WEEKLY_QUOTA = 3

    def form_valid(self, form):
        user = self.request.user
        item = form.cleaned_data.get("item")
        date = form.cleaned_data.get("date")
        period = form.cleaned_data.get("period")
        period_time = form.cleaned_data.get("period_time")

        # Check for conflicting rental on the same date and time
        conflicting_rental = Rental.objects.filter(
            item=item, date=date, period=period, period_time=period_time
        ).first()

        if conflicting_rental:
            conflict_message = (
                f"Conflito: {conflicting_rental.item.name} para {conflicting_rental.client.username} "
                f"no dia {conflicting_rental.date}, {conflicting_rental.get_period_display()} "
                f"na {conflicting_rental.get_period_time_display()} na turma {conflicting_rental.room}."
            )
            form.add_error(None, conflict_message)
            return self.form_invalid(form)

        # Calculate the start and end of the week for the booking date
        start_of_week = date - timedelta(days=date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Count the number of rentals the user has made during the week of the booking date
        weekly_rentals = Rental.objects.filter(
            client=user, date__gte=start_of_week, date__lte=end_of_week
        ).count()

        if weekly_rentals >= self.WEEKLY_QUOTA:
            form.add_error(None, "Você atingiu sua cota semanal de reservas para a semana da data escolhida.")
            return self.form_invalid(form)

        # Save the rental
        rental = form.save(commit=False)

        if user.is_superuser:
            rental.client = form.cleaned_data.get("client")
        else:
            rental.client = user

        rental.save()
        return super().form_valid(form)
      
      

class RentalDeleteView(generic.DeleteView):
    model = Rental
    template_name = "rental_confirm_delete.html"
    success_url = reverse_lazy("core:rental_list")


class RentalEditView(LoginRequiredMixin, generic.UpdateView):
    model = Rental
    form_class = RentalForm
    template_name = "rental_form.html"
    success_url = reverse_lazy("core:rental_list")

    def form_valid(self, form):
        item = form.cleaned_data.get("item")
        date = form.cleaned_data.get("date")
        period = form.cleaned_data.get("period")
        period_time = form.cleaned_data.get("period_time")

        existing_rental = (
            Rental.objects.filter(
                item=item, date=date, period=period, period_time=period_time
            )
            .exclude(pk=self.object.pk)
            .exists()
        )

        if existing_rental:
            form.add_error(None, "Esse agendamento já existe.")
            return self.form_invalid(form)

        rental = form.save(commit=False)

        if self.request.user.is_superuser:
            rental.client = form.cleaned_data.get("client")
        else:
            rental.client = self.request.user
        rental.save()

        return super().form_valid(form)


class CheckConflictView(View):
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        item_id = request.GET.get("item")
        date = request.GET.get("date")
        period = request.GET.get("period")
        period_time = request.GET.get("period_time")

        conflict = Rental.objects.filter(
            item_id=item_id, date=date, period=period, period_time=period_time
        ).first()

        if conflict:
            conflict_message = f"CONFLITO DE AGENDAMENTO: O {conflict.item.name} já foi reservado para {conflict.client.username} neste dia/horário."
            return JsonResponse({"conflict": True, "message": conflict_message})
        else:
            return JsonResponse({"conflict": False})


class CheckQuotaView(View):
    @method_decorator(require_GET)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        user_id = request.GET.get("user_id")
        date_str = request.GET.get("date")

        if not user_id or not date_str:
            return JsonResponse({"quota_reached": False})

        user = User.objects.get(pk=user_id)
        booking_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()

        # Calculate the start and end of the week for the booking date
        start_of_week = booking_date - timedelta(days=booking_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Count the number of rentals the user has made during the week of the booking date
        weekly_rentals = Rental.objects.filter(
            client=user, date__gte=start_of_week, date__lte=end_of_week
        ).count()

        quota_reached = weekly_rentals >= RentalCreateView.WEEKLY_QUOTA

        return JsonResponse({"quota_reached": quota_reached})

