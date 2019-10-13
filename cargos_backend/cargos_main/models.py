from django.db import models
import datetime as dt


# Create your models here.
class Cell(models.Model):
    row = models.IntegerField()
    elevation = models.IntegerField()  # y
    position = models.IntegerField()  # x

    height = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    length = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    width = models.DecimalField(decimal_places=2, max_digits=9, default=1)

    class Meta:
        unique_together = (('row', 'elevation', 'position'),)

    def __str__(self):
        return 'r: ' + str(self.row) + ' e: ' + str(self.elevation) + ' p: ' + str(self.position)


class Cargo(models.Model):
    # cargo_ID = models.IntegerField(unique=True, primary_key=True)

    # row = models.IntegerField()
    # elevation = models.IntegerField()
    # position = models.IntegerField()
    cell = models.ForeignKey(Cell, on_delete=models.CASCADE, default=1)

    height = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    length = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    width = models.DecimalField(decimal_places=2, max_digits=9, default=1)

    description = models.CharField(max_length=500)
    title = models.CharField(max_length=200)

    date_added = models.DateTimeField(auto_now=True)
    date_dated = models.DateField(default=dt.datetime.now)

    def __str__(self):
        return str(self.id) + ": " + str(self.title)
