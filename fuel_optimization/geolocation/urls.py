from django.urls import path
from . import views

urlpatterns = [
    path('fuel-route/', views.fuel_route_api, name='fuel-route'),
]
