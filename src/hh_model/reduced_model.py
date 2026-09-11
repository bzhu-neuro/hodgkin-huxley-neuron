"""
FitzHugh-Nagumo (FHN) model — a 2-variable reduction of Hodgkin-Huxley.


HH's 4 variables (V, m, h, n) are hard to visualize and
analyze directly. FitzHugh (1961) noticed that m relaxes so much faster
than the other variables that you can treat it as instantaneous, and that
h and n move roughly oppositely and can be lumped into one "recovery"
variable w. That leaves 2 variables — small enough to draw an actual phase
portrait.


    dv/dt = v - v^3/3 - w + I        (v: fast "voltage-like" variable)
    dw/dt = eps * (v + a - b*w)      (w: slow "recovery" variable)


v and w here are dimensionless and NOT literally in mV — they capture the
same qualitative excitable behavior as HH's V and (h,n)-combination, not
the exact biophysical scale. That's the tradeoff for analytical tractability.


Standard parameters (FitzHugh 1961): a=0.7, b=0.8, eps=0.08
"""


A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

import numpy as np

def fhn_derivatives(state, t, I_func, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT):
    """
    Parameters
    ----------
    state = [v, w]
    t : float, current time in ms
    I_func : callable, I_func(t) -> injected current (constant is fine —
             pass e.g. `lambda t: 0.5` for a fixed-current bifurcation study)
             Matches the generic deriv_func(state, t) interface after currying I_func,
    a, b, eps — henomenological parameters of the FitzHugh-Nagumo model.


    Returns
    -------
    np.ndarray, d(state)/dt
    """


    v = state[0]
    w = state[1]
    dvdt = v - (v**3)/3 - w + I_func(t)
    dwdt = eps * (v + a - b*w)    
    return np.array([dvdt, dwdt])



def v_nullcline(v, I):
    """w as a function of v where dv/dt = 0."""
    w = v - (v**3)/3 + I
    return w



def w_nullcline(v, a=A_DEFAULT, b=B_DEFAULT):
    """w as a function of v where dw/dt = 0. (This one's a straight line.)"""
    w = (v + a) / b
    return w



def find_fixed_point(I, a=A_DEFAULT, b=B_DEFAULT):
    """
    Solve for the fixed point (v*, w*) where BOTH nullclines intersect.


    Substituting the w-nullcline (affine in v) into the v-nullcline gives a
    CUBIC polynomial in v alone — solvable exactly with numpy.roots, no
    iterative root-finder needed. This is a nice concrete use of
    linear algebra background: numpy.roots itself works by finding the
    eigenvalues of the polynomial's companion matrix.


    Derivation: v - v^3/3 + I = (v + a)/b
        => -(1/3) v^3 + (1 - 1/b) v + (I - a/b) = 0


    Returns (v_star, w_star) for the (unique, for standard parameters)
    real root. Raises ValueError if no real root is found (shouldn't happen for
    typical a, b, I ranges — if it does, that's worth investigating,
    not silently working around).
    """

    v_starall = np.roots([-(1/3), 0,(1 - 1/b), (I - a/b)])
    v_stararray = v_starall[np.isreal(v_starall)].real
    if len(v_stararray) != 1:
        raise ValueError("There are either more than 1 or less than 1 real root!!")
    v_star = v_stararray[0]
    w_star = (v_star + a) / b

    return v_star, w_star



def jacobian_eigenvalues(v_star, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT):
    """
    Linearize the system around the fixed point and return its eigenvalues.


    Jacobian:
        J = [[df1/dv, df1/dw],   = [[1 - v*^2,   -1  ],
             [df2/dv, df2/dw]]     [eps,       -eps*b]]


    Eigenvalue signs tell you the fixed point's stability:
        - both real parts negative -> stable
        - either real part positive -> unstable
        - complex with real part crossing zero as a parameter varies
          -> Hopf bifurcation (birth of a limit cycle / sustained
          oscillation) — this is the mechanism behind repetitive firing.


    Returns a length-2 complex numpy array of eigenvalues.
    """
    J = [[1 - v_star**2,   -1  ],
        [eps,            -eps*b]]

    eigenvalues = np.linalg.eigvals(J)
    return eigenvalues
    

