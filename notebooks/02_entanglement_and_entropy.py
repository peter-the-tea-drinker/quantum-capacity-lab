# %% [markdown] slideshow={"slide_type": "slide"}
# # Module 02: Entanglement, Density Matrices & von Neumann Entropy
# ### Conserved Many-Worlds & State-Capacity Exploration ($\mathcal{C}_{\text{max}}$)
#
# **Roadmap:**
# 1. Multi-Qubit Hilbert Spaces & Tensor Products ($\otimes$)
# 2. Bell State Creation ($|\Phi^+\rangle$) & Non-Locality
# 3. Density Matrices ($\rho$) & Partial Trace Operations
# 4. Quantifying Subsystem Entanglement via von Neumann Entropy ($S(\rho)$)

# %% slideshow={"slide_type": "skip"}
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace, entropy
from utils import show_img

plt.style.use('dark_background')
os.makedirs('data', exist_ok=True)

# %% [markdown]
# ## Section 1: Spontaneous Parametric Downconversion
#

# %%
show_img('images/Spontaneous_Parametric_Downconversion.png','By <a href="https://en.wikipedia.org/wiki/User:J_S_Lundeen" class="extiw" title="wikipedia:User:J S Lundeen">J S Lundeen</a> at <a href="https://en.wikipedia.org/wiki/" class="extiw" title="wikipedia:">English Wikipedia</a> - <span class="int-own-work" lang="">Own work by the original uploader</span>, <a href="http://creativecommons.org/licenses/by-sa/3.0/" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=36352608">Link</a>')

# %% [markdown]
#
# Nonlinear crystals (such as bbo) can create pairs of photons that share a wave function - they are entangled.
#
# A UV laser will sometimes interact with the crystal, become absorbed, and two entangled low energy photons emerge (conserving momentum).
#
# Assuming one of these entangled photons takes "Path A" (towards one of your detectors) then the second one must take "Path B", but this is not known until one of them is detected.
#
# The photons can also have polarisation, which gives us 2 qubits:
#
# **Qubit 1: Path Space**
# * Path A: $\vert A \rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$
# * Path B: $\vert B \rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$
#
# **Qubit 2: Polarization Space**
# * Horizontal: $\vert H \rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix}$
# * Vertical: $\vert V \rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix}$
#
#
# A 2-qubit system exists in a 4-dimensional Hilbert space $\mathcal{H}_{total} = \mathcal{H}_{path} \otimes \mathcal{H}_{polarisation}$.
#
# The basis vectors are constructed via the Kronecker product:
#
# $$|00\rangle = |0\rangle \otimes |0\rangle = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}, \quad |01\rangle = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}, \quad |10\rangle = \begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix}, \quad |11\rangle = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}$$
#
#
# We could choose to ensure that path A is Horizontal and path B is Vertical:
#
#
# $$\vert A, H \rangle = \begin{pmatrix} 1 \\ 0 \end{pmatrix} \otimes \begin{pmatrix} 1 \\ 0 \end{pmatrix} = \begin{pmatrix} 1 \cdot 1 \\ 1 \cdot 0 \\ 0 \cdot 1 \\ 0 \cdot 0 \end{pmatrix} = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}$$
#
# $$\vert B, V \rangle = \begin{pmatrix} 0 \\ 1 \end{pmatrix} \otimes \begin{pmatrix} 0 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \cdot 0 \\ 0 \cdot 1 \\ 1 \cdot 0 \\ 1 \cdot 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}$$
#
#
#

# %%

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 1: Multi-Qubit Hilbert Spaces & Tensor Products
#
# A 2-qubit system exists in a 4-dimensional Hilbert space $\mathcal{H}_A \otimes \mathcal{H}_B$.
#
# The basis vectors are constructed via the Kronecker product:
#
# $$|00\rangle = |0\rangle \otimes |0\rangle = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}, \quad |01\rangle = \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix}, \quad |10\rangle = \begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix}, \quad |11\rangle = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix}$$

# %% slideshow={"slide_type": "subslide"}
# Explicit Tensor Product Construction
ket_0 = np.array([1, 0], dtype=complex)
ket_1 = np.array([0, 1], dtype=complex)

ket_00 = np.kron(ket_0, ket_0)
ket_11 = np.kron(ket_1, ket_1)

print("Composite state |00⟩ vector:")
print(ket_00)

# %% [markdown]
# ## Section 2: Bell State Entanglement ($|\Phi^+\rangle$)
#
#

# %% [markdown] slideshow={"slide_type": "slide"}
#
# #### **Step A: The "Which-Way" Marked State (Bell State)**
# A waveplate rotates A so it marks Path A as Vertical ($\vert V \rangle$) and leaves Path B as Horizontal ($\vert H \rangle$):
# $$\vert\psi\rangle = \frac{1}{\sqrt{2}} \big( \vert A\rangle\vert V\rangle + \vert B\rangle\vert H\rangle \big) = \frac{1}{\sqrt{2}} \left[ \begin{pmatrix} 0 \\ 1 \\ 0 \\ 0 \end{pmatrix} + \begin{pmatrix} 0 \\ 0 \\ 1 \\ 0 \end{pmatrix} \right] = \frac{1}{\sqrt{2}} \begin{pmatrix} 0 \\ 1 \\ 1 \\ 0 \end{pmatrix}$$
#
# The Bell State is an important first step in most experiments - both particles are "equal and opposite" as much as possible, but as entangled as possible.
#
#
#
#
#
# An entangled state cannot be factored into product states ($|\psi_{AB}\rangle \neq |\psi_A\rangle \otimes |\psi_B\rangle$).
#
#
#

# %% [markdown]
# ## Mathematical Framework of the Marked Bell State
#
# Let the spatial states of a photon passing through the double slit system be defined by the orthogonal basis:
# * $|1\rangle$: The photon traveling through **Slit 1**.
# * $|2\rangle$: The photon traveling through **Slit 2**.
#
# When quarter-wave plates or polarization rotators are placed at the slits, they imprint "which-way" labels on the photon. Slit 1 marks the path with a Vertical polarization state $|V\rangle$, while Slit 2 marks the path with an orthogonal Horizontal polarization state $|H\rangle$. 
#
# This creates an entangled path-polarization state (a **Bell state**):
#
# $$|\psi\rangle = \frac{1}{\sqrt{2}} \big(|1\rangle|V\rangle + |2\rangle|H\rangle\big)$$
#
# ### 1. Propagation to the Screen
# As the spatial components of the state evolve over a distance to a position $x$ on a distant detector screen, the path basis elements project onto standard spatial wavefunctions:
# $$\langle x|1\rangle = \psi_1(x)$$
# $$\langle x|2\rangle = \psi_2(x)$$
#
# Substituting these projections into our state vector gives the total quantum state at position $x$:
# $$|\psi(x)\rangle = \frac{1}{\sqrt{2}} \big(\psi_1(x)|V\rangle + \psi_2(x)|H\rangle\big)$$
#
# ### 2. Computing the Intensity Profile (No Eraser)
# To evaluate the observed physical light intensity $I(x)$ on the screen, we compute the quantum mechanical probability density by taking the inner product of the state with itself, $\langle\psi(x)|\psi(x)\rangle$:
#
# $$I(x) = \frac{1}{2} \Big( \psi_1^*(x)\langle V| + \psi_2^*(x)\langle H| \Big) \Big( \psi_1(x)|V\rangle + \psi_2(x)|H\rangle \Big)$$
#
# Expanding this product out yields four distinct terms:
# $$I(x) = \frac{1}{2}|\psi_1(x)|^2 \langle V|V\rangle + \frac{1}{2}|\psi_2(x)|^2 \langle H|H\rangle + \frac{1}{2}\psi_1^*(x)\psi_2(x)\langle V|H\rangle + \frac{1}{2}\psi_2^*(x)\psi_1(x)\langle H|V\rangle$$
#
# ### 3. The Vanishing Cross-Terms
# Because Vertical and Horizontal polarization states are perfectly orthogonal to one another, their mathematical overlaps evaluate exactly to zero:
# $$\langle V|H\rangle = \langle H|V\rangle = 0$$
# $$\langle V|V\rangle = \langle H|H\rangle = 1$$
#
# Substituting these values back into the expanded equation directly eliminates the phase-dependent interference terms:
#
# $$I(x) = \frac{1}{2}|\psi_1(x)|^2 + \frac{1}{2}|\psi_2(x)|^2$$
#
# **Conclusion:** Because the cross-terms are completely canceled out by the orthogonal path markers, no constructive or destructive interference fringes can form. The screen registers a purely classical, smooth sum of individual slit intensities.
#

# %%
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Parameter Setup
# ---------------------------------------------------------
x = np.linspace(-10, 10, 1000)  # Screen position coordinate

# Single-slit diffraction envelope (sinc function modeling slit width)
# This represents the spatial wavefunctions \psi_1(x) and \psi_2(x)
envelope = np.sinc(x / 4.0) ** 2

# Interference term (cosine function modeling slit separation)
# This arises from the cross-terms \psi_1*(x)\psi_2(x) when tags are erased
interference_factor = 1 + np.cos(2 * np.pi * x / 2.0)

# ---------------------------------------------------------
# 2. Calculating Intensities
# ---------------------------------------------------------
# Marked State / No Eraser: I(x) = 0.5*|\psi_1|^2 + 0.5*|\psi_2|^2
# Cross-terms vanish completely due to orthogonal polarization states
no_interference = envelope 

# Erased State / Diagonal Polarizer: Fringes are restored
erased_interference = envelope * (interference_factor / 2.0)

# ---------------------------------------------------------
# 3. Plotting the Results
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# Plot the smooth pattern observed without the erasure
plt.plot(x, no_interference, 
         label=r'No Eraser: $I(x) = \frac{1}{2}|\psi_1|^2 + \frac{1}{2}|\psi_2|^2$', 
         color='crimson', linewidth=2.5)

# Plot the fringe pattern observed when the diagonal eraser is applied
plt.plot(x, erased_interference, 
         label=r'With Diagonal Eraser: Which-Way Info Destroyed', 
         color='dodgerblue', linestyle='--', alpha=0.8, linewidth=2.0)

# Formatting the plot
plt.title('Double-Slit Quantum Eraser Profile', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Screen Position ($x$)', fontsize=12)
plt.ylabel('Normalized Intensity $I(x)$', fontsize=12)
plt.legend(loc='upper right', fontsize=11, framealpha=0.9)
plt.grid(True, linestyle=':', alpha=0.6)

# Display the output directly in Jupyter
plt.show()


# %% [markdown]
# Applying a Hadamard gate followed by a CNOT gate yields the maximally entangled Bell state:
#
# $$|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$

# %% slideshow={"slide_type": "fragment"}
# Build Bell State Circuit in Qiskit
qc_bell = QuantumCircuit(2)
qc_bell.h(0)
qc_bell.cx(0, 1)

state = Statevector.from_instruction(qc_bell)
print("Bell State Vector |Φ+⟩:")
print(np.round(state.data, 3))

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 3: Density Matrices & Partial Trace
#
# For a bipartite state $\rho_{AB} = |\Phi^+\rangle\langle\Phi^+|$, tracing out Subsystem $B$ yields the **Reduced Density Matrix** $\rho_A$:
#
# $$\rho_A = \text{Tr}_B(\rho_{AB}) = \frac{1}{2}|0\rangle\langle 0| + \frac{1}{2}|1\rangle\langle 1| = \begin{pmatrix} 0.5 & 0 \\ 0 & 0.5 \end{pmatrix}$$
#
# Subsystem $A$ is in a **maximally mixed state**, proving total information loss to subsystem correlations.

# %% slideshow={"slide_type": "subslide"}
# Calculate Full and Reduced Density Matrices
rho_AB = Statevector(state).to_operator()
rho_A = partial_trace(state, [1])  # Trace out qubit 1

print("Full Density Matrix ρ_AB:")
print(np.round(rho_AB.data, 2))

print("\nReduced Density Matrix ρ_A (Qubit 0):")
print(np.round(rho_A.data, 2))

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 4: Entanglement Entropy Sweep ($S(\rho)$)
#
# The **von Neumann Entropy** quantifies state-branching entropy:
#
# $$S(\rho_A) = -\text{Tr}(\rho_A \log_2 \rho_A) = -\sum \lambda_i \log_2 \lambda_i$$
#
# - **Product State:** $S(\rho_A) = 0$ bits (no branching correlation)
# - **Bell State:** $S(\rho_A) = 1.0$ bit (maximal entanglement)
#
# We sweep a parameterized CNOT angle $\theta$ to observe continuous entropy scaling.

# %% slideshow={"slide_type": "subslide"}
cache_file = 'data/entropy_sweep_cache.pkl'

if os.path.exists(cache_file):
    print("Loading cached entropy data from data/entropy_sweep_cache.pkl...")
    with open(cache_file, 'rb') as f:
        cache_data = pickle.load(f)
    thetas, entropies = cache_data['thetas'], cache_data['entropies']
else:
    print("Simulating parameterized entanglement entropy sweep...")
    thetas = np.linspace(0, np.pi, 50)
    entropies = []
    
    for th in thetas:
        qc_param = QuantumCircuit(2)
        qc_param.h(0)
        qc_param.cry(th, 0, 1)  # Controlled-RY rotation
        
        sv = Statevector.from_instruction(qc_param)
        rho_sub = partial_trace(sv, [1])
        
        # Calculate von Neumann Entropy (base 2)
        S = entropy(rho_sub, base=2)
        entropies.append(S)
    
    with open(cache_file, 'wb') as f:
        pickle.dump({'thetas': thetas, 'entropies': entropies}, f)

# Plot Entanglement Entropy Scaling
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(thetas, entropies, 'o-', color='#FF007F', linewidth=2, label=r'von Neumann Entropy $S(\rho_A)$')
ax.set_xlabel('Entanglement Parameter $\\theta$ (rad)')
ax.set_ylabel('Entropy $S(\\rho_A)$ (bits)')
ax.set_title('Subsystem Entanglement Entropy Scaling')
ax.axhline(1.0, color='#00FF66', linestyle='--', label='Maximal Entanglement Bound (1 Bit)')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Exercise 3: Entanglement with a Continuous Field Mode
#
# Instead of a single discrete detector qubit, let the system qubit entangle with a continuous electromagnetic mode inside a resonant cavity (prepared in a coherent state $|\alpha\rangle$).
#
# The joint system-environment state after interaction is:
#
# $$|\Psi\rangle = \frac{1}{\sqrt{2}} \left( |0\rangle_S |\alpha\rangle_E + |1\rangle_S |-\alpha\rangle_E \right)$$
#
# 1. **Environmental Overlap:** Calculate the inner product $\langle -\alpha | \alpha \rangle$ between the two continuous coherent states.
# 2. **Visibility Bound:** Given that Ramsey fringe visibility is $V = |\langle -\alpha | \alpha \rangle|$, prove that:
#    $$V = e^{-2|\alpha|^2}$$
# 3. **Capacity Threshold:** How many average photons $\bar{n} = |\alpha|^2$ are required to suppress system coherence below $1\%$? What does this scaling limit imply about macro-system state capacity ($\mathcal{C}_{\text{max}}$)?

# %%
### A different version:

# %%
show_img('images/erasure1.png','By <a href="//commons.wikimedia.org/wiki/User:Patrick_Edwin_Moran" title="User:Patrick Edwin Moran">Patrick Edwin Moran</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="https://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=31186313">Link</a>')
show_img('images/erasure2.png','By <a href="//commons.wikimedia.org/wiki/User:Patrick_Edwin_Moran" title="User:Patrick Edwin Moran">Patrick Edwin Moran</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="https://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=31186314">Link</a>')

# %%
