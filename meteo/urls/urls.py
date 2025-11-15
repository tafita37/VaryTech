from django.urls import path

from meteo.controllers.MeteoController import meteo_prediction_page

urlpatterns = [
    path('meteo_prediction_page/', meteo_prediction_page, name='meteo_prediction_page'),
]