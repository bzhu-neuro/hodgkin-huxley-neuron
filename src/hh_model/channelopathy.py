import numpy as np
import hh_model.model as module
from hh_model.constants import g_Na, g_K
from hh_model.model import hh_derivatives

def scaled_conductances(g_Na, scale1, g_K, scale2):
    """
    Inputs conductances and scales each conductance

    Returns
    -------
    {g_Na_scaled, g_K_scaled}
    """
    Na = g_Na * scale1
    K = g_K * scale2
    return {"g_Na_scaled": Na,"g_K_scaled": K}


def fhn_parameter_mapping(g_Na_scale, g_K_scale, a, b, eps):
    """
    Maps the parameters from HH_model to FHN_model

    Returns
    -------
    {a_scaled,b_scaled,eps_scaled}
    """
    a_scaled = a/g_Na_scale
    b_scaled = b * g_K_scale
    eps_scaled = eps/(0.77 * g_Na_scale + 0.23 * g_K_scale)
    return {"a_scaled": a_scaled,"b_scaked": b_scaled,"eps_scaled": eps_scaled}


def hh_derivatives_channelopathy(state, t, I_inj_func, g_Na_scale, g_K_scale):
    """
    Maps the parameters from HH_model to FHN_model

    Returns
    -------
    np.array[]
    """
    try:
        conductance = scaled_conductances(g_Na,g_Na_scale,g_K,g_K_scale)
        original_g_Na = module.g_Na
        original_g_K = module.g_K
        module.g_Na = conductance["g_Na_scaled"]
        module.g_K = conductance["g_K_scaled"]
        hh_derivatives(state, t, I_inj_func)

    finally:
        module.g_Na = original_g_Na
        module.g_K = original_g_K     



def fhn_derivative_channelopathy():