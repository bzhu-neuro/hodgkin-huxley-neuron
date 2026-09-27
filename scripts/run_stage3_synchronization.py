import numpy as np
import matplotlib.pyplot as plt
from hh_model.integrators import rk4_integrate
from hh_model.networks import kuramoto_order_parameters, all_to_all_adjacency, kuramoto_derivatives, coupled_fhn_derivatives, ring_adjacency

A_DEFAULT = 0.7
B_DEFAULT = 0.8
EPS_DEFAULT = 0.08

# -----------------------------------------------------------------------
# FIGURE 1: Two coupled FHN oscillators, a few coupling strengths
# -----------------------------------------------------------------------

import matplotlib.pyplot as plt
I_array = np.array([0.34, 0.42])
t_array = np.linspace(0,300,1000)
adj_matr = all_to_all_adjacency(2)
state0 = np.array([-1, 1, -0.3, 0.3])
K_array = np.array([0.0,0.02,0.15])

fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
fig.suptitle("Two coupled FHN oscillators: synchronization vs. coupling strength K")
for index,K in enumerate(K_array):
    deriv_func = lambda state,t: coupled_fhn_derivatives(state, t, lambda t: I_array, K, adj_matr, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
    v = rk4_integrate(deriv_func, state0, t_array)
    ax[index].plot(t_array, v[:,0], label = "oscillater 1 (I=0.34)")
    ax[index].plot(t_array, v[:,1], label = "oscillater 2 (I=0.42)")
    ax[index].set_title("K = " + str(K))
    ax[index].set_ylabel("v")
    ax[index].legend(loc = 'upper right')

plt.xlabel("Time")

plt.savefig("results/figures/stage3_fhn_coupling.png", dpi=150)

plt.show()


# -------------------------------------------------------------------------
# FIGURE 2: Synchronization error vs. coupling strength (2 FHN oscillators)
# -------------------------------------------------------------------------

K_array = np.linspace(0,0.15,25)
I_array = np.array([0.34, 0.42])
t_array = np.linspace(0,300,1000)
adj_matr = all_to_all_adjacency(2)
state0 = np.array([-1, 1, -0.3, 0.3])

fig, ax = plt.subplots(1, 1, figsize=(9, 7), sharex=True)
plt.title("Synchronization Error vs Coupling Strength (2 FHN Oscillators)")

rms = np.zeros_like(K_array)
for index,K in enumerate(K_array):
    deriv_func = lambda state,t: coupled_fhn_derivatives(state, t, lambda t: I_array, K, adj_matr, a=A_DEFAULT, b=B_DEFAULT, eps=EPS_DEFAULT)
    v = rk4_integrate(deriv_func, state0, t_array)
    difference = v[:,1] - v[:,0]
    rms[index] = np.sqrt(np.mean(np.square(difference)))

plt.plot(K_array, rms, color='k', marker='o', linestyle='-')
plt.xlabel("Coupling Strength K")
plt.ylabel("RMS (v1 - v2), post-transient")

plt.savefig("results/figures/stage3_fhn_sync_error.png", dpi=150)

plt.show()



# -------------------------------------------------------------------------
# FIGURE 3: Kuramoto network — order parameter vs coupling strength
# -------------------------------------------------------------------------

N = 20
K_array = np.linspace(0,20,30)
rng = np.random.default_rng(seed=67)
freq = rng.normal(loc=1.0, scale=0.3, size=N)
state = rng.uniform(0, 2 * np.pi, size=N)
t_array = np.linspace(0,100,2000)

ring_matr = ring_adjacency(N)
all_matr = all_to_all_adjacency(N)
matr = np.array([ring_matr, all_matr])
word = np.array(["Ring", "All to All"])

r_ring = np.zeros_like(K_array)

for index, matr in enumerate(matr):
    fig, ax = plt.subplots(1, 1, figsize=(8, 7), sharex=True)
    for index1,K in enumerate(K_array):
        deriv_func = lambda state,t: kuramoto_derivatives(state, freq, K, matr)
        theta = rk4_integrate(deriv_func, state, t_array)
        better_theta = theta[int(0.8 * len(t_array)):]
        j =  [kuramoto_order_parameters(thetatheta) for thetatheta in better_theta]
        
        r_ring[index1] = np.mean(j)

    ax.plot(K_array, r_ring, color='k', marker='o', linestyle='-')
    ax.set_title("Kuramoto Synchronization Transition (N=20, " + word[index] + " Coupling)")
    ax.set_xlabel("Coupling Strength K")
    ax.set_ylabel("Order Parameter r, post-transient average")
    ax.set_ylim(0,1.05)

    plt.savefig(f"results/figures/stage3_kuramoto_transition_{word[index].lower().replace(" ", "_")}.png", dpi=150)



