"""
Biophysical constants for the Hodgkin-Huxley squid giant axon model.

Values are the original empirical fits from Hodgkin & Huxley (1952),
"A quantitative description of membrane current and its application to
conduction and excitation in nerve". Page #520.

To get the values accepted today, the voltage scale has to be shifted by -65 mV.
https://lcnwww.epfl.ch/gerstner/SPNM/node14.html#table-HH1
"""

C_m = 1.0      # membrane capacitance, uF/cm^2
g_Na = 120.0   # max sodium conductance, mS/cm^2
g_K = 36.0     # max potassium conductance, mS/cm^2
g_L = 0.3      # max leak conductance, mS/cm^2
E_Na = 50.0    # sodium reversal (equilibrium) potential, mV
E_K = -77.0    # potassium reversal potential, mV
E_L = -54.387  # leak reversal potential, mV
