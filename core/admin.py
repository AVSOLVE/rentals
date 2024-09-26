from django.contrib import admin
from .models import Item, Rental, ExclusionRule

# Register your models here.
admin.site.register(Item)
admin.site.register(Rental)

@admin.register(ExclusionRule)
class ExclusionRuleAdmin(admin.ModelAdmin):
    list_display = ('item', 'weekday', 'period', 'period_time')
    list_filter = ('item', 'weekday', 'period', 'period_time')