import datetime

from djongo import models


class MsMsPeak(models.Model):

    id = models.PositiveIntegerField('Peak ID')
    ms_ms_id = models.PositiveIntegerField('Spectrum ID')
    mass_charge = models.FloatField('Mass charge')
    intensity = models.FloatField('Intensity')
    molecule_id = models.PositiveIntegerField('Molecule ID')

    class Meta:
        abstract = True


class MsMsPeakArray(models.Model):

    ms_ms_peak = models.ArrayModelField(
        model_container=MsMsPeak
    )

    class Meta:
        abstract = True


class Reference(models.Model):

    id = models.PositiveIntegerField('Reference ID')
    spectra_id = models.PositiveIntegerField('Spectra ID')
    spectra_type = models.TextField('Spectra type', max_length=10)
    pubmed_id = models.PositiveIntegerField('Pubmed ID')
    ref_text = models.TextField('Reference text', max_length=1000)
    database = models.TextField('Database', max_length=50)
    database_id = models.TextField('Database id', max_length=10)

    class Meta:
        abstract = True


class ReferenceArray(models.Model):
    reference = models.ArrayModelField(
        model_container=Reference
    )

    class Meta:
        abstract = True


class MsMs(models.Model):
    collection_date = models.DateField('Collection date')
    collision_energy_level = models.TextField('Collision energy level', max_length=20)
    collision_energy_voltage = models.PositiveSmallIntegerField('Collision energy voltage')
    created_at = models.DateTimeField('Created at')
    database_id = models.TextField('Database id', max_length=20)

    # Energy field is null everywhere
    energy_field = models.TextField('Energy field', max_length=20, blank=True)
    id = models.PositiveIntegerField('Spectrum id')
    instrument_type = models.TextField('Instrument type', max_length=50)
    ionization_mode = models.TextField('Ionization mode', max_length=10)

    # Mono mass is null everywhere
    mono_mass = models.FloatField('Mono mass')

    ms_ms_peaks = models.EmbeddedModelField(
        model_container=MsMsPeakArray
    )

    notes = models.TextField('Notes', max_length=1000)
    peak_counter = models.PositiveIntegerField('Peak count')
    predicted = models.BooleanField('Is predicted?')

    references = models.EmbeddedModelField(
        model_container=ReferenceArray
    )

    sample_assessment = models.TextField('Sample assessment', max_length=20)
    sample_concentration = models.FloatField('Sample concentration')
    sample_concentration_units = models.TextField('Sample concentration units', max_length=10)
    sample_mass = models.FloatField('Sample mass')
    sample_mass_units = models.TextField('Sample mass units', max_length=10)

    # Sample source is null everywhere
    sample_source = models.TextField('Sample source', max_length=50)

    # Solvent is null everywhere
    solvent = models.TextField('Solvent', max_length=50)
    spectra_assessment = models.TextField('Spectra assessment', max_length=50)
    splash_key = models.TextField('Splash key', max_length=100)
    structure_id = models.PositiveIntegerField('Structure id')
    updated_at = models.DateTimeField('Updated at')

    class Meta:
        abstract = True


class Spectra(models.Model):

    ms_ms = models.EmbeddedModelField(
        model_container=MsMs
    )

    # TODO
    # Change __str__ function and add other functions
    def __str__(self):
        return "Spectra test"
