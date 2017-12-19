from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter
from .models import Amenity
from .serializers import AmenitySerializer


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    # Configure the bbox filter, filter backends, and fields to filter on
    bbox_filter_field = 'geometry'
    bbox_filter_include_overlapping = True
    filter_backends = (
        DjangoFilterBackend,
        InBBoxFilter,
    )
    filter_fields = ('name', 'amenity_type')

    # change all objects to filter()
    queryset = Amenity.objects.filter()
    serializer_class = AmenitySerializer
