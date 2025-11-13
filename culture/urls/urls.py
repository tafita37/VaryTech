from django.urls import path

from culture.controllers.ParcelleController import new_parcelle, parcelle_list_page


urlpatterns = [
    path('parcelle_page/', parcelle_list_page, name='parcelle_page'),
    path('new_parcelle/', new_parcelle, name='new_parcelle'),
]