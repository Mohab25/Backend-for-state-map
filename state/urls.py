from django.urls import path,re_path 
from . import views 
urlpatterns=[
    re_path(r'paus/$',views.PAUListView.as_view(),name='pau-list'), 
    re_path(r'closest_healthcare/$',views.ClosestFacility,name='closest-healthcare')
]