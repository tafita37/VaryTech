from django.db import models

from culture.model.Unite import Unite

class Ressource(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    nom = models.CharField(
        unique=True, 
        max_length=50, 
        db_column='nom'
    )
    prix = models.FloatField(
        unique=True, 
        db_column='prix'
    )
    unite=models.ForeignKey(Unite, models.DO_NOTHING, db_column='unite_id')

    class Meta:
        managed = False
        db_table = 'ressource'