from django.urls import path

from culture.controllers.ParcelleController import culture_detail_page, culture_list_page, new_culture, new_parcelle, new_recolte, parcelle_list_page

urlpatterns = [
    path('parcelle_page/', parcelle_list_page, name='parcelle_page'),
    path('new_parcelle/', new_parcelle, name='new_parcelle'),
    path('culture_page/<int:parcelle_id>/', culture_list_page, name='culture_page'),
    path('culture_detail_page/<int:culture_id>/', culture_detail_page, name='culture_detail_page'),
    path('new_culture/', new_culture, name='new_culture'),
    path('new_recolte/', new_recolte, name='new_recolte'),
]