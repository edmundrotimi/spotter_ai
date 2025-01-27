from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Spotter AI Remote',
        default_version='v1',
        description='Spotter AI',
        terms_of_service='http://127.0.0.1:8000',
        contact=openapi.Contact(
            name='Edmund Rotimi', url='https://github.com/edmundrotimi/', email='edmundrotimi@gmail.com'
        ),
        license=openapi.License(
            name='MIT License', url='https://github.com/edmundrotimi/spotter_ai/blob/main/LICENSE'
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
