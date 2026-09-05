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

# %% [markdown]
# ### The CNOT gate
#
# A CNOT (controlled not) gate will flip the second qubit, but only if the the first qubit is 1.
#
# $$
# \text{CNOT} = \begin{pmatrix} 
# 1 & 0 & 0 & 0 \\ 
# 0 & 1 & 0 & 0 \\ 
# 0 & 0 & 0 & 1 \\ 
# 0 & 0 & 1 & 0 
# \end{pmatrix}
# $$
#
# ### CNOT Bit-Flip Example
#
# When the control qubit is set to $|1\rangle$, the CNOT gate acts as a NOT gate (bit-flip) on the target qubit. 
#
# ---
#
# ### 1. Initial Conditions
# We initialize the system to the state where the **Control is $|1\rangle$** and the **Target is $|0\rangle$**.
#
# * **Bra-Ket Form:**  
#   $$|\psi_{\text{in}}\rangle = |1\rangle_C \otimes |0\rangle_T = |10\rangle$$
#
# * **Vector Form:**  
#   Under the standard computational basis ordered as $\{|00\rangle, |01\rangle, |10\rangle, |11\rangle\}$, the initial state vector is:
#   $$|\psi_{\text{in}}\rangle = \begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix}$$
#
# ---
#
# ### 2. Matrix Multiplication Form
# Applying the ideal CNOT matrix operator to the input state vector yields:
#
# $$
# |\psi_{\text{out}}\rangle = \text{CNOT} \, |\psi_{\text{in}}\rangle = 
# \begin{pmatrix} 
# 1 & 0 & 0 & 0 \\ 
# 0 & 1 & 0 & 0 \\ 
# 0 & 0 & 0 & 1 \\ 
# 0 & 0 & 1 & 0 
# \end{pmatrix} 
# \begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix} = 
# \begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}
# $$
#
# ---
#
#
# $$
# \begin{aligned}
# \text{CNOT}|10\rangle &= |11\rangle
# \end{aligned}
# $$
#
#
#

# %% [markdown]
# ### Generating a Bell State Using Kronecker Products
#
# To create the entangled Bell State $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$, we track two qubits initialized to $|0\rangle_C |0\rangle_T$.
#
# ---
#
# ### Step 1: Initialize the System Vector
# The input state is $|00\rangle$. Mathematically, this is the Kronecker product ($\otimes$) of two single-qubit vectors:
#
# $$
# |0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}
# $$
#
# $$
# |\psi_0\rangle = |0\rangle \otimes |0\rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 1 \cdot 1 \\ 1 \cdot 0 \\ 0 \cdot 1 \\ 0 \cdot 0 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}
# $$
#
# ---
#
# ### Step 2: Apply the Hadamard Gate to QuBit 1
# We apply a Hadamard gate ($H$) to the Control qubit while leaving the Target qubit unchanged using the Identity matrix ($I$). 
#
# #### 2a. Building the $4 \times 4$ Operator Matrix
# We expand the local operations into the full 2-qubit space using the Kronecker product ($H \otimes I$):
#
# $$
# H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}, \quad I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}
# $$
#
# $$
# H \otimes I = \frac{1}{\sqrt{2}} \begin{pmatrix} 1\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} & 1\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \\ 1\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} & -1\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 1 & 0 & -1 & 0 \\ 0 & 1 & 0 & -1 \end{pmatrix}
# $$
#
# #### 2b. Computing the Superposition State Vector
# Multiplying this expanded matrix by our initial state vector puts the control qubit into a superposition:
#
# $$
# |\psi_1\rangle = (H \otimes I)|\psi_0\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 1 & 0 & -1 & 0 \\ 0 & 1 & 0 & -1 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix} = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 0 \\ 1 \\ 0 \end{pmatrix}
# $$
# *(This vector represents the unentangled state $\frac{1}{\sqrt{2}}(|00\rangle + |10\rangle)$).*
#
# ---
#
# ### Step 3: Apply the CNOT Gate to Entangle the Qubits
# Finally, we apply the standard $4 \times 4$ CNOT matrix directly to our state vector $|\psi_1\rangle$:
#
# $$
# |\psi_{\text{out}}\rangle = \text{CNOT} |\psi_1\rangle = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & 1 & 0 \end{pmatrix} \cdot \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 0 \\ 1 \\ 0 \end{pmatrix}
# $$
#
# Evaluating the row multiplications:
# * Row 1: $1 \cdot 1 = 1$
# * Row 2: $1 \cdot 0 = 0$
# * Row 3: $1 \cdot 0 = 0$ (the 1 in the vector gets multiplied by the 0 in row 3)
# * Row 4: $1 \cdot 1 = 1$ (the 1 in the vector gets multiplied by the 1 in row 4)
#
# $$
# |\psi_{\text{out}}\rangle = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 \\ 0 \\ 0 \\ 1 \end{pmatrix}
# $$
#
# ### Final Result
# The resulting vector has amplitudes only at the first index ($|00\rangle$) and the last index ($|11\rangle$):
#
# $$
# |\psi_{\text{out}}\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle) = |\Phi^+\rangle
# $$
#

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 3: Superposition & Single-Qubit Unitary Operators
#
# Qiskit includes the **Hadamard Gate ($H$)**:
#
# $$H = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$$
#

# %% slideshow={"slide_type": "fragment"}
# Execute single-qubit Hadamard superposition in Qiskit
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

simulator = AerSimulator()
counts = simulator.run(qc, shots=1000).result().get_counts()

plot_histogram(counts, title="Single Qubit Measurement in Superposition (|---------------+)", color='#00D2FF')

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 4: Interference Sweep
#
# It closely resembles the Mach-Zehnder interferometer -https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Quantum_Tutorials_(Rioux)/07%3A_Quantum_Optics/7.23%3A_The_Ramsey_Atomic_Interferometer
#
# The classical MZI transfer sequence ($T_{BS} \cdot P(\theta) \cdot T_{BS}$) is mapped directly to a quantum **Ramsey Interferometry Sequence**:
#
# $$\text{Sequence}: H \rightarrow R_z(\theta) \rightarrow H \rightarrow \text{Measure}$$
#
# ### Mapping Classical MZI to Quantum Ramsey Interferometry
#
# The mathematical transformation sequence for a classical Mach-Zehnder Interferometer (MZI) maps directly onto a quantum Ramsey sequence. 
#
# | Physical Feature | Classical MZI | Quantum Ramsey Sequence |
# | :--- | :--- | :--- |
# | **System Basis** | Two Spatial Paths ($|path_1\rangle, |path_2\rangle$) | Two Energy Levels ($|0\rangle, |1\rangle$) |
# | **Mixing Element** | 50:50 Beam Splitter ($T_{BS}$) | $\pi/2$ Radio-Frequency Pulse ($R_{\pi/2}$) |
# | **Phase Shift** | Optical Delay Line / Phase Shifter ($P(\theta)$) | Free Precession / Detuning ($U_{\Delta t}$) |
#
# ---
#
# ### 1. Matrix Component Equivalence
#
# #### A. The Beam Splitter vs. $\pi/2$ Pulse
# A classical symmetric 50:50 beam splitter splits power evenly and introduces a $90^\circ$ ($i$) phase shift on reflection. In quantum mechanics, a $\pi/2$ pulse creates an equal superposition of states. 
#
# Up to a global phase factor, both operations are represented by the identical unitary matrix (often written using the Hadamard operator $H$ or a $Y$-rotation):
#
# $$
# T_{BS} = R_{\pi/2} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix}
# $$
#
# #### B. The Path Phase Shift vs. Free Precession
# In an MZI, a piece of glass in one arm retards the phase of that path by $\theta$. In a Ramsey sequence, letting the qubit sit idle for a duration $\Delta t$ causes its state to acquire a phase difference $\theta = \Delta \omega \cdot \Delta t$ relative to the driving laser clock (where $\Delta \omega$ is the detuning frequency).
#
# $$
# P(\theta) = U_{\Delta t} = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\theta} \end{pmatrix}
# $$
#
# ---
#
# ### 2. The Transfer Sequence Multiplication
#
# The complete transfer sequence is computed by multiplying the operators from right to left: 
# $$\text{Total Transformation} = T_{BS} \cdot P(\theta) \cdot T_{BS}$$
#
# #### Step 2a: First Split and Phase Shift
# Multiplying the phase shift matrix by the first beam splitter matrix yields:
#
# $$
# P(\theta) \cdot T_{BS} = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\theta} \end{pmatrix} \cdot \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix} = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & i \\ i e^{i\theta} & e^{i\theta} \end{pmatrix}
# $$
#
# #### Step 2b: Final Recombination Matrix
# Multiplying the second beam splitter matrix by the result of Step 2a yields the total transfer matrix:
#
# $$
# M_{\text{total}} = \frac{1}{2}\begin{pmatrix} 1 & i \\ i & 1 \end{pmatrix} \begin{pmatrix} 1 & i \\ i e^{i\theta} & e^{i\theta} \end{pmatrix}
# $$
#
# Evaluating the matrix elements:
# * **Top Left:** $1(1) + i(ie^{i\theta}) = 1 - e^{i\theta}$
# * **Top Right:** $1(i) + i(e^{i\theta}) = i(1 + e^{i\theta})$
# * **Bottom Left:** $i(1) + 1(ie^{i\theta}) = i(1 + e^{i\theta})$
# * **Bottom Right:** $i(i) + 1(e^{i\theta}) = -1 + e^{i\theta}$
#
# $$
# M_{\text{total}} = \frac{1}{2} \begin{pmatrix} 1 - e^{i\theta} & i(1 + e^{i\theta}) \\ i(1 + e^{i\theta}) & e^{i\theta} - 1 \end{pmatrix}
# $$
#
# ---
#
# ### 3. Physical Interference Output
#
# If we initialize the system in the baseline state ($|path_1\rangle$ for MZI, or ground state $|0\rangle = \begin{pmatrix}1 \\ 0\end{pmatrix}$ for Ramsey):
#
# $$
# |\psi_{\text{out}}\rangle = M_{\text{total}} \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \frac{1}{2} \begin{pmatrix} 1 - e^{i\theta} \\ i(1 + e^{i\theta}) \end{pmatrix}
# $$
#
# #### Finding the Transition Probability
# The probability of detecting the particle in the second output channel ($|path_2\rangle$ or excited state $|1\rangle$) is found by taking the absolute square of the bottom element:
#
# $$
# P_{\text{transition}} = \left| \frac{i}{2}(1 + e^{i\theta}) \right|^2 = \frac{1}{4}(1 + e^{i\theta})(1 + e^{-i\theta}) = \frac{1}{4}(2 + e^{i\theta} + e^{-i\theta})
# $$
#
# Using Euler's identity $\cos\theta = \frac{e^{i\theta} + e^{-i\theta}}{2}$:
#
# $$
# P_{\text{transition}} = \frac{1}{2}(1 + \cos\theta) = \cos^2\left(\frac{\theta}{2}\right)
# $$
#
# #### Conclusion
# Whether measuring **classical optical fringe intensity** in an MZI or tracking **quantum population oscillations (Ramsey fringes)** in an atomic clock, the exact same trigonometric $\cos^2(\theta/2)$ mathematical relationship governs the system.
#

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

# %% [markdown]
# ## Optional CNOT using optics

# %%
show_img('images/KLM_CNOT.png',"Demonstration of an optical quantum controlled-NOT gate without path interference Okamoto, Hofmann, Takeuchi, Sasaki")

# %% [markdown]
# A partially polarising beam splitter (PPBS in the diagram above, not to be comfused with a polarisation preserving beam splitter) by  Okamoto et al. 2005:
#
#
# The gate operates in the coincidence basis where:
# * Horizontal polarisation: $|H\rangle = |0\rangle$
# * Vertical polarisation: $|V\rangle = |1\rangle$
#
#
# ### A. Intrinsic Central Element ($PPBS_A$)
# The central mixing beam splitter handles polarization components according to:
# * **Vertical ($V$)**: Reflects perfectly ($R_V = 1 \implies r_V = 1$).
# * **Horizontal ($H$)**: Reflects $1/3$ and transmits $2/3$ ($R_H = 1/3, T_H = 2/3$).
#
# Following the standard phase conventions, its path transformation matrices are:
# $$
# M_{A, H} = \begin{pmatrix} \sqrt{\frac{2}{3}} & \sqrt{\frac{1}{3}} \\ \sqrt{\frac{1}{3}} & -\sqrt{\frac{2}{3}} \end{pmatrix}, \quad M_{A, V} = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}
# $$
#
# ### B. Supplemental Attenuating Elements ($PPBS_B$)
# The two $PPBS_B$ elements act exclusively to balance amplitudes. Unlike $PPBS_A$, they **transmit $H$ perfectly ($T_H = 1$)** and **transmit only $1/3$ of $V$ ($T_V = 1/3$)**. Their inline single-path transmission operator is:
# $$
# T_B = \begin{pmatrix} 1 & 0 \\ 0 & \sqrt{\frac{1}{3}} \end{pmatrix}
# $$
#
# ---
#
# ### Coincidence-Filtered Path Amplitudes 
#
# When tracking two photons interacting across the network, we only accept outcomes where **exactly one photon exits the Control path and one photon exits the Target path** (Post-Selection). 
#
# ### Case 1: $|HH\rangle$ (Both Transmit)
# * $PPBS_B$ elements leave $H$ unattenuated ($1 \times 1 = 1$).
# * At $PPBS_A$, both photons transmit: $\sqrt{2/3} \times \sqrt{2/3} = 2/3$.
# $$\psi_{\text{out}} = \frac{2}{3}|HH\rangle$$
#
# ### Case 2: $|HV\rangle$ (H Transmits, V Reflects)
# * $PPBS_{B1}$ leaves $H_C$ at $1$. $PPBS_{B2}$ scales $V_T$ by $\sqrt{1/3}$.
# * At $PPBS_A$, $H_C$ transmits ($\sqrt{2/3}$) and $V_T$ reflects ($1$).
# $$\psi_{\text{out}} = (1) \times \left(\sqrt{\frac{2}{3}} \cdot 1\right) \times \left(\sqrt{\frac{1}{3}}\right)|HV\rangle = \sqrt{\frac{2}{9}}|HV\rangle = \frac{\sqrt{2}}{3}|HV\rangle$$
#
# ### Case 3: $|VH\rangle$ (V Reflects, H Transmits)
# * $PPBS_{B1}$ scales $V_C$ by $\sqrt{1/3}$. $PPBS_{B2}$ leaves $H_T$ at $1$.
# * At $PPBS_A$, $V_C$ reflects into the target output ($1$) and $H_T$ reflects into the control output with a unitary phase shift ($-\sqrt{1/3}$).
# $$\psi_{\text{out}} = \left(\sqrt{\frac{1}{3}}\right) \times \left(-\sqrt{\frac{1}{3}} \cdot 1\right) \times (1)|VH\rangle = -\frac{1}{3}|VH\rangle$$
#
# ### Case 4: $|VV\rangle$ (Both Reflect)
# * Both $PPBS_B$ elements scale the $V$ amplitudes: $\sqrt{1/3} \times \sqrt{1/3} = 1/3$.
# * At $PPBS_A$, both photons reflect perfectly ($1 \times 1 = 1$), swapping paths.
# $$\psi_{\text{out}} = \left(\sqrt{\frac{1}{3}}\right) \times (1 \times 1) \times \left(\sqrt{\frac{1}{3}}\right)|VV\rangle = \frac{1}{3}|VV\rangle$$
#
# ---
#
# ### The Uncompiled Matrix
#
# When we assemble these raw output amplitudes into a matrix, we get:
# $$
# M_{\text{raw}} = \begin{pmatrix} 
# \frac{2}{3} & 0 & 0 & 0 \\ 
# 0 & \frac{\sqrt{2}}{3} & 0 & 0 \\ 
# 0 & 0 & -\frac{1}{3} & 0 \\ 
# 0 & 0 & 0 & \frac{1}{3} 
# \end{pmatrix}
# $$
#
# Because this matrix still lacks uniform diagonal amplitudes, the actual experiment by Okamoto et al. swaps the supplemental filters for simple **quarter-wave and half-wave plate combinations** ($QWP-HWP-QWP$). This forces a clean, uniform coincidence amplitude of exactly $1/3$ across all paths:
#
# $$
# M_{\text{coincidence}} = \frac{1}{3}\begin{pmatrix} 
# 1 & 0 & 0 & 0 \\ 
# 0 & 1 & 0 & 0 \\ 
# 0 & 0 & -1 & 0 \\ 
# 0 & 0 & 0 & 1 
# \end{pmatrix}
# $$
#
# This is a **Controlled-Phase (CZ) gate** with a success efficiency of $(1/3)^2 = 1/9$. 
#
# By framing the Target path with two **Hadamard rotations ($H$)** using $22.5^\circ$ HWPs, the negative phase shift on the $|10\rangle$ state transforms directly into the target-flipping **CNOT** permutation:
# $$\text{CNOT} = (I \otimes H) \cdot M_{\text{coincidence}} \cdot (I \otimes H)$$
#
# ## Ideal CNOT
#
# $$
# \text{CNOT} = \begin{pmatrix} 
# 1 & 0 & 0 & 0 \\ 
# 0 & 1 & 0 & 0 \\ 
# 0 & 0 & 0 & 1 \\ 
# 0 & 0 & 1 & 0 
# \end{pmatrix}
# $$
#

# %%
