import random

from django import template
from django.db.models import F
from django.db.models.functions import ExtractSecond
from django.utils import timezone
from django.utils.timezone import timedelta
from pytz import timezone as tz  # type: ignore

from core.fuel.models import FuelPrices  # type: ignore

# init register
register = template.Library()

# get the current time in UTC
utc_now = timezone.now()
# convert the current time to the local time zone
arizona = tz('US/Arizona')
current_timestamp = utc_now.astimezone(arizona)

# days computations in local johannesburg time
# each count include current day
previous_27_days_from_today = timezone.localtime(current_timestamp - timedelta(days=27))


@register.filter(name='prices_chart_data')
def prices_chart_data(value='price'):

    # Extract the second since the instaces where imported
    # they will have same minutes and hours.
    # ExtractSecond offers better performace

    # init holding list
    holding_list = [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0],
                    [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]]

    if FuelPrices.objects.all().exists():
        min_value = 0
        max_value = FuelPrices.objects.all().count() - 24

        # range for random prices
        starter_num = random.randint(min_value, max_value)
        end_num = starter_num + 24 if starter_num + 24 > FuelPrices.objects.all().count() else FuelPrices.objects.all(
        ).count()

        recent_prices = (
            FuelPrices.objects.annotate(second=ExtractSecond('timestamp')
                                        ).values('second').annotate(price=F('retail_price')
                                                                    ).order_by('second')[starter_num:end_num]
        )

        # init holding list
        for entry in recent_prices:
            holding_list[entry['second']][1] = entry['price']

    return holding_list
