from django.db import models

from culture.model.Parcelle import Parcelle
from culture.model.Produit import Produit

class Culture(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    produit=models.ForeignKey(Produit, models.DO_NOTHING, db_column='produit_id')
    parcelle=models.ForeignKey(Parcelle, models.DO_NOTHING, db_column='parcelle_id')
    dateSemis = models.DateTimeField(auto_now_add=True, db_column='date_semis')
    dateRecoltePrevu = models.DateTimeField(db_column='date_recolte_prevu', null=True)
    dateRecolteReelle = models.DateTimeField(db_column='date_recolte_reelle', null=True)
    rendementEstime = models.FloatField(db_column='rendement_estime')
    rendementReel = models.FloatField(db_column='rendement_reel')
    quantiteSemee = models.FloatField(db_column='quantite_semee')
    photoA = models.CharField(
        max_length=100, 
        db_column='photo_a'
    )
    photoE = models.TextField(
        unique=True, 
        db_column='photo_e'
    )

    class Meta:
        managed = False
        db_table = 'culture'