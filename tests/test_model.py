from hh_model.model import hh_derivatives
from hh_model.integrators import rk4_integrate
from hh_model.kinetics import steady_state
from hh_model.stimuli import step_current
import numpy as np

def test_steady_state_gates_in_valid_range():
    """Gating variables are probabilities — must lie in [0, 1]."""
    m_inf, h_inf, n_inf = steady_state(-65.0)
    for gate in (m_inf, h_inf, n_inf):
        assert 0.0 <= gate <= 1.0

def test_resting_potential_is_stable_without_stimulus():
    """With zero injected current, a neuron started at rest should stay
    near -65 mV (allowing small numerical drift)."""
    V0 = -65.0
    m0, h0, n0 = steady_state(V0)
    state0 = np.array([V0, m0, h0, n0])

    no_current = step_current(amplitude=0.0, t_on=0.0, t_off=0.0)
    t_array = np.arange(0.0, 20.0, 0.01)
    deriv_func = lambda state,t: hh_derivatives( state,  t, no_current)
    states = rk4_integrate(deriv_func, state0, t_array)
    a = np.abs(states[:, 0] - V0)
    assert np.all(np.abs(states[:, 0] - V0) < 1.0)


def test_suprathreshold_current_produces_a_spike():
    """A strong enough current step should produce a spike (V > 0 mV
    at some point), since threshold for this parameter set is well
    below 10 uA/cm^2."""
    V0 = -65.0
    m0, h0, n0 = steady_state(V0)
    state0 = np.array([V0, m0, h0, n0])

    strong_current = step_current(amplitude=10.0, t_on=5.0, t_off=30.0)
    t_array = np.arange(0.0, 50.0, 0.01)
    deriv_func = lambda state,t: hh_derivatives( state,  t, strong_current)
    states = rk4_integrate(deriv_func, state0, t_array)

    assert np.max(states[:, 0]) > 0.0


def test_subthreshold_current_does_not_spike():
    """A very weak current step should NOT produce a full spike."""
    V0 = -65.0
    m0, h0, n0 = steady_state(V0)
    state0 = np.array([V0, m0, h0, n0])

    weak_current = step_current(amplitude=0.5, t_on=5.0, t_off=30.0)
    t_array = np.arange(0.0, 50.0, 0.01)
    deriv_func = lambda state,t: hh_derivatives( state,  t, weak_current)
    states = rk4_integrate(deriv_func, state0, t_array)


    assert np.max(states[:, 0]) < 0.0