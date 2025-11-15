from django.db import models

from culture.model.Culture import Culture
from culture.model.Ressource import Ressource

class CultureRessource(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    culture=models.ForeignKey(Culture, models.DO_NOTHING, db_column='culture_id')
    ressource=models.ForeignKey(Ressource, models.DO_NOTHING, db_column='ressource_id')
    quantiteResource = models.FloatField(db_column='quantite_resource')

    class Meta:
        managed = False
        db_table = 'culture_ressource'