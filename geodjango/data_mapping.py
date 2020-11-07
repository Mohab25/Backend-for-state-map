from django.contrib.gis.utils import LayerMapping
from .models import roads
import os 

roads_mapping = {
    'med_descri': 'MED_DESCRI',
    'rtt_descri': 'RTT_DESCRI',
    'f_code_des': 'F_CODE_DES',
    'iso': 'ISO',
    'isocountry': 'ISOCOUNTRY',
    'geom': 'MULTILINESTRING',
}
path = os.path.abspath(os.path.join(os.path.dirname(__file__),'Diva_SDN_rds/SDN_roads.shp'))

def load():
    layer = LayerMapping(roads,path,roads_mapping)
    layer.save(strict=True,verbose=True)