# %% [markdown] slideshow={"slide_type": "slide"}
# # Module 01: From Classical Optics Matrix Algebra to Ramsey Interference
# ### Conserved Many-Worlds & State-Capacity Exploration ($\mathcal{C}_{\text{max}}$)
#
# **Roadmap:**
# 1. Physical Wave Optics & Classical $2\times2$ Transfer Matrix Algebra
# 2. Dirac Bra-Ket Notation & Hilbert Vector Space
# 3. Superposition & Single-Qubit Unitary Operators
# 4. Experimental Ramsey Fringe Coherence Sweep

# %% slideshow={"slide_type": "skip"}
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from utils import show_img
plt.style.use('dark_background')
os.makedirs('data', exist_ok=True)

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 0: Mach-Zehnder Interferometer
# In Mach-Zehnder Interferometry (ZMI), 2 beam splitters will create a total of 4 beam paths, combining into 2 images.
#

# %%
show_img("./images/ZMI-classic.png",'By <a href="//commons.wikimedia.org/wiki/User:Stigmatella_aurantiaca" title="User:Stigmatella aurantiaca">Stigmatella aurantiaca</a> with modification by <a href="//commons.wikimedia.org/w/index.php?title=User:Kid222r&amp;action=edit&amp;redlink=1" class="new" title="User:Kid222r (page does not exist)">Kid222r</a> - <a href="//commons.wikimedia.org/wiki/File:Mach_Zehnder_interferometer.svg" title="File:Mach Zehnder interferometer.svg">File:Mach Zehnder interferometer.svg</a>, <a href="https://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=74141621">Link</a>')

# %% [markdown]
# Image 1 will be composed of:
#
# * Arm 1, which for image 1 experiences of phase shift of $\phi\$ + 3 reflections.
# * Arm 2, which for image 1 experiences 1 reflection (and 2 transmissions).
#
# Since both arms experience an odd number of reflections, they will change from sin to cos functions (with arm 1 also shifted by $\phi$)
#
# Image 2 will be composed of:
#
# * Arm 1, which for image 2 experiences a phase shift of $\phi\$ + 2 reflections
# * Arm 2, which for image 2 experiences 2 reflection (and 1 transmissions).
#
# They will remain sin functions.
#
# They then combine into two sperate images, where the phase shift will result in:
# $$I_1 = I_0 \cos^2\frac{\phi}{2}$$
# $$I_2 = I_0 \sin^2\frac{\phi}{2}$$
#
# This is due to the trig identity $\cos({t})+\cos({t+\phi})=2\cos({\frac{\phi}{2}})\cos({t+\frac{\phi}{2}})$, then squaring to get Intensity, and averaging over time we get $I\propto\cos^2({\frac{\phi}{2}})$, and equivalent sin identities.
#
# ZMI is useful to show changes in the properties of air, for studying aerodynamics or to visualise heat.
#
# To conserve energy, the beam must have split so that on average:
# $$E_1 = E_2 = \frac{1}{\sqrt{2}}E_0$$
#
# But if we want to use imaginary numbers to show the waveform:
#
# $$E_1 = \frac{1}{\sqrt{2}}E_0$$
# $$E_2 = \frac{1}{\sqrt{2}}E_0\times e^{i\phi}$$
#
# ### Exercise - you could check this more carefully, explicitly doing all path difference / wave number differences and trig ....

# %% [markdown]
# ## Section 1: Classical Optics Matrix Algebra (Mach-Zehnder Interferometer)
#
#
# In classical wave optics, an optical path through a Mach-Zehnder Interferometer (MZI) is modeled using $2 \times 2$ transfer matrices acting on complex electric field amplitude vectors $\mathbf{E} = \begin{pmatrix} E_0 \\ E_1 \end{pmatrix}$:
#
# $E_0$ will be the field strength of waves moving horizontally, and $E_1$ will be the field strenth of waves moving vertically.
#   
#
# - **Beam Splitter Matrix ($T_{BS}$):** $T_{BS} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix}$, if a photon (or part of the beam) is moving horizontally it will hit a beam splitter then split into a horizontal component, and a vertical phase shifted component (and similarly a vertical beam will split into an unshifted vertical beam, and a shifted horizontal beam). 
#
#
#   
# - **Phase Shift Matrix ($P(\theta)$):** $P(\theta) = \begin{pmatrix} e^{i\theta} & 0 \\ 0 & 1 \end{pmatrix}$ - only the horizontal beam is phase shifted (depending on the diagram you could change it so that only the vertical beam is shifted). 
#
# The full classical MZI system transformation matrix $M_{MZI}$ is the matrix product:
#
# $$M_{MZI} = T_{BS} \cdot P(\theta) \cdot T_{BS}$$

# %%
show_img('images/ZMI.gif','By <a href="//commons.wikimedia.org/wiki/User:L3erdnik" title="User:L3erdnik">L3erdnik</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/publicdomain/zero/1.0/deed.en" title="Creative Commons Zero, Public Domain Dedication">CC0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=155028116">Link</a>')


# %% slideshow={"slide_type": "subslide"}
# Classical Optical Transfer Matrix Functions
def T_BS():
    return (1 / np.sqrt(2)) * np.array([[1, 1j], 
                                        [1j, 1]], dtype=complex)

def P_phase(theta):
    return np.array([[np.exp(1j * theta), 0], 
                     [0, 1]], dtype=complex)

# Initial classical beam in Port 0: E_in = [1, 0]^T
E_in = np.array([1, 0], dtype=complex)

# Calculate classical intensity interference curve across theta in [0, 2pi]
thetas = np.linspace(0, 2 * np.pi, 100)
I_out_port0 = []

for th in thetas:
    M_MZI = T_BS() @ P_phase(th) @ T_BS()
    E_out = M_MZI @ E_in
    # Classical Intensity I = |E|^2
    I_out_port0.append(np.abs(E_out[0])**2)

# Plot Classical Wave Interference
fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(thetas, I_out_port0, color='#00D2FF', linewidth=2, label=r'Classical Intensity $I(\theta) = \cos^2(\theta/2)$')
ax.set_xlabel('Relative Phase Shift $\theta$ (rad)')
ax.set_ylabel('Normalized Output Intensity $I_0$')
ax.set_title('Classical Wave Optics MZI Matrix Simulation')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 2: Dirac Bra-Ket Notation & Vector Space
#
# Quantum mechanics translates classical path vectors into state vectors in a 2D Hilbert space $\mathcal{H}$:
#
# - **Ket Vector $|0\rangle$:** Represents state vector $\begin{pmatrix} 1 \\ 0 \end{pmatrix}$
# - **Ket Vector $|1\rangle$:** Represents state vector $\begin{pmatrix} 0 \\ 1 \end{pmatrix}$
# - **Bra Vector $\langle\psi|$:** Conjugate transpose $(|\psi\rangle^\dagger = \alpha^* \langle 0| + \beta^* \langle 1|)$
#
# In the Copenhargen interpretation, the Bra vector is the measurment, and it should give you the probabilities (or probability amplitudes) as the system collapses.
#
# In a many worlds interpretation, there never is a Bra vector, the measurment itself is a ket as well (but now there are essentially two universes).
#
# Inner product yields probability amplitude ($\langle \phi | \psi \rangle$), and Born's rule gives measurement probability ($P = |\langle \phi | \psi \rangle|^2$).

# %% slideshow={"slide_type": "subslide"}
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

# Superposition state: |+> = (1/sqrt(2))(|0> + |1>)
ket_plus = (1 / np.sqrt(2)) * (ket_0 + ket_1)
bra_plus = ket_plus.conj().T

# Inner product <+|---------------+
norm = np.dot(bra_plus, ket_plus)
print(f"Norm <+|---------------+ = {norm.real:.3f} (Probability conserved)")

# %% [markdown]
# ### Converting a Beam Splitter to a Hadamard Gate
#
# A standard physical $50:50$ beam splitter matrix $U_{BS}$ introduces a phase shift of $i = e^{i\pi/2}$ on reflection:
#
# $$U_{BS} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix}$$
#
# If the vertical beams are phase shifted before and after the beam splitter:
#
# $$R = \begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix}$$
#
# This can make a Hadamard Gate $H$, and important quantum computing component:
#
# $$H = R \cdot U_{BS} \cdot R$$
#
# $$\begin{aligned}
# H &= \begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix} \left[ \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix} \right] \begin{pmatrix} 1 & 0 \\ 0 & -i \end{pmatrix} \\
# &= \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
# \end{aligned}$$

# %% [markdown]
# #### Why Is the Hadamard Gate Important?
#
# Classical computers start with bits set to `0`. Quantum algorithms almost always start by applying a Hadamard gate to every qubit initialized at $|0\rangle$. 
#
# This transforms classical states into equal superpositions:
#
# $$H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}} = |+\rangle$$
#
# In quantum mechanics, measuring along the standard computational basis ($Z$-axis) asks: *"Are you $|0\rangle$ or $|1\rangle$?"*
#
# Applying $H$ before a measurement changes the basis from the $Z$-axis to the $X$-axis ($|+\rangle$ and $|-\rangle$). This allows algorithms to read out quantum phase information that would otherwise be lost during standard $Z$-basis collapse.
#
# While $H$ operates on single qubits, combining it with a two-qubit **CNOT** gate creates maximum entanglement (a Bell state):
#
# $$\left(|00\rangle\right) \xrightarrow{\text{H on Qubit 1}} \frac{|00\rangle + |10\rangle}{\sqrt{2}} \xrightarrow{\text{CNOT}} \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$
#
# Without the Hadamard gate to generate the initial superposition, multi-qubit conditional gates could never create entangled states.
#
# Because $H$ is Hermitian and Unitary, applying it twice returns the qubit to its original state:
#
# $$H \cdot H = I$$
#
# This self-inverting property is heavily exploited in algorithms

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 3: Superposition & Single-Qubit Unitary Operators
#
# Qiskit includes the **Hadamard Gate ($H$)**:
#
# $$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$

# %% slideshow={"slide_type": "fragment"}
# Execute single-qubit Hadamard superposition in Qiskit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

simulator = AerSimulator()
counts = simulator.run(qc, shots=1000).result().get_counts()

plot_histogram(counts, title="Single Qubit Measurement in Superposition (|---------------+)", color='#00D2FF')

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 4: Ramsey Fringe Interference Sweep
#
# The classical MZI transfer sequence ($T_{BS} \cdot P(\theta) \cdot T_{BS}$) is mapped directly to a quantum **Ramsey Interferometry Sequence**:
#
# $$\text{Sequence}: H \rightarrow R_z(\theta) \rightarrow H \rightarrow \text{Measure}$$

# %% slideshow={"slide_type": "subslide"}
cache_file = 'data/ramsey_cache.pkl'

if os.path.exists(cache_file):
    print("Loading cached simulation data from data/ramsey_cache.pkl...")
    with open(cache_file, 'rb') as f:
        cache_data = pickle.load(f)
    angles, p0_list = cache_data['angles'], cache_data['p0_list']
else:
    print("Running Qiskit Ramsey Fringe simulation sweep...")
    angles = np.linspace(0, 2 * np.pi, 50)
    p0_list = []
    
    for theta in angles:
        qc_ramsey = QuantumCircuit(1, 1)
        qc_ramsey.h(0)
        qc_ramsey.rz(theta, 0)
        qc_ramsey.h(0)
        qc_ramsey.measure(0, 0)
        
        result = simulator.run(qc_ramsey, shots=1000).result().get_counts()
        p0_list.append(result.get('0', 0) / 1000)
    
    with open(cache_file, 'wb') as f:
        pickle.dump({'angles': angles, 'p0_list': p0_list}, f)

# Plotting Ramsey Fringe Oscillations
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(angles, p0_list, 'o-', color='#00FF66', label='Quantum Simulated P(|0⟩)', linewidth=2)
ax.plot(thetas, I_out_port0, '--', color='#00D2FF', label='Classical Wave Intensity Limit')
ax.set_xlabel('Phase Angle θ (radians)')
ax.set_ylabel('Probability / Intensity')
ax.set_title('Ramsey Fringe vs Classical MZI Interference Sweep')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Exercise 2: Position-Momentum Complementarity in Continuous Systems
#
# Consider a particle of mass $m$ passing through a double slit with separation $d$. The spatial wavefunction on a screen at position $x$ is given by:
#
# $$\psi(x) = \frac{1}{\sqrt{2}} \Big( \psi_1(x) + e^{i \phi(x)} \psi_2(x) \Big)$$
#
# 1. **State Branching:** Suppose each slit contains a microscopic spin-1/2 particle that flips its state ($|\uparrow\rangle \rightarrow |\downarrow\rangle$) when the photon passes through Slit 2. Derive the spatial density matrix $\rho(x, x') = \text{Tr}_{\text{spin}}(|\Psi\rangle \langle \Psi|)$ after tracing out the spin degree of freedom.
# 2. **Phase Erasure:** Show mathematically why the continuous interference term $\cos(\phi(x))$ vanishes in the diagonal probability density $\rho(x, x)$.
# 3. **Coincidence Recovery:** If an observer measures the spin particle in the transverse basis $|+\rangle = \frac{1}{\sqrt{2}}(|\uparrow\rangle + |\downarrow\rangle)$, prove how filtering screen detections $x$ conditional on outcome $|+\rangle$ recovers the continuous fringe pattern.

# %%
