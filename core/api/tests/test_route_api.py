# flake8: noqa

from django.test import TestCase, tag

from core.api.utils.find_routes import get_route


class RouteAPITests(TestCase):

    @tag('integration')
    def test_real_route(self):
        # An integration test with a real API call
        start = [40.7128, -74.0060]
        finish = [34.0522, -118.2437]
        response = get_route(start, finish)
        self.assertIn('features', response)
