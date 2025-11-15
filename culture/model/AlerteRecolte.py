from django.db import models

from culture.model.Parcelle import Parcelle
from culture.model.Culture import Culture

class AlerteRecolte(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    culture=models.ForeignKey(Culture, models.DO_NOTHING, db_column='culture_id')
    temperatureMin = models.FloatField(db_column='temperature_min')
    temperatureMax = models.FloatField(db_column='temperature_max')
    humiditeMin = models.FloatField(db_column='humidite_min')
    humiditeMax = models.FloatField(db_column='humidite_max')
    vitesseVent = models.FloatField(db_column='vitesse_vent')

    class Meta:
        managed = False
        db_table = 'alerte_recolte'