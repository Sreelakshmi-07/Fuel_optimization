from django.urls import path
from . import views

urlpatterns = [
    path('fuel-route/', views.fetch_route_from_ors, name='fuel-route'),
    path('map/', views.map_view, name='map'),
]
