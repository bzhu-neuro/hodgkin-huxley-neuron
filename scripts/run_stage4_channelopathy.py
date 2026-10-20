import numpy as np
import matplotlib.pyplot as plt
from hh_model.channelopathy import scaled_conductances, fhn_parameter_mapping, hh_derivatives_channelopathy, fhn_derivative_channelopathy
from hh_model.reduced_model import find_fixed_point, jacobian_eigenvalues
from hh_model.integrators import rk4_integrate
from hh_model.kinetics import steady_state
from hh_model.constants import g_Na, g_K

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

fig, ax = plt.subplots(1, 1, figsize=(9, 7), sharex=True)
g_Na_scale = np.array([0.7,1.0,1.3])
color = np.array(["blue","orange","green"])
I_current = np.linspace(0, 12, 25)
V0 = -65.0
m0, h0, n0 = steady_state(V0)

for indexNa,Na in enumerate(g_Na_scale):
    firing_rate = np.zeros_like(I_current)
    for indexC,current in enumerate(I_current):
        state0 = np.array([V0, m0, h0, n0])
        t_array = np.arange(0.0, 120.0, 0.01)
        conductances = scaled_conductances(g_Na, Na, g_K, 1)
        deriv_func = lambda state, t: hh_derivatives_channelopathy(state, t, lambda t: current, Na, 1)
        states = rk4_integrate(deriv_func, state0, t_array)
        v_threshold = 0
        spike_count = np.sum((states[:-1,0] < v_threshold) & (states[1:,0] >= v_threshold))
        firing_rate[indexC] = spike_count/120
    

    ax.plot(I_current, firing_rate, linestyle = '-', marker = 'o',label="g_Na = " + str(g_Na_scale[indexNa]) + "x", color=color[indexNa])

ax.set_title("HH f-I curves under sodium-channel scaling")
ax.set_ylabel("Firing rate (spikes/ms)")
ax.set_xlabel("Injected current I (uA/cm^2)")
ax.legend(loc = 'upper left')

plt.savefig("results/figures/stage4_current_to_firing_rate_channelopathy.png", dpi=150)

plt.show()



fig, ax1 = plt.subplots(1, 1, figsize=(9, 7), sharex=True)
g_Na_scale = np.array([0.7,1.0,1.3])
color_stable = np.array(["blue","green","purple"])
color_unstable = np.array(["orange","red","brown"])


for indexNa,Na in enumerate(g_Na_scale):
    I_values = np.linspace(-1.0,1.5,300)
    values = np.zeros_like(I_values)
    stability = np.zeros_like(I_values, dtype = bool)
    fhn_constants = fhn_parameter_mapping(Na, 1, A_DEFAULT, B_DEFAULT, EPS_DEFAULT)

    for index, I_val in enumerate(I_values):
        point = find_fixed_point(I_val, fhn_constants["a_scaled"], fhn_constants["b_scaled"])
        eigenvalues = jacobian_eigenvalues(point[0], fhn_constants["a_scaled"], fhn_constants["b_scaled"], fhn_constants["eps_scaled"])
        values[index] = point[0]
        if eigenvalues[0].real < 0 and eigenvalues[1].real < 0:
            stability[index] = True
        else:
            stability[index] = False

    ax1.plot(I_values[stability], values[stability], color = color_stable[indexNa], marker = '.', linestyle="None", label = "stable, g_Na = " + str(g_Na_scale[indexNa]) + "x")
    ax1.plot(I_values[~stability], values[~stability], color = color_unstable[indexNa], marker = '.', linestyle="None", label = "unstable, g_Na = " + str(g_Na_scale[indexNa]) + "x")


ax1.set_title("Approximate FHN bifurcation curves under sodium-channel scaling")
ax1.set_xlabel("Injected Current")
ax1.set_ylabel("Fixed point v")
ax1.legend(loc = 'upper left')

plt.savefig("results/figures/stage4_bifurcation_diagram_channelopathy.png", dpi=150)

plt.show()