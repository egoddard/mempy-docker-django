from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Amenity


class AmenitySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Amenity
        geo_field = "geometry"
        fields = (
            'id',
            'osm_id',
            'name',
            'amenity_type',
        )
