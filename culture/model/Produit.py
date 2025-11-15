from django.db import models

class Produit(models.Model):
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

    class Meta:
        managed = False
        db_table = 'produit'