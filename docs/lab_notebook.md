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

##

Day 1: 2026-08-23

**Goal today:** Finish the later parts of section 1 which was to graph the 
HH-neuron's behavior.

**What I did:** Implemented the 4 coupled ODEs (V, m, h, n) and both Euler
and RK4 integrators. Ran with a 10 uA/cm^2 step current from t=5 to t=30 ms,
dt=0.01 ms.

**Result / observation:** Neuron rests at -65 mV, spikes to ~+40 mV shortly
after stimulus onset, shows afterhyperpolarization, gates fire in the
expected order (m fast, h slower, n slowest). Euler and RK4 agree closely
at dt=0.01.

**Problem or surprise (if any):** A random variable overwrote the previous 
variable so it took a lot of time to find it.

**Next step:** Compare Euler vs RK4 at larger dt to find where Euler starts
to break down. Then find the minimum (threshold) current for a spike via
bisection.

##

Day 2: 2026-08-24

**Goal today:** Fix some github display issues about Stage 1.

**Result / observation:** Using commands to fix the issues.

**Problem or surprise (if any):** It displays correctly on VS but not on github.

**Next step:** Compare Euler vs RK4 at larger dt to find where Euler starts to break down. Then find the minimum (threshold) current for a spike via
bisection. (Start Stage 2)

##

Day 3: 2026-08-26

**Goal today:** Learn about everything I need for Stage 2. Ex: Reduce to the 2D FitzHugh-Nagumo model, phase-plane analysis, nullclines, Jacobian linearization, bifurcation diagram vs. injected current.

**Result / observation:** Learned the material.

**Problem or surprise (if any):** N/A

**Next step:** Actually start the code of Stage 2. 
