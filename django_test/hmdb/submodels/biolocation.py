from djongo import models


class Biolocation(models.Model):
    name = models.TextField('Biolocation name', max_length=100)

    def __str__(self):
        return "Biolocation"
