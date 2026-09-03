# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Module 05: Theoretical Speculations & Fundamental Spacetime Bounds
#
# **Objective:** Bridge core quantum information concepts to high-energy physics, spacetime thermodynamics, and cosmic-scale limits. This module explores how fundamental bounds—such as the Dyson power limit ($c^5/G$), Bekenstein entropy capacity, Penrose mechanisms, matter-antimatter asymmetries, and macroscopic phase tunneling—frame experimental tests for the $\mathcal{C}_{\text{max}}$ (State-Capacity) collapse hypothesis.

# %% [markdown]
# ## 5.1 Maximum Power (Dyson-Glover-Luminosity Limit)
#
# In general relativity and quantum field theory, there exists a fundamental upper limit to power (energy flow per unit time) independent of the force mechanism:
#
# $$P_{\text{max}} = \frac{c^5}{G} \approx 3.63 \times 10^{52} \text{ Watts}$$
#
# * **Physical Insight:** This "Dyson Limit" occurs when local energy flux creates an event horizon, preventing faster energy transfer.
# * **Black Hole Mergers:** Coalescing binary black holes briefly radiate near this exact maximum power limit in gravitational waves.

# %%
import numpy as np

# Physical constants (SI units)
C = 299792458.0             # Speed of light (m/s)
G = 6.67430e-11             # Gravitational constant (m^3 kg^-1 s^-2)
HBAR = 1.054571817e-34      # Reduced Planck constant (J s)
KB = 1.380649e-23           # Boltzmann constant (J/K)
L_P = np.sqrt(HBAR * G / C**3) # Planck length (m)

def dyson_maximum_power():
    """Calculates the Dyson maximum power limit c^5 / G in Watts."""
    return C**5 / G

p_max = dyson_maximum_power()
print(f"Dyson Maximum Power Limit (c^5/G): {p_max:.4e} Watts")

# %% [markdown]
# ## 5.2 Maximum Energy Density & Bekenstein Capacity Bound
#
# The maximum information $I$ (or entropy $S$) that can be contained within a bounded region of radius $R$ and total energy $E$ is bounded by the Bekenstein criterion:
#
# $$I \le \frac{2\pi E R}{\hbar c \ln 2}$$
#
# Saturating this bound yields a Schwarzschild black hole, linking maximum information storage directly to gravitational collapse and the $\mathcal{C}_{\text{max}}$ hypothesis:
#
# $$S_{\text{BH}} = \frac{A}{4 l_P^2}$$

# %% [markdown]
# ## 5.3 The Penrose Process & Superradiance
#
# Energy can be extracted from a rotating (Kerr) black hole's ergosphere:
# 1. A particle with energy $E_0$ enters the ergosphere and splits into two fragments ($E_1, E_2$).
# 2. Fragment 1 falls into the event horizon with **negative energy** relative to an observer at infinity ($E_1 < 0$).
# 3. Fragment 2 escapes to infinity carrying energy $E_2 = E_0 - E_1 > E_0$.

# %% [markdown]
# ## 5.4 Linking Cosmic Bounds to Experimental $\mathcal{C}_{\text{max}}$ Tests
#
# Under linear quantum mechanics, Hilbert space dimension scales exponentially as $\mathcal{D} = 2^N$ for $N$ entangled entities. The $\mathcal{C}_{\text{max}}$ hypothesis asserts that **local state capacity is bounded by spacetime geometry**. When subsystem von Neumann entropy $S(\rho_{\text{sub}})$ breaches $\mathcal{C}_{\text{max}}$, a non-linear term in `src/collapse_model.py` ($F_{\text{suppression}} = e^{-\max(0, S - \mathcal{C}_{\text{max}})}$) triggers non-unitary branch suppression.

# %% [markdown]
# ## 5.5 High-Energy Antimatter Tests & Cosmological Limits
#
# Beyond terrestrial QPUs, fundamental spacetime capacity limits can be probed using matter-antimatter systems and astrophysical observations:
#
# 1. **Positronium ($e^+e^-$) Gamma-Ray Polarimetry:** Annihilation produces entangled $511\text{ keV}$ photon pairs $|\Psi\rangle = \frac{1}{\sqrt{2}}(|H\rangle|V\rangle - |V\rangle|H\rangle)$. Polarization correlations over long baselines test high-energy continuous state capacity.
# 2. **Antihydrogen ($\bar{\text{H}}$) Interferometry:** Comparing decoherence rates between hydrogen ($H$) and antihydrogen ($\bar{\text{H}}$) in Earth's gravitational field probes CPT equivalence in spatial superpositions.
# 3. **Cosmological GRB / Blazar Polarimetry:** Transverse phase polarization of $100\text{ GeV}$ photons from distant sources ($z > 1$) sets empirical bounds on continuous Hilbert space capacity ($d_{\text{crit}} = 2^{\mathcal{C}_{\text{max}}}$) across megaparsec baselines.

# %%
def predict_cosmic_phase_diffusion(energy_gev: float, distance_gpc: float) -> float:
    """
    Estimates Planck-scale phase uncertainty cumulative over cosmological baselines.
    """
    energy_joules = energy_gev * 1e9 * 1.60218e-19
    planck_energy_joules = np.sqrt(HBAR * C**5 / G)
    distance_meters = distance_gpc * 3.085677581e25
    
    delta_phi = (energy_joules / planck_energy_joules) * (distance_meters / L_P)
    return delta_phi

phi_uncertainty = predict_cosmic_phase_diffusion(energy_gev=100.0, distance_gpc=1.0)
print(f"Phase uncertainty for 100 GeV photon over 1 Gpc: {phi_uncertainty:.4e} rad")

# %% [markdown]
# ## 5.6 Practical Test Protocol: Macroscopic Josephson Junction Phase Tunneling
#
# Macroscopic Quantum Tunneling (MQT) in current-biased Josephson junctions involves trillions of Cooper pairs acting as a single collective variable—the phase difference $\phi$ moving in a tilted-washboard potential:
#
# $$U(\phi) = -E_J \cos\phi - E_J \left(\frac{I}{I_c}\right)\phi$$
#
# As $\phi$ tunnels from the trapped state into a running voltage state, spatial/phase entanglement with the bias line creates a subsystem entropy $S(\rho_\phi)$. Crossing $\mathcal{C}_{\text{max}}$ suppresses the effective tunneling rate below the standard WKB plateau.

# %%
def simulate_josephson_cmax_plateau(i_bias_ratio=0.98, ej_ec_ratio=80.0, c_max_bound=0.4):
    """
    Computes WKB MQT phase tunneling rate and evaluates C_max non-linear suppression.
    """
    barrier_factor = (1.0 - i_bias_ratio)**(1.25)
    t_wkb = np.exp(-12.0 * np.sqrt(ej_ec_ratio) * barrier_factor)
    
    if 0.0 < t_wkb < 1.0:
        s_phase = -(t_wkb * np.log2(t_wkb) + (1.0 - t_wkb) * np.log2(1.0 - t_wkb))
    else:
        s_phase = 0.0
        
    delta_s = max(0.0, s_phase - c_max_bound)
    suppression = np.exp(-delta_s)
    
    return {
        "t_wkb": t_wkb,
        "entropy_bits": s_phase,
        "c_max_suppressed_rate": t_wkb * suppression
    }

mqt_res = simulate_josephson_cmax_plateau(i_bias_ratio=0.98, ej_ec_ratio=80.0, c_max_bound=0.4)
print(f"Josephson MQT Raw WKB Rate:         {mqt_res['t_wkb']:.6f}")
print(f"Phase Subsystem Entropy:            {mqt_res['entropy_bits']:.6f} bits")
print(f"C_max Suppressed Tunneling Rate:    {mqt_res['c_max_suppressed_rate']:.6f}")

# %% [markdown]
# ## 5.7 Discriminating Non-Linear Dynamics: Gross-Pitaevskii Mean-Field vs. $\mathcal{C}_{\text{max}}$ Collapse
#
# A critical task in experimental design is distinguishing true non-unitary wavefunction collapse ($\mathcal{C}_{\text{max}}$) from emergent non-linearities governed by standard linear quantum mechanics, such as Gross-Pitaevskii (GP) interaction terms ($g|\psi|^2\psi$) in Bose-Einstein Condensates.
#
# | Feature | Gross-Pitaevskii (GP) Mean-Field | $\mathcal{C}_{\text{max}}$ State-Capacity Collapse |
# | :--- | :--- | :--- |
# | **Physical Origin** | Inter-particle $s$-wave scattering ($g = \frac{4\pi\hbar^2 a_s}{m}$) | Local entanglement entropy saturation ($S(\rho_{\text{sub}}) \to \mathcal{C}_{\text{max}}$) |
# | **Governing Equation** | $i\hbar \frac{\partial \psi}{\partial t} = \left(-\frac{\hbar^2}{2m}\nabla^2 + V_{\text{ext}} + g|\psi|^2\right)\psi$ | $i\hbar \frac{\partial |\psi\rangle}{\partial t} = \hat{H}|\psi\rangle - i\hbar \gamma \max(0, S - \mathcal{C}_{\text{max}})|\psi\rangle$ |
# | **Unitarity** | **Unitary** (Conserves particle number $\int |\psi|^2 d^3r = N$) | **Non-Unitary** (Prunes non-viable state branches) |
# | **Scaling Variable** | Spatial particle density $n(\mathbf{r}) = |\psi(\mathbf{r})|^2$ | Reduced subsystem von Neumann entropy $S(\rho_A)$ |
# | **Reversibility** | Reversible via potential inversions ($U^\dagger$) | Irreversible loss of uncomputation fidelity |

# %%
def compare_gp_vs_cmax_decay(
    t_steps: np.ndarray, 
    g_interaction: float = 0.5, 
    c_max_bound: float = 0.8, 
    subsystem_entropy: float = 1.2
) -> dict:
    """
    Simulates contrasting decay profiles between Gross-Pitaevskii (GP) mean-field 
    density shifts and C_max state-capacity non-linear branch suppression.
    """
    linear_amplitude = np.exp(-0.1 * t_steps)
    
    # GP conservative phase/density modulation
    gp_density = linear_amplitude**2
    gp_amplitude = linear_amplitude * np.cos(g_interaction * gp_density * t_steps)
    
    # C_max non-unitary branch suppression
    delta_s = max(0.0, subsystem_entropy - c_max_bound)
    cmax_suppression_factor = np.exp(-delta_s * t_steps)
    cmax_amplitude = linear_amplitude * cmax_suppression_factor
    
    return {
        "time": t_steps,
        "linear": linear_amplitude,
        "gp_mean_field": gp_amplitude,
        "cmax_suppressed": cmax_amplitude
    }

t_grid = np.linspace(0, 5, 50)
decay_res = compare_gp_vs_cmax_decay(t_steps=t_grid, g_interaction=0.8, c_max_bound=0.5, subsystem_entropy=1.0)

print(f"Amplitude Comparison at t = 5.0s:")
print(f"  -> Linear Baseline:       {decay_res['linear'][-1]:.4f}")
print(f"  -> GP Mean-Field (g=0.8): {decay_res['gp_mean_field'][-1]:.4f}")
print(f"  -> C_max Collapse (S=1.0): {decay_res['cmax_suppressed'][-1]:.4f}")

# %% [markdown]
# ## 5.8 Summary of Experimental Platforms
#
# | Platform | Primary Variable Probed | Signal of $\mathcal{C}_{\text{max}}$ |
# | :--- | :--- | :--- |
# | **QPU / Cavity QED** | Subsystem Entropy $S(\rho_A)$ | $U^\dagger$ uncomputation fidelity drop |
# | **Positronium ($e^+e^-$)** | High-energy polarization entanglement | Polarization correlation visibility cutoff |
# | **Antihydrogen ($\bar{\text{H}}$)** | CPT Gravitational Equivalence | Asymmetric spatial superposition collapse rates |
# | **Josephson Junction MQT** | Phase difference $\phi$ branching | Non-linear suppression of WKB tunneling plateau |
# | **Feshbach-Tuned BEC** | Entanglement $S$ vs Scattering length $g \to 0$ | Damping that persists when $g = 0$ |