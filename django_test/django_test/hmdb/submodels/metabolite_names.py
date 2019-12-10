from djongo import models


class MetaboliteNames(models.Model):
    name = models.TextField('Metabolite name', max_length=100)
    met_id = models.PositiveIntegerField('Metabolite ID')

    class Meta:
        db_table = 'hmdb_met_names'

    def __str__(self):
        return "Metabolite names"
