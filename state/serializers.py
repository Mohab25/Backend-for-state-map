from rest_framework_gis import serializers
from .models import PAU, ShortestPath

class PAUSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = PAU
        geo_field='geom'
        id_field='objectid_1'
        fields = '__all__'

class ShortestPathSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model=ShortestPath
        geo_field='geom'
        fields='__all__'
