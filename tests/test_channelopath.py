import numpy as np
from hh_model.channelopathy import scaled_conductances, fhn_parameter_mapping, hh_derivatives_channelopathy, fhn_derivative_channelopathy
from hh_model.constants import g_Na, g_K

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

def test_scaled_conductances_scale():
    conductances = scaled_conductances(g_Na, 0.7, g_K, 0.7)
    assert np.isclose(0.7 * g_Na, conductances["g_Na_scaled"])
    assert np.isclose(0.7 * g_K, conductances["g_K_scaled"])


def test_fhn_parameter_mapping():
    conductances = scaled_conductances(g_Na, 0.7, g_K, 0.7)
    g_Na_scaled = conductances["g_Na_scaled"]
    g_K_scaled = conductances["g_K_scaled"]
    parameters = fhn_parameter_mapping(g_Na_scaled, g_K_scaled, 0.7, 0.8, 0.08)
    assert np.isclose(0.7 / g_Na_scaled, parameters["a_scaled"])
    assert np.isclose(0.8 * g_K_scaled, parameters["b_scaled"])
    assert np.isclose(0.08/(0.77 * g_Na_scaled + 0.23 * g_K_scaled), parameters["eps_scaled"])


def test_hh_derivatives_channelopathy():