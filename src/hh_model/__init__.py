"""
hh_model
========
A from-scratch Hodgkin-Huxley neuron modeling package, built as a research
project progressing from single-neuron dynamics to network synchronization.

Public API is kept intentionally small and explicit — import what you need:

    from hh_model.model import hh_derivatives
    from hh_model.integrators import rk4_integrate, euler_integrate
    from hh_model.kinetics import alpha_m, beta_m, alpha_h, beta_h, alpha_n, beta_n
    from hh_model.constants import C_m, g_Na, g_K, g_L, E_Na, E_K, E_L
    from hh_model.stimuli import step_current
"""

__version__ = "0.1.0"
