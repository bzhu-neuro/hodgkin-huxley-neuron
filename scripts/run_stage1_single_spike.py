"""
Stage 1: Single Hodgkin-Huxley neuron, step current, RK4 vs Euler comparison.

"""
from hh_model.model import hh_derivatives
from hh_model.integrators import rk4_integrate, euler_integrate
from hh_model.kinetics import steady_state
from hh_model.stimuli import step_current
import numpy as np
import matplotlib.pyplot as plt

# Initial conditions: resting steady state
V0 = -65.0
m0, h0, n0 = steady_state(V0)
state0 = np.array([V0, m0, h0, n0])

# Stimulus and time base
I_inj = step_current(amplitude=10.0, t_on=5.0, t_off=30.0)
dt = 0.01
t_array = np.arange(0.0, 50.0, dt)

I_injarray = np.zeros(len(t_array))
for i in range(len(t_array)):
    I_injarray[i - 1] = I_inj(t_array[i - 1])

# Integrate
deriv_func = lambda state,t: hh_derivatives( state,  t, I_inj)
states_rk4 = rk4_integrate(deriv_func, state0, t_array)
states_euler = rk4_integrate(deriv_func, state0, t_array)

# Plot
fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)

axes[0].plot(t_array, states_rk4[:, 0], label='RK4', color='black')
axes[0].plot(t_array, states_euler[:, 0], label='Euler', color='red', alpha=0.6, linestyle='--')
axes[0].set_ylabel('Membrane potential (mV)')
axes[0].set_title('Injected current (the stimulus)')
axes[0].legend()

axes[1].plot(t_array, I_injarray, color='b')
axes[1].set_ylabel('I_inj (uA/cm^2)')
axes[1].set_title('Hodgkin-Huxley membrane potential')

axes[2].plot(t_array, states_rk4[:, 1], label='m (Na activation)', color='steelblue')
axes[2].plot(t_array, states_rk4[:, 2], label='h (Na inactivation)', color='orange')
axes[2].plot(t_array, states_rk4[:, 3], label='n (K activation)', color='g')
axes[2].set_ylabel('Gating variable value')
axes[2].set_xlabel('Time (ms)')
axes[2].set_title('Gating variables (RK4)')

plt.tight_layout()

plt.savefig('results/figures/stage1_single_spike.png', dpi=150)

plt.show()
