"""
Tests for the FitzHugh-Nagumo reduced model — verifies the fixed-point
solver and Jacobian eigenvalue analysis are internally consistent, and
that known qualitative behavior (a Hopf bifurcation somewhere in the
standard parameter regime) actually occurs.
"""
import numpy as np
from hh_model.reduced_model import find_fixed_point, fhn_derivatives, jacobian_eigenvalues

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

def test_fixed_point_actually_satisfies_both_nullclines():
    """The solver should return a point where BOTH dv/dt=0 and dw/dt=0."""
    I = 0.3

    v_star, w_star = find_fixed_point(I, a=A_DEFAULT, b=B_DEFAULT)

    deriv_func = lambda state,t: fhn_derivatives( state,  t, lambda t: I, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
    derivatives_0 = deriv_func(np.array([v_star, w_star]),0.0)
    assert derivatives_0[0] < 1 * np.exp(-8)
    assert derivatives_0[1] < 1 * np.exp(-8)

def test_jacobian_eigenvalues_match_trace_and_determinant():
    """Sanity check the eigenvalue computation against the analytic
    trace/determinant formulas for a 2x2 Jacobian — this is exactly the
    kind of cross-check worth doing by hand once, then automating."""
    b = 0.8
    eps = 0.08

    v_star = 0.67
    jcob_eigen = jacobian_eigenvalues(v_star, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
    trace = 1 - v_star**2 - eps*b
    determinant = (1 - v_star**2) * (- eps*b) + eps

    assert np.isclose(np.sum(jcob_eigen),trace)
    assert np.isclose(np.prod(jcob_eigen),determinant)

def test_stability_flips_somewhere_in_standard_range():
    """For standard FHN parameters, the fixed point should be stable for
    some I and unstable for others (a Hopf bifurcation exists) — this is
    the qualitative behavior the whole Stage 2 project hinges on."""
    stabilities = []
    numList = np.linspace(-1.0,1.5,100)

    for I in range(len(numList)):
        point = find_fixed_point(numList[I - 1], a=A_DEFAULT, b=B_DEFAULT)
        eigenvalues = jacobian_eigenvalues(point[0], a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
        if eigenvalues[0].real < 0 and eigenvalues[1].real < 0:
            stabilities.append(True)
        else:
            stabilities.append(False)



    assert np.any(np.array(stabilities) == True)
    assert np.any(np.array(stabilities) == False)   
    