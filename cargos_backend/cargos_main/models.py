from django.db import models


# Create your models here.
class Cargo(models.Model):
    cargo_ID = models.IntegerField(unique=True, primary_key=True)

    row = models.IntegerField()
    elevation = models.IntegerField()
    position = models.IntegerField()

    description = models.CharField(max_length=500)
    title = models.CharField(max_length=200)

    def __str__(self):
        return str(self.cargo_ID) + ": " + str(self.title)
