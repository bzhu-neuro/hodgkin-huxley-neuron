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

**Next step:** Compare Euler vs RK4 at larger dt to find where Euler starts to 
break down. Then find the minimum (threshold) current for a spike via
bisection. (Start Stage 2)

##

Day 3: 2026-08-26

**Goal today:** Learn about everything I need for Stage 2. Ex: Reduce to the 
2D FitzHugh-Nagumo model, phase-plane analysis, nullclines, Jacobian 
linearization, bifurcation diagram vs. injected current.

**Result / observation:** Learned the material.

**Problem or surprise (if any):** N/A

**Next step:** Actually start the code of Stage 2.

##

Day 4: 2026-08-29

**Goal today:** To complete my learning on the FitzHugh-Nagumo model and 
transition into implementing that model into code.

**What I did:** Created functions using the FitzHugh-Nagumo model with the 
variables (v,w). Made a function for the nullclines of the model. Made a 
function for where they intersect. Made a function for the eigenvalues of 
the Jacobian Matrix of the intersection of the nullclines.

**Result / observation:** Created those functions.

**Problem or surprise (if any):** N/A

**Next step:** Implement those functions to display the model.

##

Day 5: 2026-09-03

**Goal today:** To double check the functions I created from the previous
day.

**What I did:** Created a test for a fixed_point function and a test for
the jacobian eigenvalue function.

**Result / observation:** Created those functions.

**Problem or surprise (if any):** N/A

**Next step:** Create another test for another function and Update ODE
Integrators.

##

Day 6: 2026-09-06

**Goal today:** Finish creating the last function test. Import and change
the rk4 and euler integrate functions from part 1 to here. To graph the 
v and w nullclines, a fixed point on the intersection, and to find the 
trajectory of a random point to that line.

**What I did:** Created a test for a stability in the plane. I also copy
and pasted my euler and rk4 functions from last part, but I changed it such
that it works for any general function and not just hh or fhn derivatives.
I also plotted the nullclines.

**Result / observation:** The plot looks pretty cool. There is a vector
space on top that also displays the direction.

**Problem or surprise (if any):** The graphing is really annoying. The
w-nullcline for some reason isn't interesting where it should be. Also
changing the functions is a headache.

**Next step:** Plot when a point has unstable current input.

##

Day 7: 2026-09-10

**Goal today:** Finish the rest of Stage 2. Create a graph of injected
current vs v-star. Find the flip in stability in different injected
currents. Graph two values, one stable and another unstable, onto the
v-null and w-null graph.

**What I did:** I created the graphs. I also needed to import it back
to github.

**Result / observation:** Both plots look pretty cool.

**Problem or surprise (if any):** The stability graph was acting weird
by an increment of 0.5. Turns out that I misread the labels of the axes.
Also importing is really annoying.

**Next step:** Start learning the material necessary for stage 3.

##


Day 8: 2026-09-13

**Goal today:** Learn about HH Coupled Oscillators and the Kuramoto 
Model of Oscillators.

**What I did:** Learned about the coupled oscillators which are a more
realistic but complex model and learned about the Kuramoto Model which
is a more simple but abstract model.

**Result / observation:** Obtained knoledge.

**Problem or surprise (if any):** N/A

**Next step:** Start creating variables and have an idea on how to
transition this into code.


##


Day 9: 2026-09-14

**Goal today:** Finish off coding CFHN and Kuramoto deratives.

**What I did:** I coded what I was supposed to do.

**Result / observation:** N/A

**Problem or surprise (if any):** I was pretty hard to find the
"right" formula because there are some variations.

**Next step:** Create tests to verify the legitimacy of the
functions.
