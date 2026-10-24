from hh_model.channelopathy import networks_parameter_sets_FHN_with_fraction
from hh_model.networks import all_to_all_adjacency, coupled_fhn_derivatives
from hh_model.integrators import rk4_integrate
import numpy as np
import matplotlib.pyplot as plt

def sweep_synchronization_change(severity_values, fraction_values, seeds, n=8, coupling=0.15, duration=300, dt=0.05):
    """Return mean and standard deviation of paired synchronization changes."""
    changes = np.zeros((len(severity_values),len(fraction_values),len(seeds)))
    adj_matr = all_to_all_adjacency(n)
    I_array = np.linspace(0.34, 0.42, n)
    t_array = np.arange(0,duration,dt)

    for indexi,i in enumerate(seeds):
        for indexj,j in enumerate(fraction_values):
            for indexk,k in enumerate(severity_values):
                seed = np.random.default_rng(i)
                state0 = np.concatenate(seed.uniform(-0.3, 0.3, n), seed.uniform(-1, 1, n))) 
                baseline_params, perturbed_params, affected_count = networks_parameter_sets_FHN_with_fraction(n, k, 1, fraction=j)
                base = run_network(baseline_params, coupling, I_array, adj_matr, state0, t_array)
                perturb = run_network(perturbed_params, coupling, I_array, adj_matr, state0, t_array)
                changes[indexk,indexj,indexi] = perturb - base
        
    mean_change = np.mean(changes, axis=2)
    std_change = np.std(changes, ddof = 1, axis=2)

    return mean_change, std_change, changes



def run_network(parameter_set, coupling, currents, adjancency, state0, t_array):
    """Integrate one network realization and return its synchronization error."""
    deriv_func = lambda state,t: coupled_fhn_derivatives(state, t, lambda t: currents, coupling, adjancency, parameter_set[0], parameter_set[1], parameter_set[2])
    trajectory = rk4_integrate(deriv_func, state0, t_array)
    return synchronization_error(trajectory, adjancency.shape[0])


def synchronization_error(trajectory, n, transient_fraction=0.5):
    """Compute post-transient RMS voltage deviation from the network mean."""
    start = int(len(trajectory) * transient_fraction)
    voltage = trajectory[start:, :n]
    mean_voltage = np.mean(voltage, axis=1, keepdims=True)
    rms = np.sqrt(np.mean(np.square(voltage - mean_voltage)))
    return rms


def heatmap(axis, values, severity_values, fraction_values, title, colorbar_label):
    my_extent = [severity_values[0], severity_values[-1], fraction_values[0], fraction_values[-1]]
    image = axis.imshow(values, aspect = "auto", origin = "lower", extent = my_extent, cmap='coolwarm')
    axis.set_xlabel("Sodium conductance scale (g_Na / g_Na_baseline)")
    axis.set_ylabel("Fraction of network affected")
    axis.set_title(title)
    axis.figure.colorbar(image, label=colorbar_label)




## PROCEDURE
severity_values = [0.5, 0.7, 0.9, 1.0]
fraction_values = [0.0, 0.25, 0.5, 0.75, 1.0]
seeds = [11, 23, 37, 41, 59]

mean_change, std_change, _ = sweep_synchronization_change(severity_values, fraction_values, seeds)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(13, 5))
heatmap(axes[0], mean_change, severity_values, fraction_values, "Mean synchronization change", "Perturbed - baseline RMS error")
heatmap(axes[1], std_change, severity_values, fraction_values, "Across-seed spread", "Standard deviation of RMS error change")
fig.suptitle("Network synchronization sensitivity to channelopathy")

plt.show()