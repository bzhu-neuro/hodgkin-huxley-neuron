import numpy as np
import matplotlib.pyplot as plt
from hh_model.channelopathy import networks_parameter_sets_FHN
from hh_model.networks import all_to_all_adjacency, coupled_fhn_derivatives
from hh_model.integrators import rk4_integrate

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

fig, ax = plt.subplots(1, 1, figsize=(9, 7), sharex=True)
n = 8
K_array = np.linspace(0,0.15,25)
I_array = np.linspace(0.34, 0.42, n)
t_array = np.linspace(0,300,6000)
adj_matr = all_to_all_adjacency(n)
state0 = np.concatenate((np.linspace(-1, 1, n), np.linspace(-0.3, 0.3, n)))
baseline_params, perturbed_params = networks_parameter_sets_FHN(0.7, 1, n)
params = [baseline_params, perturbed_params]
colors = np.array(['steelblue','orange'])
labels = ['Unperturbed network','One neuron: g_Na = 0.7x']

for indexC,param in enumerate(params):
    rms = np.zeros_like(K_array)
    for index,K in enumerate(K_array):
        deriv_func = lambda state,t: coupled_fhn_derivatives(state, t, lambda t: I_array, K, adj_matr, param[0],param[1],param[2])
        trajectory = rk4_integrate(deriv_func, state0, t_array)

        start = int(len(trajectory) * 0.5)
        voltage = trajectory[start:, :n]
        mean_voltage = np.mean(voltage, axis=1, keepdims=True)
        rms[index] = np.sqrt(np.mean(np.square(voltage - mean_voltage)))

    ax.plot(K_array, rms, marker='o', color=colors[indexC], linestyle='-',label = labels[indexC])


ax.set_title("Network synchronization with one channelopathy defect")
ax.set_ylabel("Post-transient RMS voltage error")
ax.set_xlabel("Coupling strength K")
ax.legend(loc = 'upper right')

plt.show()