"""
Calculate the amount of time to apply mist to raise the rH from Ho% to Ht%
for a given volume of air assuming const temp (25 C).
"""

import math

class MistModel:
    """Mist model class

    Provide the mist flow rate in ml per second.

    Provide the volume of air to humidify in cubic meters.

    Provide the current rH in percent.
    """

    def __init__(self):
        # rH setpoint
        self.target = 0.8
        # mist rate (ml/s)
        self.rate = 2.5
        # atmospheric pressure in kPa
        self.pressure = 100.0
        # volume of air in m^3
        self.volume = 0.11

    def rh_to_sec(self, rh):
        # initial partial pressure in kilopascals
        e1 = rh * 3.17
        # target partial pressure in kilopascals
        e2 = self.target * 3.17

        w = 0.622 * self.pressure * (e2 - e1) / (self.pressure - e1)

        return w

if __name__ == "__main__":
    m = MistModel()
    print(m.rh_to_sec(0.5))
