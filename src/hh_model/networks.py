"""
Coupled FitzHugh-Hagumo Model - N biophysically-motivated oscillators,
diffusively coupled through their voltage-like variable v 
(this is the standard way to model electrical/gap-junction 
coupling between neurons: current flows proportional to the 
voltage DIFFERENCE between connected cells). 
This is close to the actual biophysics.

Kuramoto Model — a much more abstract model where each oscillator is 
reduced to JUST a phase (no amplitude, no separate excitability dynamics).
It's the canonical model in synchronization theory because it's simple 
enough to reason about analytically, and it's what most of the 
"EEG mu/beta synchronization" BCI literature implicitly draws on conceptually. 
Comparing the two is the point of this stage: you'll see the SAME qualitative
phenomenon (coupling strength -> synchrony) emerge from a detailed
biophysical model and a minimal abstract one.


"""

import numpy as np

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

def all_to_all_adjacency(N):
    """
    Parameters
    ----------
    N : the amount of neurons

    Returns
    -------
    A matrix of 1's size N besides its main diagonal.
    Demonstrates that all neurons are synchronized.
    """
    
    all_to_all_matrix = np.ones((N, N)) - np.identity(N)
    return all_to_all_matrix



def ring_adjacency(N):
    """
    Parameters
    ----------
    N : the amount of neurons

    Returns
    -------
    A matrix of 1's above and below it's main diagonal
    of size N. Everywhere else, it's zero. Demonstrates
    that each neuron is synchronized with the neuron
    to the left and to the right of it.
    """
    
    ring_matrix = np.eye(N, N, k = 1) + np.eye(N, N, k = -1) + np.eye(N, N, k = N - 1) + np.eye(N, N, k = -N + 1)
    return ring_matrix



def coupled_fhn_derivatives(state, t, I_func, K, matr, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT):
    """
    Parameters
    ----------
    state = [v_1, v_2, v_3 ... v_n, w_1, w_2, w_3 ... w_n]
    t : float, current time in ms
    I_func : callable, I_func(t) -> injected current (constant is fine —
             pass e.g. `lambda t: 0.5` for a fixed-current bifurcation study)
             Matches the generic deriv_func(state, t) interface after currying I_func,
    K : Coupling Strength (synchronization)
    matr : the Adjancency Matrix that shows the sychronization of neurons
    a, b, eps — henomenological parameters of the FitzHugh-Nagumo model.


    Returns
    -------
    np.ndarray, d(state)/dt
    """

    n = len(state)//2
    v = state[:n]
    w = state[n:]

    if np.isscalar(I_func(t)):
        I_inj = np.full(n,I_func(t))
    else:
        I_inj = np.asarray(I_func(t))

    degree = matr.sum(axis=1)
    dot_product = matr @ v

    dvdt = v - (v**3)/3 - w + I_inj + K * (dot_product - degree * v)
    dwdt = eps * (v + a - b*w)    
    return np.concatenate((dvdt, dwdt))



def kuramoto_derivatives(state, freq, K, matr):
    """
    Parameters
    ----------
    state = [theta_1, theta_2, theta_3 ... theta_n]
    freq = [freq_1, freq_2, freq_3 ... freq_n]
    K : Coupling Strength (synchronization)
    matr : the Adjancency Matrix that shows the sychronization of neurons


    Returns
    -------
    np.ndarray, d(state)/dt
    """

    n = len(state)
    dthetadt = freq + (K / n) * np.sum(matr * (np.sin(state[np.newaxis,:] - state[:,np.newaxis])),axis=1)

    return dthetadt



def kuramoto_order_parameters(state):
    """
    Parameters
    ----------
    state = [theta_1, theta_2, theta_3 ... theta_n]

    Returns
    -------
    r (order parameter)

    """
    complex_phases = np.exp(1j * state)
    average_vector = np.mean(complex_phases)
    r = np.abs(average_vector)
    return r
