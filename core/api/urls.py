from django.urls import path

from .views import CalculateRouteAPIView

urlpatterns = [
    path('optimal_route/', CalculateRouteAPIView.as_view(), name='cal_route'),
]
