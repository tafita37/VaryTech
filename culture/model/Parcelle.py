from django.db import models

from culture.model.TypeSol import TypeSol

class Parcelle(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    nom = models.CharField(
        unique=True, 
        max_length=100, 
        db_column='nom'
    )
    photoA = models.CharField(
        max_length=100, 
        db_column='photo_a'
    )
    photoE = models.TextField(
        unique=True, 
        db_column='photo_e'
    )
    superficie = models.FloatField(
        db_column='superficie'
    )
    humiditeMoyenne = models.FloatField(
        db_column='humidite_moyenne',
        null=True
    )
    temperatureMoyenne = models.FloatField(
        db_column='temperature_moyenne',
        null=True
    )
    sol=models.ForeignKey(TypeSol, models.DO_NOTHING, db_column='type_sol_id')

    class Meta:
        managed = False
        db_table = 'parcelle'