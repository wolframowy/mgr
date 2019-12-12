
class RegistrationParameter:

    def __init__(self, q2_3: float, intensity: float):
        self.q2_3 = q2_3
        self.intensity = intensity

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


class MetaboliteRegistration:

    def __init__(self, name: str, m_1: float):
        self.name = name
        self.m_1 = m_1
        self.spectra_params = []

    def add_spectrum_param(self, spec_param: SpectrumParameter):
        self.spectra_params.append(spec_param)

