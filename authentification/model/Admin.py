from django.db import models

class Admin(models.Model):
    id = models.AutoField(
        primary_key=True, 
        db_column='id'
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

    class Meta:
        managed = False
        db_table = 'admin'