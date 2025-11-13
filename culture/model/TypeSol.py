from django.db import models

class TypeSol(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    nom = models.CharField(
        unique=True, 
        max_length=50, 
        db_column='nom'
    )

    class Meta:
        managed = False
        db_table = 'type_sol'