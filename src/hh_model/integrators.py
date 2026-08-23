"""
Numerical integrators for the HH ODE(Ordinary Differential Equation) system.

Kept separate from model.py deliberately: the vector field (physics) and
the integration method (numerics) are conceptually different things, and
this project's Stage 1 goal is explicitly to compare integration methods
on the same vector field.
"""
from hh_model.constants import C_m, g_Na, g_K, g_L, E_Na, E_K, E_L
from hh_model.kinetics import alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n
from hh_model.model import hh_derivatives
import numpy as np

def euler_integrate(state0, t_array, I_inj_func):
    dt = t_array[1] - t_array[0]
    states = np.zeros((len(t_array), len(state0)))
    states[0] = state0
    for i in range(1, len(t_array)):
        deriv = hh_derivatives(states[i - 1], t_array[i - 1], I_inj_func)
        states[i] = states[i - 1] + dt * deriv
    return states


def rk4_integrate(state0, t_array, I_inj_func):
    dt = t_array[1] - t_array[0]

    states = np.zeros((len(t_array), len(state0)))
    states[0] = state0
    for i in range(1, len(t_array)):
        t = t_array[i - 1]
        s = states[i - 1]
        k1 = hh_derivatives(s, t, I_inj_func)
        k2 = hh_derivatives(s + dt/2 * k1, t + dt/2, I_inj_func)
        k3 = hh_derivatives(s + dt/2 * k2, t + dt/2, I_inj_func)
        k4 = hh_derivatives(s + dt * k3, t + dt, I_inj_func)
        states[i] = states[i - 1] + (dt/6) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return states