
class RegistrationParameter:

    def __init__(self, q2_3: float, intensity: float, rel_intensity: float):
        self.q2_3 = q2_3
        self.intensity = intensity
        self.rel_intensity = rel_intensity

    def to_dict(self):
        return self.__dict__


class SpectrumParameter:

    def __init__(self, e: int, ionization_mode: str):
        self.ionization_mode = ionization_mode
        self.e = e
        self.reg_param = []

    def add_reg_param(self, reg_param: RegistrationParameter):
        self.reg_param.append(reg_param)

    def to_dict(self):
        return self.__dict__


def sort_func(x):
    return -1 if x['e'] is None else x['e']


class MetaboliteRegistration:

    def __init__(self, name: str, m_1: float, accession: str):
        self.name = name
        self.m_1 = m_1
        self.accession = accession
        self.spectra_params = {
            'positive': [],
            'negative': [],
            'na': []
        }

    def add_spectrum_param(self, spec_param: SpectrumParameter):
        if spec_param['ionization_mode'] == 'Positive':
            self.spectra_params['positive'].append(spec_param)
        elif spec_param['ionization_mode'] == 'Negative':
            self.spectra_params['negative'].append(spec_param)
        else:
            self.spectra_params['na'].append(spec_param)

    def sort_spectra_params(self):
        self.spectra_params['positive'].sort(key=sort_func)
        self.spectra_params['negative'].sort(key=sort_func)
        self.spectra_params['na'].sort(key=sort_func)
