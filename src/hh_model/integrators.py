"""
Numerical integrators for the HH ODE(Ordinary Differential Equation) system.

"""

import numpy as np

def euler_integrate(deriv_func, state0, t_array):
    """
    Parameters
    ----------
    deriv_func : callable, deriv_func(state, t) -> d(state)/dt
    state0 : array-like, initial condition
    t_array : array-like, uniformly spaced time points


    Returns
    -------
    np.ndarray of shape (len(t_array), len(state0))
    """

    dt = t_array[1] - t_array[0]
    states = np.zeros((len(t_array), len(state0)))
    states[0] = state0
    for i in range(1, len(t_array)):
        deriv = deriv_func(states[i - 1], t_array[i - 1])
        states[i] = states[i - 1] + dt * deriv
    return states


def rk4_integrate(deriv_func, state0, t_array):
    """    
    Parameters
    ----------
    deriv_func : callable, deriv_func(state, t) -> d(state)/dt
    state0 : array-like, initial condition
    t_array : array-like, uniformly spaced time points


    Returns
    -------
    np.ndarray of shape (len(t_array), len(state0))
    
    Same interface as euler_integrate, but 4th-order Runge-Kutta.
    """
    
    dt = t_array[1] - t_array[0]
    states = np.zeros((len(t_array), len(state0)))
    states[0] = state0
    for i in range(1, len(t_array)):
        t = t_array[i - 1]
        s = states[i - 1]
        k1 = deriv_func(s, t)
        k2 = deriv_func(s + dt/2 * k1, t + dt/2)
        k3 = deriv_func(s + dt/2 * k2, t + dt/2)
        k4 = deriv_func(s + dt * k3, t + dt)
        states[i] = states[i - 1] + (dt/6) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return states
