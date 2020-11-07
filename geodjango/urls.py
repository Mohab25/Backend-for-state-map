from django.urls import path,re_path
from .views import RoadListView,RoadDetail

urlpatterns=[
    path('',RoadListView.as_view(),name=RoadListView.name),
    re_path(r'(?P<pk>\d+)/$',RoadDetail.as_view(),name=RoadDetail.name),
]