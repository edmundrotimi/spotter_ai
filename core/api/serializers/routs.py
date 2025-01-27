from rest_framework import serializers


class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(help_text="start location must be in 'lat,lng' eg 40.7128,-74.0060")
    finish = serializers.CharField(help_text="finish location must be in 'lat,lng' eg 34.0522,-118.2437")

    def validate_start(self, value):
        if ',' not in value:
            raise serializers.ValidationError("Start location must be in 'lat,lng' format with valid numbers.")

        return value

    def validate_finish(self, value):
        if ',' not in value:
            raise serializers.ValidationError("Finish location must be in 'lat,lng' format with valid numbers.")

        return value
