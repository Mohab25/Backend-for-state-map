from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import roads
class RoadsSerializer(GeoFeatureModelSerializer):
    class Meta: 
        model = roads 
        geo_field = 'geom'
        fields=('med_descri','rtt_descri','f_code_des','isocountry','geom')