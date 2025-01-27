import os

import joblib
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.project.settings import BASE_DIR

from .serializers.routs import RouteRequestSerializer
from .utils.find_routes import get_route
from .utils.map_link import generate_map_link
from .utils.station_optimality_with_ml import find_optimal_stations_ml

# init trained ML mode path
model_path = os.path.join(BASE_DIR, 'core/fuel/utils/fuel_stop_model.pkl')


class CalculateRouteAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        # input validtion
        serializer = RouteRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # validated data
        validated_data = serializer.validated_data
        start = validated_data['start'].split(',')
        finish = validated_data['finish'].split(',')

        try:
            # get route
            route = get_route(start, finish)

            route_coordinates = route['features'][0]['geometry']['coordinates']

            # load ML trained model
            model = joblib.load(model_path)

            # find an optimal stations using ML
            optimal_stations, total_cost, valid_route_points = find_optimal_stations_ml(route_coordinates, model)

            # response
            response = {
                'valid_route_points': valid_route_points,
                'optimal_stations': optimal_stations,
                'total_cost': total_cost,
                'map_link': generate_map_link(valid_route_points)
            }

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
