import numpy as np
from hh_model.integrators import rk4_integrate
from hh_model.networks import kuramoto_order_parameters, all_to_all_adjacency, kuramoto_derivatives, coupled_fhn_derivatives, ring_adjacency

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

def test_kuramoto_order_parameter_is_one_for_identical_phases():
    """If every oscillator has the exact same phase, r must be exactly 1."""
    state = np.full(5,10)
    r = kuramoto_order_parameters(state)
    assert np.isclose(r,1)

def test_kuramoto_order_parameter_is_bounded():
    """r is defined as a magnitude of an average of unit vectors — must lie in [0, 1] for any input."""
    state = np.random.rand(10)
    r = kuramoto_order_parameters(state)
    assert 0 - np.exp(-8) < r < 1 + np.exp(-8)

def test_uncoupled_fhn_oscillators_do_not_synchronize_their_currents():
    """With K=0, coupled_fhn_derivatives should reduce to two INDEPENDENT FHN oscillators — verify the coupling term truly vanishes."""
    state = np.random.rand(10)
    uncoupled_state = coupled_fhn_derivatives(state, 0.0, lambda t: 1.3, 0.0, ring_adjacency(5), a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
    n = len(state)//2
    v = state[:n]
    w = state[n:]
    dvdt = v - (v**3)/3 - w + 1.3
    assert np.allclose(uncoupled_state[:n],dvdt)

def test_strong_kuramoto_coupling_increases_synchrony():
    """For a fixed set of heterogeneous natural frequencies, stronger coupling should produce higher final synchrony than weak coupling — the core qualitative claim of the whole stage."""
    random = np.random.default_rng(1)
    # ensures system starts in a state of complete disorder (incoherence). 
    # At timestamp t=0, the oscillators are scattered evenly in all directions around the circle,
    # meaning their net alignment (the order parameter R) will start very close to 0.0
    state = random.uniform(0, 2 * np.pi, size=5) 
    freq = random.normal(1.0, 0.3, size=5)
    t_array = np.linspace(0,50,1000)

    deriv_func = lambda state,t: kuramoto_derivatives(state, freq, 0.1, all_to_all_adjacency(5))
    weak = rk4_integrate(deriv_func, state, t_array)

    weak_synchrony = kuramoto_order_parameters(weak)

    deriv_func1 = lambda state,t: kuramoto_derivatives(state, freq, 0.5, all_to_all_adjacency(5))
    strong = rk4_integrate(deriv_func1, state, t_array)

    strong_synchrony = kuramoto_order_parameters(strong)

    assert strong_synchrony > weak_synchrony

def test_ring_adjacency_has_correct_degree():
    """Each node in a ring should have exactly 2 neighbors."""
    adjancy = ring_adjacency(5)
    columns = np.sum(adjancy, axis = 1)
    assert np.all(columns == 2.0)
