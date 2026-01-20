import unittest

import numpy as np
import numpy.testing as npt

from storagesim.simulation import Simulator


class TestSimulator(unittest.TestCase):
    """Various test cases for Simulator class"""

    def test_temp_increase(self):
        """Test that g > 0 results in temperature rise"""
        sim = Simulator()
        # get every 5 minutes for an hour
        t_eval = np.arange(0, 3600, 5 * 60)
        t, y = sim.solve_ivp(duration=3600, t_eval=t_eval)
        npt.assert_array_less(
            0, np.diff(y), err_msg="Storage tank temperature did not increase"
        )

    def test_no_g_no_loss(self):
        """
        Test that with no solar irradiance and no tank loss
        the temperature exponentially approaches ambient
        """
        sim = Simulator()
        sim.g = 0
        sim.tank_loss = 0
        sim._t_a = 30
        sim._tank_temp = 20
        t_eval = np.arange(0, 3600, 5)
        true_T = sim._t_a + (sim._tank_temp - sim._t_a) * np.exp(
            -sim.panel_loss
            * sim.panel_area
            * sim.f_r
            * t_eval
            / (sim.tank_mass * sim.water_cp)
        )
        t, T = sim.solve_ivp(duration=3600, t_eval=t_eval)
        npt.assert_array_almost_equal(
            T,
            true_T,
            decimal=9,
            err_msg="Exponential temperature increase not seen",
        )

    def test_no_losses(self):
        """
        Test that total energy is equal when there are no losses anywhere
        """
        sim = Simulator()
        sim.panel_loss = 0
        sim.tank_loss = 0
        t, T = sim.solve_ivp(duration=3600)
        true_energy = sim.panel_area * sim.f_r * sim.ta * sim.g * (3600)
        test_energy = sim.tank_mass * sim.water_cp * (T[-1] - T[0])
        self.assertAlmostEqual(
            test_energy, true_energy, places=6, msg="Energy not conserved"
        )

    def test_no_flow(self):
        """
        Test when there is no flow
        """
        # should exponentially approach ambient
        sim = Simulator()
        sim.m_dot = 0
        t_eval = np.arange(0, 3600, 5)
        t, T = sim.solve_ivp(duration=3600, t_eval=t_eval)
        true_T = sim._t_a + (sim._tank_temp - sim._t_a) * np.exp(
            -sim.tank_loss * t_eval / (sim.tank_mass * sim.water_cp)
        )
        npt.assert_array_almost_equal(
            true_T,
            T,
            6,
            err_msg="No flow case did not exponentially approach ambient",
        )
