from django.shortcuts import render 
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from . import conn
from . import conn_optimized as con
from .models import PAU,ShortestPath
from .serializers import PAUSerializer,ShortestPathSerializer
from rest_framework import generics

@api_view(['GET','POST'])
def ClosestFacility(req):
    coords = req.data  #getting data from fetch about map coords, it's parsed automatically thanks to @api_view
    value = con.geom_as_json(coords)
    # legacy code 
    # value = conn.get_shortestPath(coords)
    # #serialize the value here 
    # line = ShortestPath(pathid=1,geom=value)
    # line.save()
    # line_serial = ShortestPathSerializer(line)
    # print(line_serial.data)
    
    
    return Response(value)
    # what this function returns should be a geometry and an id, a model of dijkstra 
    # resuts function follows such a schema. 
    
    # for i in values:
    #     id = i[0]
    #     geom=i[1]
    # return HttpResponse(f'id:{id} \n geom:{geom}')

class PAUListView(generics.ListCreateAPIView):
    queryset = PAU.objects.all()
    serializer_class = PAUSerializer


