from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin

from .models import FuelPrices


class FuelResource(resources.ModelResource):

    class Meta:
        model = FuelPrices
        skip_unchanged = True
        report_skipped = True
        exclude = ['id', 'last_update', 'history', 'slug']


@admin.register(FuelPrices)
class FuelPriceAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = FuelResource
    list_display = ['opis_id', 'truckstop_name', 'city', 'state', 'rack_id', 'retail_price']
    list_display_links = ['opis_id', 'truckstop_name', 'city', 'state', 'rack_id', 'retail_price']
    search_fields = ['opis_id', 'truckstop_name', 'city', 'state', 'rack_id', 'retail_price']
    list_per_page = 100
    show_full_result_count = True
    actions_on_top = True
    actions_on_bottom = True
    save_as = True
    save_as_continue = True
    save_on_top = True
    fieldsets = [
        [
            'Truck ID',
            {
                'classes': ['wide', 'extrapretty'],
                'fields': [('opis_id', 'rack_id')],
            },
        ],
        [
            'Registration Info',
            {
                'classes': ['wide', 'extrapretty'],
                'fields': ['truckstop_name', ('city', 'state')],
            },
        ],
        [
            'Price Info',
            {
                'classes': ['wide', 'extrapretty'],
                'fields': ['retail_price'],
            },
        ],
        [
            'Timestamp',
            {
                'classes': ['wide', 'extrapretty'],
                'fields': ['last_update'],
            },
        ],
    ]
