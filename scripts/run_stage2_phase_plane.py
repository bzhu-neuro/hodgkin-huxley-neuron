from hh_model.reduced_model import fhn_derivatives, find_fixed_point, jacobian_eigenvalues, v_nullcline, w_nullcline
from hh_model.integrators import rk4_integrate
import matplotlib.pyplot as plt
import numpy as np

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

# -----------------------------------------------------------------------
# FIGURE 1: Phase portrait at a fixed, subthreshold-ish current
# -----------------------------------------------------------------------

I_fixed = 0.35
v = np.linspace(-2.5,2.5,500 )
t_array = np.linspace(0,300,1000)

v_grid, w_grid = np.meshgrid(np.linspace(-2.5,2.5,20),np.linspace(-1.0,2.0,20))
derivatives = fhn_derivatives((v_grid, w_grid),v,lambda x: I_fixed)
magnitude = np.sqrt(derivatives[0]**2 + derivatives[1]**2)

fixedpoint = find_fixed_point(I_fixed, a=A_DEFAULT, b=B_DEFAULT)
eigenvalues = jacobian_eigenvalues(fixedpoint[0], a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)

deriv_func = lambda state,t: fhn_derivatives( state,  t, lambda t: I_fixed, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
results = rk4_integrate(deriv_func, (-1.5,-0.5), t_array)

fig, ax = plt.subplots(1,1, figsize = (10,10))

ax.plot(v, v_nullcline(v, I_fixed), color='steelblue', label='v-nullcline  (dv/dt=0)')
ax.plot(v, w_nullcline(v), color='orange', label='w-nullcline  (dw/dt=0)')

if eigenvalues[0].real < 0 and eigenvalues[1].real < 0:
    ax.plot(fixedpoint[0], fixedpoint[1], marker='o', markersize=12, color='green', label='fixed point (stable)')
else:
    ax.plot(fixedpoint[0], fixedpoint[1], marker='o', markersize=12, color='red', label='fixed point (unstable)')

ax.plot(results[:, 0], results[:, 1], color='black', label='trajectory')

ax.quiver(v_grid, w_grid, derivatives[0]/magnitude, derivatives[1]/magnitude, color='lightgray', alpha = 0.6)
ax.set_title("FHN phase portrait (I = " + str(I_fixed) + ")")
ax.set_xlabel("v")
ax.set_ylabel("w")
ax.set_ylim((-1,2))
ax.set_xlim((-2.5,2.5))
ax.legend()

plt.savefig(f"results/figures/stage2_phase_portrait_I_{I_fixed}.png", dpi=150)
plt.show()



# -----------------------------------------------------------------------
# FIGURE 2: Bifurcation diagram — fixed point and stability vs I
# -----------------------------------------------------------------------

I_values = np.linspace(-1.0,1.5,300)
values = np.zeros_like(I_values)
stability = np.zeros_like(I_values, dtype = bool)

for index, I_val in enumerate(I_values):
    point = find_fixed_point(I_val, a=A_DEFAULT, b=B_DEFAULT)
    eigenvalues = jacobian_eigenvalues(point[0], a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
    values[index] = point[0]
    if eigenvalues[0].real < 0 and eigenvalues[1].real < 0:
        stability[index] = True
    else:
        stability[index] = False

plt.plot(I_values[stability], values[stability], color = "green", marker = '.', linestyle="None", label = "stable fixed point")
plt.plot(I_values[~stability], values[~stability], color = "red", marker = '.', linestyle="None", label = "unstable fixed point")


plt.title("Bifurcation diagram: fixed point stability vs. injected current")
plt.xlabel("Injected Current")
plt.ylabel("Fixed point v")

plt.legend()

plt.savefig("results/figures/stage2_bifurcation_diagram.png", dpi=150)

plt.show()