from .models import Item, Rental
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = "__all__"


class RentalForm(ModelForm):

    item = forms.ModelChoiceField(
        queryset=Item.objects.filter(available=True), required=True
    )
    period = forms.ChoiceField(
        choices=Rental.PERIOD_CHOICES, required=True, widget=forms.Select
    )
    period_time = forms.ChoiceField(
        choices=Rental.CLASSES_CHOICES, required=True, widget=forms.Select
    )
    client = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))

    class Meta:
        model = Rental
        exclude = ['client']
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
