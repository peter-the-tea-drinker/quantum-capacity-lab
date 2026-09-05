# %% [markdown] slideshow={"slide_type": "slide"}
# # Module 03: Quantum Eraser, Decoherence & $U^\dagger$ Uncomputation
# ### Conserved Many-Worlds & State-Capacity Exploration ($\mathcal{C}_{\text{max}}$)
#
# **Roadmap:**
# 1. Mach-Zehnder / Ramsey Interference Baseline
# 2. Decoherence via Which-Way Detector Entanglement (State Branching)
# 3. Quantum Erasure: Coherent Uncomputation ($U^\dagger$)
# 4. Quantum Erasure: Delayed Choice Basis Erasure & Coincidence Correlation
# 5. Student Exercise 1: Polarization-Based Quantum Eraser & Fringe Visibility Sweep

# %% slideshow={"slide_type": "skip"}
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

plt.style.use('dark_background')
os.makedirs('data', exist_ok=True)

# %% [markdown]
#
#
# #### **Step B: The Eraser Operator (Diagonal Polarizer)**
#
# The diagonal eraser state is $\vert D \rangle = \frac{1}{\sqrt{2}}(\vert H \rangle + \vert V \rangle) = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 1 \end{pmatrix}$. 
#
# To project the polarization qubit while leaving the path qubit untouched, we construct the measurement matrix $M = I \otimes \langle D \vert$:
# $$M = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \otimes \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \cdot \begin{pmatrix} 1 & 1 \end{pmatrix} & 0 \cdot \begin{pmatrix} 1 & 1 \end{pmatrix} \\ 0 \cdot \begin{pmatrix} 1 & 1 \end{pmatrix} & 1 \cdot \begin{pmatrix} 1 & 1 \end{pmatrix} \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \end{pmatrix}$$
#
# #### **Step C: The Resulting State Post-Erasure**
# We apply the projection matrix $M$ to our marked state $\vert\psi\rangle$:
# $$\vert\psi_{\text{final}}\rangle = M \vert\psi\rangle$$
#
# $$\vert\psi_{\text{final}}\rangle = \left[ \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 & 0 & 0 \\ 0 & 0 & 1 & 1 \end{pmatrix} \right] \cdot \left[ \frac{1}{\sqrt{2}} \begin{pmatrix} 0 \\ 1 \\ 1 \\ 0 \end{pmatrix} \right]$$
#
# $$\vert\psi_{\text{final}}\rangle = \frac{1}{2} \begin{pmatrix} (1\cdot0) + (1\cdot1) + (0\cdot1) + (0\cdot0) \\ (0\cdot0) + (0\cdot1) + (1\cdot1) + (1\cdot0) \end{pmatrix} = \frac{1}{2} \begin{pmatrix} 1 \\ 1 \end{pmatrix} = \frac{1}{2} (\vert A \rangle + \vert B \rangle)$$
#
# ## Mathematical Framework with a Diagonal Eraser
#
# To destroy the "which-way" information and recover the interference fringes, we place a diagonal polarizer in front of the detector screen. 
#
# A diagonal polarizer filters the incoming photons by projecting their polarization states onto the Diagonal state basis vector $|D\rangle$:
# $$|D\rangle = \frac{1}{\sqrt{2}}\big(|V\rangle + |H\rangle\big)$$
#
# ### 1. Projecting the Quantum State
# Recall the entangled spatial-polarization state arriving at position $x$ on the screen before the polarizer:
# $$|\psi(x)\rangle = \frac{1}{\sqrt{2}} \big(\psi_1(x)|V\rangle + \psi_2(x)|H\rangle\big)$$
#
# When the photon passes through the diagonal polarizer, the state is projected onto $\langle D|$. The new post-selection state vector $|\psi_D(x)\rangle$ becomes:
# $$|\psi_D(x)\rangle = |D\rangle\langle D|\psi(x)\rangle$$
#
# We compute the scalar probability amplitude coefficient $\langle D|\psi(x)\rangle$:
# $$\langle D|\psi(x)\rangle = \frac{1}{\sqrt{2}}\big(\langle V| + \langle H|\big) \cdot \frac{1}{\sqrt{2}}\big(\psi_1(x)|V\rangle + \psi_2(x)|H\rangle\big)$$
#
# Multiplying this out using the orthogonality rules ($\langle V|V\rangle = \langle H|H\rangle = 1$ and $\langle V|H\rangle = \langle H|V\rangle = 0$):
# $$\langle D|\psi(x)\rangle = \frac{1}{2}\big(\psi_1(x) + \psi_2(x)\big)$$
#
# ### 2. Computing the Recovered Intensity Profile
# The observed light intensity $I_D(x)$ behind the diagonal eraser is found by calculating the absolute square of this filtered amplitude:
# $$I_D(x) = \left|\langle D|\psi(x)\rangle\right|^2 = \frac{1}{4}\big(\psi_1(x) + \psi_2(x)\big)^*\big(\psi_1(x) + \psi_2(x)\big)$$
#
# Expanding this expression gives:
# $$I_D(x) = \frac{1}{4}|\psi_1(x)|^2 + \frac{1}{4}|\psi_2(x)|^2 + \frac{1}{4}\big(\psi_1^*(x)\psi_2(x) + \psi_2^*(x)\psi_1(x)\big)$$
#
# ### 3. Re-emergence of the Interference Fringes
# Unlike the previous step where the cross-terms vanished, the eraser has mixed the states together. By expressing the spatial wavefunctions in terms of their magnitudes and phase difference $\phi(x)$ (where $\psi_1^*(x)\psi_2(x) = |\psi_1(x)||\psi_2(x)|e^{i\phi(x)}$), the terms inside the parentheses collapse into a real cosine wave via Euler's identity:
#
# $$\psi_1^*(x)\psi_2(x) + \psi_2^*(x)\psi_1(x) = 2|\psi_1(x)||\psi_2(x)|\cos\phi(x)$$
#
# Assuming symmetric slits for simplicity ($|\psi_1(x)| = |\psi_2(x)| = |\psi_0(x)|$), the equation fully simplifies to:
# $$I_D(x) = \frac{1}{2}|\psi_0(x)|^2\big(1 + \cos\phi(x)\big)$$
#
# **Conclusion:** By erasing the distinct polarization tags and projecting them into a shared state, the path information is completely lost to the universe. As a direct result, the phase-dependent cross-term returns to the equation, and highly visible constructive and destructive **interference fringes re-emerge** on the detector screen.
#
# * **Without the Eraser:** The quantum state is perfectly entangled ($|\psi\rangle = \frac{1}{\sqrt{2}} [|1,V\rangle + |2,H\rangle]$). Because the polarization states are orthogonal ($\langle V|H\rangle = 0$), the mathematical cross-terms completely vanish. The universe retains "which-way" path information, destroying all interference.
# * **With the Eraser:** Passing the photons through a diagonal polarizer filters the light into a single, shared state ($|D\rangle$). This projection removes the distinguishing tags, rendering the paths identical again. The cross-terms re-emerge as a phase-dependent cosine wave, restoring the physical interference fringes.
#

# %% [markdown]
# ## Student Exercise: The Anti-Diagonal Polarizer
#
# Now that you have seen how a **Diagonal Polarizer** $|D\rangle$ erases which-way information to restore interference fringes, your task is to analyze what happens when we use an **Anti-Diagonal Polarizer** $|A\rangle$ instead.
#
# The Anti-Diagonal state vector is defined as:
# $$|A\rangle = \frac{1}{\sqrt{2}}\big(|V\rangle - |H\rangle\big)$$
#
# ### Your Tasks:
# 1. **Mathematical Derivation:** Following the exact same steps used for the diagonal polarizer, project the arriving state $|\psi(x)\rangle = \frac{1}{\sqrt{2}} \big(\psi_1(x)|V\rangle + \psi_2(x)|H\rangle\big)$ onto $\langle A|$. Compute the resulting filtered intensity profile $I_A(x) = \left|\langle A|\psi(x)\rangle\right|^2$.
# 2. **Phase Comparison:** How does your derived equation for $I_A(x)$ differ from the diagonal intensity profile $I_D(x)$? Pay close attention to the mathematical sign in front of the cosine/interference term.
# 3. **The Big Picture:** If you physically added the two independent intensity patterns together ($I_D(x) + I_A(x)$), what resulting pattern would you get? Why does this make physical sense considering conservation of energy and the "No Eraser" pattern?
#
# ---
#
# ### Hint for your derivation:
# * Recall that $\langle A|V\rangle = \frac{1}{\sqrt{2}}$ and $\langle A|H\rangle = -\frac{1}{\sqrt{2}}$.
# * Use Euler's identity to simplify the resulting cross-terms: $\psi_1^*(x)\psi_2(x) + \psi_2^*(x)\psi_1(x) = 2|\psi_1(x)||\psi_2(x)|\cos\phi(x)$.
#

# %%
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Parameter Setup
# ---------------------------------------------------------
x = np.linspace(-10, 10, 1000)  # Screen position coordinate

# Single-slit diffraction envelope (spatial wavefunction magnitudes)
envelope = np.sinc(x / 4.0) ** 2

# Cosine factor representing the phase difference between the paths
interference_term = np.cos(2 * np.pi * x / 2.0)

# ---------------------------------------------------------
# 2. Calculating the Three Intensity Profiles
# ---------------------------------------------------------
# 1. No Eraser: Simple sum of intensities (Cross-terms are 0)
no_erasure = envelope 

# 2. Diagonal Eraser: Cross-term returns with a POSITIVE sign
diagonal_erasure = envelope * (1 + interference_term) / 2.0

# 3. Anti-Diagonal Eraser: Cross-term returns with a NEGATIVE sign (Anti-fringes)
antidiagonal_erasure = envelope * (1 - interference_term) / 2.0

# ---------------------------------------------------------
# 3. Plotting the Results
# ---------------------------------------------------------
plt.figure(figsize=(11, 6.5))

# Plot the base "No Eraser" envelope
plt.plot(x, no_erasure, 
         label=r'No Eraser: $I_{Total}(x) = \frac{1}{2}|\psi_1|^2 + \frac{1}{2}|\psi_2|^2$', 
         color='yellow', linewidth=3.0, zorder=3)

# Plot the Diagonal Eraser fringes
plt.plot(x, diagonal_erasure, 
         label=r'Diagonal Eraser ($|D\rangle$ Fringes): $\propto (1 + \cos\phi)$', 
         color='dodgerblue', linestyle='--', linewidth=2.0)

# Plot the Anti-Diagonal Eraser anti-fringes
plt.plot(x, antidiagonal_erasure, 
         label=r'Anti-Diagonal Eraser ($|A\rangle$ Anti-fringes): $\propto (1 - \cos\phi)$', 
         color='darkorange', linestyle=':', linewidth=2.5)

# Formatting the visualization
plt.title('Quantum Eraser: Fringes, Anti-Fringes, and the Total Distribution', 
          fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Screen Position ($x$)', fontsize=12)
plt.ylabel('Normalized Intensity $I(x)$', fontsize=12)
plt.legend(loc='upper right', fontsize=10.5, framealpha=0.95, shadow=True)
plt.grid(True, linestyle=':', alpha=0.6)

# Display the output directly in Jupyter
plt.show()


# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 1: Ramsey Interference Baseline (System Only)
#
# A single qubit passing through $H \rightarrow R_z(\theta) \rightarrow H$ produces standard sinusoidal interference fringes:
#
# $$P(|0\rangle) = \cos^2\left(\frac{\theta}{2}\right)$$
#
# As long as no environmental state branches correlate with the internal path, coherence remains $100\%$.

# %% slideshow={"slide_type": "fragment"}
simulator = AerSimulator()

def run_ramsey_clean(theta_val):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.rz(theta_val, 0)
    qc.h(0)
    qc.measure(0, 0)
    res = simulator.run(qc, shots=1000).result().get_counts()
    return res.get('0', 0) / 1000

thetas = np.linspace(0, 2 * np.pi, 50)
p0_clean = [run_ramsey_clean(th) for th in thetas]

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(thetas, p0_clean, color='#00FF66', linewidth=2, label='Coherent Ramsey Interference')
ax.set_xlabel('Phase Angle $\\theta$ (rad)')
ax.set_ylabel('Probability $P(|0\\rangle)$')
ax.set_title('Baseline Coherent Interference Sweep')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 2: Environmental Entanglement & Decoherence
#
# Introducing an environmental "Which-Way" detector qubit (qubit 1) via a CNOT gate correlates path information with the environment:
#
# $$|\psi\rangle = \frac{1}{\sqrt{2}}\left(|0\rangle_S |0\rangle_E + e^{i\theta}|1\rangle_S |1\rangle_E\right)$$
#
# Tracing out the environment destroys subsystem phase visibility, flattening the Ramsey fringe to $P(|0\rangle) = 0.5$.

# %% slideshow={"slide_type": "subslide"}
def run_ramsey_decohered(theta_val):
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.rz(theta_val, 0)
    
    # Entangle with Environment (Which-Way Marker)
    qc.cx(0, 1)
    
    qc.h(0)
    qc.measure(0, 0)  # Measure System Qubit only
    res = simulator.run(qc, shots=1000).result().get_counts()
    return res.get('0', 0) / 1000

p0_decohered = [run_ramsey_decohered(th) for th in thetas]

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(thetas, p0_clean, '--', color='#00FF66', alpha=0.5, label='Coherent Baseline')
ax.plot(thetas, p0_decohered, color='#FF007F', linewidth=2, label='Decohered (Which-Way Marked)')
ax.set_xlabel('Phase Angle $\\theta$ (rad)')
ax.set_ylabel('Probability $P(|0\\rangle)$')
ax.set_title('Decoherence via Environmental State Branching')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 3: Reversibility via $U^\dagger$ Uncomputation
#
# Decoherence is not an irreversible loss of physical information; it is the dispersion of phase into correlations.
#
# Applying the exact inverse unitary operation ($U^\dagger = \text{CNOT}^\dagger$) **uncomputes** the environmental record, completely restoring $100\%$ interference visibility.

# %% slideshow={"slide_type": "subslide"}
def run_ramsey_uncomputed(theta_val):
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.rz(theta_val, 0)
    
    # Forward Entanglement
    qc.cx(0, 1)
    
    # Coherent Uncomputation (U-dagger)
    qc.cx(0, 1)
    
    qc.h(0)
    qc.measure(0, 0)
    res = simulator.run(qc, shots=1000).result().get_counts()
    return res.get('0', 0) / 1000

p0_uncomputed = [run_ramsey_uncomputed(th) for th in thetas]

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(thetas, p0_decohered, ':', color='#FF007F', label='Decohered')
ax.plot(thetas, p0_uncomputed, 'o-', color='#00D2FF', label=r'Restored via $U^\dagger$ Uncomputation', markersize=4)
ax.set_xlabel('Phase Angle $\\theta$ (rad)')
ax.set_ylabel('Probability $P(|0\\rangle)$')
ax.set_title(r'Quantum Information Recovery via Unitary Inversion ($U^\dagger$)')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 4: Basis Erasure & Coincidence Correlations
#
# If the environment cannot be uncomputed directly, measuring the detector qubit in the **diagonal basis** ($|+\rangle / |-\rangle$) erases which-way information.
#
# Sorting system outcomes conditional on the detector result recovers anti-correlated interference fringes ($P_{|+ \rangle}(\theta)$ vs $P_{|- \rangle}(\theta)$).

# %% slideshow={"slide_type": "subslide"}
cache_file = 'data/eraser_coincidence_cache.pkl'

if os.path.exists(cache_file):
    print("Loading cached coincidence data from data/eraser_coincidence_cache.pkl...")
    with open(cache_file, 'rb') as f:
        cache_data = pickle.load(f)
    p0_given_env_plus, p0_given_env_minus = cache_data['p0_plus'], cache_data['p0_minus']
else:
    print("Simulating Quantum Eraser coincidence measurements...")
    p0_given_env_plus = []
    p0_given_env_minus = []

    for th in thetas:
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.rz(th, 0)
        qc.cx(0, 1)  # Entangle
        qc.h(0)      # System recombine
        
        # Erase detector in Hadamard basis
        qc.h(1)
        qc.measure([0, 1], [0, 1])
        
        counts = simulator.run(qc, shots=2000).result().get_counts()
        
        # System = 0 given Detector = 0 (|+)
        c_00 = counts.get('00', 0)
        c_10 = counts.get('10', 0)
        p0_plus = c_00 / (c_00 + c_10) if (c_00 + c_10) > 0 else 0.5
        
        # System = 0 given Detector = 1 (|-)
        c_01 = counts.get('01', 0)
        c_11 = counts.get('11', 0)
        p0_minus = c_01 / (c_01 + c_11) if (c_01 + c_11) > 0 else 0.5
        
        p0_given_env_plus.append(p0_plus)
        p0_given_env_minus.append(p0_minus)

    with open(cache_file, 'wb') as f:
        pickle.dump({'p0_plus': p0_given_env_plus, 'p0_minus': p0_given_env_minus}, f)

# Plot Coincidence Eraser Fringes
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(thetas, p0_given_env_plus, 'o-', color='#00FF66', label=r'Conditional on Detector $|+\rangle$')
ax.plot(thetas, p0_given_env_minus, 's-', color='#FF007F', label=r'Conditional on Detector $|-\rangle$')
ax.plot(thetas, p0_decohered, '--', color='gray', alpha=0.5, label='Unconditioned Total (Flat)')
ax.set_xlabel('Phase Angle $\\theta$ (rad)')
ax.set_ylabel('Conditional Probability $P(|0\\rangle_S)$')
ax.set_title('Quantum Eraser Coincidence Fringe Recovery')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 5: Exercise 1 — Polarization-Based Quantum Eraser
#
# **Task:** Instead of a full CNOT flip, replace the environmental entanglement with a parameterized controlled rotation $CRY(\phi)$ on Qubit 1.
#
# This mimics placing a Half-Wave Plate (HWP) at variable angle $\phi \in [0, \pi/2]$ in one path of a Mach-Zehnder Interferometer:
#
# - **$\phi = 0$:** No polarization rotation (No which-way information, $V = 1.0$)
# - **$\phi = \pi/2$:** Full orthogonal polarization shift (Complete which-way marking, $V = 0.0$)
#
# We compute fringe visibility $V(\phi) = \frac{I_{\text{max}} - I_{\text{min}}}{I_{\text{max}} + I_{\text{min}}}$ as a function of continuous entanglement angle $\phi$.

# %% slideshow={"slide_type": "subslide"}
# Executable Student Code: Parameterized Polarization Entanglement Sweep
phi_angles = np.linspace(0, np.pi / 2, 25)
visibilities = []

for phi in phi_angles:
    p0_sweep = []
    # Measure Ramsey curve for a specific polarization angle phi
    for th in np.linspace(0, 2 * np.pi, 20):
        qc_pol = QuantumCircuit(2, 1)
        qc_pol.h(0)
        qc_pol.rz(th, 0)
        
        # Parameterized environmental marking (HWP equivalent)
        qc_pol.cry(phi, 0, 1)
        
        qc_pol.h(0)
        qc_pol.measure(0, 0)
        
        res = simulator.run(qc_pol, shots=1000).result().get_counts()
        p0_sweep.append(res.get('0', 0) / 1000)
    
    # Calculate Fringe Visibility V = (max - min) / (max + min)
    i_max = np.max(p0_sweep)
    i_min = np.min(p0_sweep)
    v = (i_max - i_min) / (i_max + i_min) if (i_max + i_min) > 0 else 0.0
    visibilities.append(v)

# Plot Visibility Decay vs Polarization Angle
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(phi_angles, visibilities, 'o-', color='#00D2FF', linewidth=2, label=r'Simulated Visibility $V(\phi)$')
ax.plot(phi_angles, np.cos(phi_angles / 2), '--', color='#FF007F', label=r'Theoretical Bound $\cos(\phi/2)$')
ax.set_xlabel('Polarization Rotation Angle $\\phi$ (rad)')
ax.set_ylabel('Fringe Visibility $V$')
ax.set_title('Exercise 1: Ramsey Fringe Visibility vs Which-Way Marking Angle')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Exercise 4: Uncomputation Limits under Environmental Noise
#
# In Section 3, we assumed the inverse operator $U^\dagger$ can perfectly undo environmental entanglement. However, physical environments undergo amplitude damping (photon decay).
#
# 1. **Noisy Channel:** If the environmental qubit has a probability $\gamma \in [0, 1]$ of decaying to $|0\rangle$ before $U^\dagger$ is applied, derive the reduced density matrix $\rho_S$ of the system.
# 2. **Recoverable Visibility:** Calculate the maximum recoverable fringe visibility $V(\gamma)$ as a function of the decay parameter $\gamma$.
# 3. **Conceptual Check:** Distinguish between **decoherence** (reversible phase dispersion into subsystem correlations) and **dissipation** (irreversible loss of information to an unmeasured reservoir).

# %% [markdown]
#

# %%
