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

plt.style.use('dark_background')
os.makedirs('data', exist_ok=True)

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

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 2: Bell State Entanglement ($|\Phi^+\rangle$)
#
# An entangled state cannot be factored into product states ($|\psi_{AB}\rangle \neq |\psi_A\rangle \otimes |\psi_B\rangle$).
#
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

# %%
