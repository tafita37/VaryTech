from django.db import models

from culture.model.Parcelle import Parcelle
from culture.model.Produit import Produit

class AlerteCulture(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    produit=models.ForeignKey(Produit, models.DO_NOTHING, db_column='produit_id')
    temperatureMin = models.FloatField(db_column='temperature_min')
    temperatureMax = models.FloatField(db_column='temperature_max')
    humiditeMin = models.FloatField(db_column='humidite_min')
    humiditeMax = models.FloatField(db_column='humidite_max')
    vitesseVent = models.FloatField(db_column='vitesse_vent')

    class Meta:
        managed = False
        db_table = 'alerte_culture'