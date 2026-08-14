# Lab Notebook

Dated research log. Keep entries honest and specific — what tried, what
failed, what changed, and why. 

Format for each entry:

```
## YYYY-MM-DD

**Goal today:**

**What I did:**

**Result / observation:**

**Problem or surprise (if any):**

**Next step:**
```

---

## Example entry (to be deleted when start)

## 2026-07-30

**Goal today:** Get a single HH neuron to spike and validate against known
qualitative behavior.

**What I did:** Implemented the 4 coupled ODEs (V, m, h, n) and both Euler
and RK4 integrators. Ran with a 10 uA/cm^2 step current from t=5 to t=30 ms,
dt=0.01 ms.

**Result / observation:** Neuron rests at -65 mV, spikes to ~+40 mV shortly
after stimulus onset, shows afterhyperpolarization, gates fire in the
expected order (m fast, h slower, n slowest). Euler and RK4 agree closely
at dt=0.01.

**Problem or surprise (if any):** None yet — matches textbook behavior.

**Next step:** Compare Euler vs RK4 at larger dt to find where Euler starts
to break down. Then find the minimum (threshold) current for a spike via
bisection.
