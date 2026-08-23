"""
Voltage-dependent gating kinetics for the m (Na activation), h (Na
inactivation), and n (K activation) gates.

Each gate x relaxes according to:
    dx/dt = alpha_x(V) * (1 - x) - beta_x(V) * x

alpha_x is the voltage-dependent opening rate, beta_x the closing rate.
Formulas are the standard modern-convention versions (V = actual membrane
potential in mV) of Hodgkin & Huxley's original empirical fits.

In their original 1952 paper, Hodgkin and Huxley used an older convention where:
The resting membrane potential was set to exactly 0 mV.The sign of the voltage 
was inverted compared to today (depolarization was treated as a negative displacement).
Modern neuroscience sets the outside of the cell to 0 mV, meaning a typical 
neuron's resting potential sits at -65 mV. To convert from the original paper's voltage
V_orig to modern voltage V_mod, the formula is: V_orig = -(V_mod+65).
"""

import numpy as np

def alpha_m(V):
    return 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))


def beta_m(V):
    return 4.0 * np.exp(-(V + 65.0) / 18.0)


def alpha_h(V):
    return 0.07 * np.exp(-(V + 65.0) / 20.0)


def beta_h(V):
    return 1.0 / (np.exp(-(V + 35.0) / 10.0) + 1.0)


def alpha_n(V):
    return 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))


def beta_n(V):
    return 0.125 * np.exp(-(V + 65.0) / 80.0)


def steady_state(V):
    """Return (m_inf, h_inf, n_inf) at a given voltage — useful for
    initializing simulations at rest, or for building activation curves."""
    m_inf = alpha_m(V) / (alpha_m(V) + beta_m(V))
    h_inf = alpha_h(V) / (alpha_h(V) + beta_h(V))
    n_inf = alpha_n(V) / (alpha_n(V) + beta_n(V))
    return m_inf, h_inf, n_inf
