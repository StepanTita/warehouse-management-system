from django.db import models


# Create your models here.
class Cargo(models.Model):
    # cargo_ID = models.IntegerField(unique=True, primary_key=True)

    row = models.IntegerField()
    elevation = models.IntegerField()
    position = models.IntegerField()

    height = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    length = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    width = models.DecimalField(decimal_places=2, max_digits=9, default=1)

    description = models.CharField(max_length=500)
    title = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id) + ": " + str(self.title)
