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
