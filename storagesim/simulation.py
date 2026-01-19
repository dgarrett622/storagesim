import numpy as np
from scipy.integrate import solve_ivp


class Simulator:
    """
    Simulates heat transfer from a solar panel to a storage tank

    The fluid used is water, adjustable parameters are:
    :param ta: transmittance-absorptance of solar panel
    :param f_r: heat removal factor of solar panel
    :param panel_area: area of solar panel in m**2
    :param panel_loss: solar panel loss factor in W/(m**2 * K)
    :param g: solar irradiance in W / m**2
    :param t_a: ambient temperature in Celsius
    :param m_dot: mass flow rate of water in kg / s
    :param tank_volume: storage tank volume in liters
    :param tank_temp: storage tank initial temperature in Celsius
    :param tank_loss: storage tank loss coefficient in W / K
    """

    def __init__(
        self,
        ta: float = 0.85,
        f_r: float = 0.85,
        panel_area: float = 1.5,
        panel_loss: float = 3.0,
        g: float = 500.0,
        t_a: float = 20.0,
        m_dot: float = 0.02,
        tank_volume: float = 150,
        tank_temp: float = 15.0,
        tank_loss: float = 5.0,
    ):
        self.ta = ta
        self.f_r = f_r
        self.panel_area = panel_area
        self.panel_loss = panel_loss
        self.g = g
        self._t_a = t_a
        self.m_dot = m_dot
        self.tank_volume = tank_volume
        self._tank_temp = tank_temp
        self.tank_loss = tank_loss

        # water constants
        self.water_density = 1000  # kg/m**3
        self.water_cp = 4180  # J/(kg * K)

        # derived quantities
        self.tank_mass = self.tank_volume / 1000 * self.water_density  # kg

    @property
    def t_a(self):
        """Ambient temperature in Kelvin"""
        return self._t_a + 273.15

    @property
    def tank_temp(self):
        """Tank temperature in Kelvin"""
        return self._tank_temp + 273.15

    def ode(self, t, y):
        """
        ODE for the simulation

        :param t: time
        :param y: tank temperature in Kelvin
        """
        # usable heat from solar panel (Hottel-Whillier model)
        q_c = self.panel_area * (
            self.f_r * self.ta * self.g - self.f_r * self.panel_loss * (y - self.t_a)
        )

        # temperature at outlet of solar panel
        t_out = y + q_c / (self.m_dot * self.water_cp)

        dy_dt = (1.0 / (self.tank_mass * self.water_cp)) * (
            self.m_dot * self.water_cp * (t_out - y) - self.tank_loss * (y - self.t_a)
        )
        # print(f"dy_dt: {dy_dt}")

        return dy_dt

    def solve_ivp(
        self, duration: float, t_eval: np.ndarray = None
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Solves the ODE

        :param duration: how long in seconds to perform simulation
        :param t_eval: desired time points from solve (optional)
        :return: time and tank temperature (in Celsius) arrays
        """
        sol = solve_ivp(
            self.ode, t_span=[0, duration], y0=np.array([self.tank_temp]), t_eval=t_eval
        )

        return sol.t, sol.y - 273.15


if __name__ == "__main__":
    sim = Simulator()
    t, y = sim.solve_ivp(duration=14 * 24 * 3600)
    print(f"time: {t}")
    print(f"tank temp: {y}")
