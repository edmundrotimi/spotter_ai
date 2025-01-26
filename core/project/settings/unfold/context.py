from django.db.models import Max, Min, Sum

from core.fuel.models import FuelPrices
from core.project.settings import ADMIN_PATH


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """

    context.update({
        'fuel_prices':
            FuelPrices.objects.all().annotate(
                max_price=Max('retail_price'), min_price=Min('retail_price'), total_price=Sum('retail_price')
            ),
        'admin_path':
            ADMIN_PATH
    },)

    return context
