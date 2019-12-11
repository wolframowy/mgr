
class RegistrationParameter:

    def __init__(self, q2_3: float, e: int, intensity: float, ionization_mode: str):
        self.q2_3 = q2_3
        self.e = e
        self.intensity = intensity
        self.ionization_mode = ionization_mode

    def to_json(self):
        return self.__dict__


class MetaboliteRegistration:

    def __init__(self, name: str, m_1: float):
        self.name = name
        self.m_1 = m_1
        self.registration_params = []

    def add_reg_param(self, reg_param: RegistrationParameter):
        self.registration_params.append(reg_param)

