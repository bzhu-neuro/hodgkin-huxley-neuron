"""
Injected-current stimulus functions, mimicking current-clamp experiments.
Each function returns a callable I_inj(t) -> current in uA/cm^2, so it can
be passed directly to hh_derivatives / the integrators.
"""


def step_current(amplitude, t_on, t_off):
    """A single rectangular current step."""
    def I_inj(t):
        return amplitude if t_on <= t <= t_off else 0.0
    return I_inj


def double_pulse_current(amplitude, t_on1, t_off1, t_on2, t_off2):
    """Two current steps — useful for probing refractory period effects."""
    def I_inj(t):
        if t_on1 <= t <= t_off1:
            return amplitude
        elif t_on2 <= t <= t_off2:
            return amplitude
        else:
            return 0.0

        
    return I_inj


def ramp_current(start_amp, end_amp, t_start, t_end):
    """A linearly ramping current between t_start and t_end."""
    def I_inj(t):
        if t <= t_start:
            return start_amp
        elif t_start <= t <= t_end:
            return (end_amp - start_amp)*(t - t_start)/(t_end - t_start) + start_amp
        else:
            return end_amp
        
    return I_inj
