from django.test import TestCase
from django.urls import reverse

from ..models import Metabolite, Spectra, Spectrum, SpectrumArray, MsMs, MsMsPeakArray, MsMsPeak


def create_test_data():
    spectra_list = SpectrumArray(
        spectrum=[
            Spectrum(spectrum_id=4),
            Spectrum(spectrum_id=5)
        ]
    )
    met = Metabolite(id=1, name="1,3-Diaminopropane", average_molecular_weight=74.1249,
                     spectra=spectra_list, secondary_accessions=None, synonyms=None, )
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


class RegParamTest(TestCase):

    def setUp(self):
        create_test_data()

    def tearDown(self):
        Metabolite.objects.filter(id=1).delete()
        Spectra.objects.filter(id__in=[4, 5]).delete()

    def test_mock_data_creation(self):
        all_mets = list(Metabolite.objects.all())
        self.assertEqual(all_mets.__len__(), 1)
        all_spectra = list(Spectra.objects.all())
        self.assertEqual(all_spectra.__len__(), 2)

    def test_reg_param_view_post(self):
        payload = {
            "minimal_intensity": 30,
            "selected_ids": [1]
        }
        response = self.client.post(reverse('hmdb:reg_param'), payload, content_type='application/json')
        met_reg = response.context['met_reg']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(met_reg.__len__(), 1)
        self.assertEqual(met_reg[0].registration_params.__len__(), 5)

    def test_reg_param_view_post_404(self):
        payload = {
            "minimal_intensity": 30,
            "selected": [
                {"name": "1,3-Diaminopropane",
                 "id": 25}
            ]
        }
        response = self.client.post(reverse('hmdb:reg_param'), payload, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content.decode(), 'Metabolites not found in database')

    def test_reg_param_viet_get(self):
        response = self.client.get(reverse('hmdb:reg_param'))
        self.assertEqual(response.status_code, 200)
