from django.contrib.gis.db import models


class Amenity(models.Model):
    osm_id = models.BigIntegerField()
    name = models.TextField(blank=True)
    amenity_type = models.CharField(max_length=30)
    geometry = models.PointField(srid=4326)
