from django.db import models

from culture.model.Culture import Culture

class Recolte(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    culture=models.ForeignKey(Culture, models.DO_NOTHING, db_column='culture_id')
    dateRecolte = models.DateTimeField(auto_now_add=True, db_column='date_recolte')
    quantiteRecoltee = models.FloatField(db_column='quantite_recoltee')

    class Meta:
        managed = False
        db_table = 'recolte'