from djongo import models


class MetaboliteNames(models.Model):
    name = models.TextField('Metabolite name', max_length=100)
    met_id = models.PositiveIntegerField('Metabolite ID')
    super_class = models.TextField('Super class', max_length=100)
    main_class = models.TextField('Class', max_length=100)
    sub_class = models.TextField('Sub class', max_length=100)
    biospecimen_locations = models.ListField('Biospecimen location')
    monisotopic_molecular_weight = models.FloatField('Monisotopic molecular weight')

    class Meta:
        db_table = 'hmdb_met_names'

    def __str__(self):
        return "Metabolite names"
