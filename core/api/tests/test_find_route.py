# flake8: noqa

import json
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from django.urls import reverse


class CalculateRouteAPITest(TestCase):

    def setUp(self):
        self.client = Client()

        # endpoint url path
        self.url = reverse('cal_route')

        # init sample data
        self.valid_payload = {"start": "28.61141,77.21833", "finish": "53.80186,21.56218"}

    # mock the OpenRouteService API call and ML model loading
    @patch('core.api.utils.find_routes.get_route')
    @patch('core.api.utils.load_csv.pandas_load_csv')
    def test_calculate_route_success(self, mock_joblib_load, mock_get_route):
        # Mock API response
        mock_get_route.return_value = {
            "features": [{
                "geometry": {
                    "coordinates": [[77.21833, 28.61141], [21.56218, 53.80186]]
                }
            }]
        }

        # mock ml model prediction
        mock_model = MagicMock()
        # predict a cost effective fuel stop
        mock_model.predict.return_value = [1]
        mock_joblib_load.return_value = mock_model

        # API request
        response = self.client.post(self.url, data=json.dumps(self.valid_payload), content_type='application/json')

        # response status code
        self.assertEqual(response.status_code, 200)

        # assert response
        response_data = response.json()
        self.assertIn('valid_route_points', response_data)
        self.assertIn('optimal_stations', response_data)
        self.assertIn('total_cost', response_data)
        self.assertIn('map_link', response_data)

    def test_calculate_route_invalid_request_method(self):
        # perform a GET request (invalid method)
        response = self.client.get(self.url)

        # assert response status code
        self.assertEqual(response.status_code, 405)

        # assert error message
        self.assertEqual(response.json()['detail'], 'Method "GET" not allowed.')

    def test_calculate_route_missing_fields(self):
        # POST request with missing finish input field
        invalid_payload = {"start": "40.7128,-74.0060"}
        response = self.client.post(self.url, data=json.dumps(invalid_payload), content_type="application/json")

        # assert response
        self.assertEqual(response.status_code, 400)
        # assert error
        self.assertEqual(response.json()['finish'][0], 'This field is required.')
