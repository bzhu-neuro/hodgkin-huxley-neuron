"""
The Hodgkin-Huxley system of 4 coupled ODEs — the vector field that every
integrator in this package operates on.
"""
from hh_model.constants import C_m, g_Na, g_K, g_L, E_Na, E_K, E_L
from hh_model.kinetics import alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n
import numpy as np

def hh_derivatives(state, t, I_inj_func):
    """
    Parameters
    ----------
    state : array-like [V, m, h, n]
    t : float, current time in ms
    I_inj_func : callable, I_inj_func(t) -> injected current in uA/cm^2

    Returns
    -------
    np.ndarray, d(state)/dt
    """
    V = state[0]
    m = state[1]
    h = state[2]
    n = state[3]
    dVdt = (I_inj_func(t) - g_K * n**4 * (V - E_K) - g_Na * h * m**3 * (V - E_Na) - g_L * (V - E_L)) / C_m
    dmdt = alpha_m(V) * (1.0 - m) - beta_m(V) * m
    dhdt = alpha_h(V) * (1.0 - h) - beta_h(V) * h
    dndt = alpha_n(V) * (1.0 - n) - beta_n(V) * n

    return np.array([dVdt, dmdt, dhdt, dndt])
