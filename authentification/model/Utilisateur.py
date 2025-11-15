from django.db import models

from authentification.model.Role import Role


class Utilisateur(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
    )
    nom = models.CharField(
        unique=True, 
        max_length=100, 
        db_column='nom'
    )
    prenom = models.CharField(
        unique=True, 
        max_length=100, 
        db_column='prenom'
    )
    username = models.CharField(
        unique=True, 
        max_length=100, 
        db_column='username'
    )
    password = models.TextField(
        unique=True,  
        db_column='password'
    )
    dateInscription = models.DateTimeField(auto_now_add=True)
    role=models.ForeignKey(Role, models.DO_NOTHING, db_column='role_id')

    class Meta:
        managed = False
        db_table = 'utilisateur'