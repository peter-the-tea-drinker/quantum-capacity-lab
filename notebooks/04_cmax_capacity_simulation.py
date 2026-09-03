# %% [markdown] slideshow={"slide_type": "slide"}
# # Module 04: Non-Linear State-Capacity ($\mathcal{C}_{\text{max}}$) Simulation
# ### Conserved Many-Worlds & State-Capacity Exploration ($\mathcal{C}_{\text{max}}$)
#
# **Roadmap:**
# 1. Importing the Custom `ConservedCapacityModel` Engine
# 2. Simulating Subsystem Entropy vs $\mathcal{C}_{\text{max}}$ Threshold Bounds
# 3. Non-Linear Branch Damping & State Suppression Dynamics
# 4. Manipulation & Control Checks (Phase Steering vs Uncomputation)

# %% slideshow={"slide_type": "skip"}
import os
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

# Ensure local src module is accessible
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from src.collapse_model import ConservedCapacityModel

plt.style.use('dark_background')
os.makedirs('data', exist_ok=True)

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 1: Instantiating the Capacity Model Engine
#
# The `ConservedCapacityModel` tracks bipartite entanglement, computes subsystem von Neumann entropy $S(\rho_A)$, and evaluates the state capacity threshold $\mathcal{C}_{\text{max}}$.
#
# Below, we instantiate a model with a conservative capacity bound of $\mathcal{C}_{\text{max}} = 0.75\text{ bits}$.

# %% slideshow={"slide_type": "fragment"}
# Initialize simulation model with C_max = 0.75 bits
c_max_bound = 0.75
model = ConservedCapacityModel(num_qubits=2, c_max=c_max_bound)

# Test evaluation at half-entanglement angle theta = pi / 3
model.build_entangled_state(theta=np.pi / 3)
current_s = model.calculate_subsystem_entropy()
eval_res = model.evaluate_collapse_threshold(current_s)

print(f"Subsystem Entropy S(rho_A): {current_s:.4f} bits")
print(f"Capacity Limit (C_max):     {eval_res['c_max']:.4f} bits")
print(f"Utilization:               {eval_res['utilization_pct']:.1f}%")
print(f"Collapsed Status:          {eval_res['is_collapsed']}")

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 2: Multi-Bound $\mathcal{C}_{\text{max}}$ Threshold Sweeps
#
# We run simulations across different capacity bounds ($\mathcal{C}_{\text{max}} \in [0.4, 0.7, 1.0]$ bits) to compare how state branching scales relative to linear quantum mechanics.
#
# Intermediate results are pickled to `data/cmax_sweep_multi.pkl` for immediate reproduction.

# %% slideshow={"slide_type": "subslide"}
cache_file = 'data/cmax_sweep_multi.pkl'

if os.path.exists(cache_file):
    print("Loading cached C_max multi-bound simulation from data/cmax_sweep_multi.pkl...")
    with open(cache_file, 'rb') as f:
        sweep_data = pickle.load(f)
    thetas = sweep_data['thetas']
    results_by_bound = sweep_data['results_by_bound']
else:
    print("Executing multi-bound C_max simulation parameter sweeps...")
    thetas = np.linspace(0, np.pi, 50)
    bounds = [0.4, 0.7, 1.0]
    results_by_bound = {}

    for b in bounds:
        m = ConservedCapacityModel(num_qubits=2, c_max=b)
        entropies = []
        suppressions = []
        
        for th in thetas:
            m.build_entangled_state(th)
            s = m.calculate_subsystem_entropy()
            res = m.evaluate_collapse_threshold(s)
            entropies.append(s)
            suppressions.append(res['suppression_factor'])
            
        results_by_bound[b] = {
            'entropies': entropies,
            'suppressions': suppressions
        }

    with open(cache_file, 'wb') as f:
        pickle.dump({'thetas': thetas, 'results_by_bound': results_by_bound}, f)

# Plot Entropy vs Capacity Bounds
fig, ax = plt.subplots(figsize=(8, 4))
for b, data in results_by_bound.items():
    ax.plot(thetas, data['entropies'], label=f'Entropy (C_max={b})', linewidth=2)
    ax.axhline(b, linestyle=':', alpha=0.6, label=f'Bound C_max={b}')

ax.set_xlabel('Entanglement Angle $\\theta$ (rad)')
ax.set_ylabel('Subsystem Entropy $S(\\rho_A)$ (bits)')
ax.set_title('Subsystem Entropy Scaling vs $\\mathcal{C}_{\\text{max}}$ Thresholds')
ax.grid(True, alpha=0.3)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 3: Non-Linear Branch Damping
#
# When $S(\rho_A) \ge \mathcal{C}_{\text{max}}$, the state capacity hypothesis introduces an exponential branch suppression factor:
#
# $$F_{\text{suppression}} = \exp\left(-\max\left(0, S(\rho_A) - \mathcal{C}_{\text{max}}\right)\right)$$
#
# This factor damps non-linear branch multiplicity without violating local trace conservation.

# %% slideshow={"slide_type": "subslide"}
fig, ax = plt.subplots(figsize=(8, 4))

colors = ['#FF007F', '#00D2FF', '#00FF66']
for (b, data), col in zip(results_by_bound.items(), colors):
    ax.plot(thetas, data['suppressions'], color=col, linewidth=2, label=f'Suppression (C_max={b})')

ax.set_xlabel('Entanglement Angle $\\theta$ (rad)')
ax.set_ylabel('Branch Suppression Factor')
ax.set_title('Non-Linear Branch Damping Dynamics')
ax.grid(True, alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()

# %% [markdown] slideshow={"slide_type": "slide"}
# ## Section 4: Manipulation & Control Checks
#
# We evaluate whether external local phase control ($R_z(\phi)$) can alter entanglement entropy or bypass the $\mathcal{C}_{\text{max}}$ threshold, versus global coherent uncomputation ($U^\dagger$).

# %% slideshow={"slide_type": "subslide"}
# Execute Phase Steering Check
phase_res = model.check_phase_control_manipulation(phase_shift=np.pi / 4, theta=np.pi / 2)
# Execute Uncomputation Recovery Check
uncomp_res = model.check_uncomputation_recovery(theta=np.pi / 2)

print("=== MANIPULATION & CONTROL CHECK RESULTS ===")
print(f"1. Phase Control Test: Invariant = {phase_res['entropy_invariant']}")
print(f"   Initial Entropy:  {phase_res['s_initial']:.4f} bits")
print(f"   Post Phase Shift: {phase_res['s_post_manipulation']:.4f} bits")
print(f"   Controllable via Local Phase: {phase_res['controllable_via_local_phase']}")

print("\n2. Uncomputation Test: Reversible = {uncomp_res['reversible']}")
print(f"   Recovered Entropy: {uncomp_res['s_recovered']:.6f} bits")
print(f"   Full Reversibility Restored: {uncomp_res['is_fully_recovered']}")

# %% [markdown]
# ## 3.5 Practical Test Protocol: Macroscopic Josephson Junction Phase Tunneling
#
# Macroscopic Quantum Tunneling (MQT) in Josephson junctions provides a highly controllable platform to benchmark continuous state capacity ($\mathcal{C}_{\text{max}}$) against standard thermal relaxation ($T_1$) and phase decoherence ($T_2$).
#
# ---
#
# ### 1. Physical System & Tunneling Mechanics
# A current-biased Josephson junction behaves as a particle of "mass" $C$ moving in a tilt-washboard potential:
#
# $$U(\phi) = -E_J \cos\phi - E_J \left(\frac{I}{I_c}\right)\phi$$
#
# * **Phase Superposition:** Near the critical current $I \approx I_c$, the phase variable $\phi$ can tunnel out of a local potential well into a running state.
# * **Entropy Generation:** As the state splits between trapped $\vert{}\phi_{\text{trapped}}\rangle$ and tunneled $\vert{}\phi_{\text{running}}\rangle$, spatial entanglement with the bias line creates a subsystem entropy $S(\rho_{\phi})$.
# * **$\mathcal{C}_{\text{max}}$ Onset:** If the tunneling probability $\mathcal{T}_{\text{MQT}}$ produces an entropy $S(\rho_{\phi}) > \mathcal{C}_{\text{max}}$, the state capacity threshold is breached, accelerating decay beyond standard environmental thermalization $\Gamma_{\text{thermal}}$.
#
# ---
#
# ### 2. Practical Student Exercise: Modeling Josephson MQT under $\mathcal{C}_{\text{max}}$
#
# #### Problem Statement
# 1. Compute the WKB escape rate $\Gamma_{\text{MQT}}$ for a junction with Josephson energy $E_J$ and charging energy $E_C$.
# 2. Calculate the resulting spatial phase entropy $S(\rho) = - \mathcal{T} \log_2 \mathcal{T} - (1 - \mathcal{T}) \log_2 (1 - \mathcal{T})$.
# 3. Predict the effective escape fidelity under non-linear state capacity suppression in `src/collapse_model.py`.
#
# #### Python Implementation Code
# ```python
# import numpy as np
#
# def evaluate_josephson_mqt_cmax(i_bias_ratio=0.98, ej_ec_ratio=50.0, c_max_bound=0.5):
#     """
#     Evaluates Macroscopic Quantum Tunneling (MQT) phase escape rate 
#     and applies C_max non-linear branch suppression.
#     """
#     # 1. WKB tunneling transmission probability approximation
#     barrier_factor = (1.0 - i_bias_ratio)**(1.25)
#     t_mqt = np.exp(-12.0 * np.sqrt(ej_ec_ratio) * barrier_factor)
#     
#     # 2. Subsystem entropy of trapped vs tunneled phase branches
#     if t_mqt <= 0.0 or t_mqt >= 1.0:
#         entropy = 0.0
#     else:
#         entropy = -(t_mqt * np.log2(t_mqt) + (1.0 - t_mqt) * np.log2(1.0 - t_mqt))
#         
#     # 3. Apply C_max state capacity suppression
#     delta_s = max(0.0, entropy - c_max_bound)
#     f_suppression = np.exp(-delta_s)
#     effective_t = t_mqt * f_suppression
#     
#     return {
#         "raw_t_mqt": t_mqt,
#         "phase_entropy": entropy,
#         "c_max_suppression": f_suppression,
#         "effective_tunneling_rate": effective_t
#     }
#
# # Execute simulation for a standard Transmon/Josephson junction
# results = evaluate_josephson_mqt_cmax(i_bias_ratio=0.98, ej_ec_ratio=50.0, c_max_bound=0.3)
# print(f"Raw Tunneling Prob (T): {results['raw_t_mqt']:.6f}")
# print(f"Phase Subsystem Entropy: {results['phase_entropy']:.6f} bits")
# print(f"C_max Suppressed Rate:   {results['effective_tunneling_rate']:.6f}")

# %%
