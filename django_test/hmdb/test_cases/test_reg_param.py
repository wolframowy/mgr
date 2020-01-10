from django.test import TestCase
from django.urls import reverse
import json

from ..models import Metabolite, Spectra, Spectrum, SpectrumArray, MsMs, MsMsPeakArray, MsMsPeak, MetaboliteNames


def create_test_data():
    spectra_list = SpectrumArray(
        spectrum=[
            Spectrum(spectrum_id=4),
            Spectrum(spectrum_id=5)
        ]
    )
    met = Metabolite(id=1, name="1,3-Diaminopropane", monisotopic_molecular_weight=74.1249,
                     spectra=spectra_list, secondary_accessions=None, synonyms=None, accession=['HMDB0000002'])
    met.save()
    spec4_msms = MsMs(
        collision_energy_voltage=10,
        ionization_mode="Positive",
        ms_ms_peaks=MsMsPeakArray(
            ms_ms_peak=[
                MsMsPeak(mass_charge=58.207, intensity=100.0),
                MsMsPeak(mass_charge=75.127, intensity=31.356)
            ]
        )
    )
    spec5_msms = MsMs(
        collision_energy_voltage=25,
        ionization_mode="Negative",
        ms_ms_peaks=MsMsPeakArray(
            ms_ms_peak=[
                MsMsPeak(mass_charge=30.381, intensity=100.0),
                MsMsPeak(mass_charge=41.312, intensity=29.514),
                MsMsPeak(mass_charge=43.217, intensity=21.701),
                MsMsPeak(mass_charge=58.122, intensity=63.889),
                MsMsPeak(mass_charge=74.885, intensity=45.833)
            ]
        )
    )
    spec4 = Spectra(id=4, ms_ms=spec4_msms)
    spec4.save()
    spec5 = Spectra(id=5, ms_ms=spec5_msms)
    spec5.save()

    MetaboliteNames(name="1,3-Diaminopropane", met_id=1, super_class="Organic nitrogen compounds",
                    main_class="Organonitrogen compounds", sub_class="Amines",
                    biospecimen_locations=["Blood", "Feces", "Urine"],
                    monisotopic_molecular_weight=74.08439833).save()
    MetaboliteNames(name="Name2", met_id=2, super_class="Organic nitrogen compounds",
                    main_class="Organonitrogen compounds", sub_class="Amines",
                    biospecimen_locations=["Blood", "Feces", "Urine"],
                    monisotopic_molecular_weight=74.08439833).save()
    MetaboliteNames(name="Name3", met_id=3, super_class="Organic nitrogen compounds",
                    main_class="Organonitrogen compounds", sub_class="Amines",
                    biospecimen_locations=["Blood", "Feces", "Urine"],
                    monisotopic_molecular_weight=74.08439833).save()


class RegParamTest(TestCase):

    def setUp(self):
        create_test_data()

    def tearDown(self):
        Metabolite.objects.all().delete()
        Spectra.objects.all().delete()
        MetaboliteNames.objects.all().delete()

    def test_mock_data_creation(self):
        all_mets = list(Metabolite.objects.all())
        self.assertEqual(all_mets.__len__(), 1)
        all_spectra = list(Spectra.objects.all())
        self.assertEqual(all_spectra.__len__(), 2)

    def test_reg_param_view_get_names_async(self):
        payload = {"type": "names",
                   "value": "Name"}
        response = self.client.get(reverse('hmdb:reg_param_get_async'), payload, content_type='application/json')
        names = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(names.__len__(), 2)

    def test_reg_param_view_get_metabolite_async(self):
        payload = {
            "type": "metabolites",
            "selected_ids": "[1]"      # ids are in a string, because in jquery we need to stringify it
        }
        response = self.client.get(reverse('hmdb:reg_param_get_async'), payload, content_type='application/json')
        met_reg = json.loads(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(met_reg.__len__(), 1)
        self.assertEqual(met_reg[0]['spectra_params']['positive'][0]['reg_param'].__len__(), 2)
        self.assertEqual(met_reg[0]['spectra_params']['negative'][0]['reg_param'].__len__(), 5)

    def test_reg_param_view_get_metabolite_async_404(self):
        payload = {
            "type": "metabolites",
            "minimal_intensity": 30,
            "selected_ids": "[25]"      # ids are in a string, because in jquery we need to stringify it
        }
        response = self.client.get(reverse('hmdb:reg_param_get_async'), payload, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), 'Metabolites not found in database')

    def test_reg_param_view_get(self):
        response = self.client.get(reverse('hmdb:reg_param'))
        self.assertEqual(response.status_code, 200)
