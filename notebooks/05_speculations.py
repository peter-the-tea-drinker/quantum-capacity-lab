# %% [markdown]
# # # Module 05: Theoretical Speculations & Fundamental Physical Bounds
# #
# # ## 5.1 Maximum Power (Dyson-Glover-Luminosity Limit)
# # In general relativity and quantum field theory, there is a fundamental upper limit to power (energy flow per unit time) independent of the force mechanism:
# #
# # $$P_{\text{max}} = \frac{c^5}{G} \approx 3.63 \times 10^{52} \text{ Watts}$$
# #
# # * **Physical Insight:** This "Dyson Limit" occurs when energy flux creates a local event horizon, preventing faster energy transfer.
# # * **Black Hole Mergers:** Coalescing binary black holes briefly radiate near this exact maximum power limit in gravitational waves.
# #
# # ## 5.2 Maximum Energy Density & Bekenstein Bound
# # The maximum information $I$ (or entropy $S$) that can be contained within a region of radius $R$ and total energy $E$ is bounded by:
# #
# # $$I \le \frac{2\pi E R}{\hbar c \ln 2}$$
# #
# # Saturating this bound yields a Schwarzschild black hole, linking maximum information storage directly to gravitational collapse ($\mathcal{C}_{\text{max}}$).
# #
# # ## 5.3 The Penrose Process & Superradiance
# # Energy can be extracted from a rotating (Kerr) black hole's ergosphere:
# # 1. A particle with energy $E_0$ enters the ergosphere and splits into two fragments ($E_1, E_2$).
# # 2. Fragment 1 falls into the event horizon with **negative energy** relative to an observer at infinity ($E_1 < 0$).
# # 3. Fragment 2 escapes to infinity carrying energy $E_2 = E_0 - E_1 > E_0$.
# #
# # ### Student Exercise 5.1: Maximum Power & Black Hole Erasure
# # > 1. Derive $P_{\text{max}} = \frac{c^5}{G}$ using dimensional analysis from fundamental constants $c$ and $G$.
# # > 2. Relate Landauer's Principle ($E_{\text{erase}} \ge k_B T \ln 2$) at the Hawking temperature $T_H = \frac{\hbar c^3}{8\pi G M k_B}$ to show that erasing 1 bit of information at a black hole horizon requires a displacement on the order of the Planck length $l_P = \sqrt{\frac{\hbar G}{c^3}}$.
#
# # ## 5.4 Linking Cosmic Bounds to Experimental $\mathcal{C}_{\text{max}}$ Tests
# #
# # The $\mathcal{C}_{\text{max}}$ hypothesis proposes that non-linear state collapse is the low-energy manifestation of spacetime capacity saturation. Below are four proposed experimental protocols to test for capacity limits:
# #
# # ---
# #
# # ### Protocol 1: Large-Scale Superposition & Cavity QED ($\mathcal{C}_{\text{max}}$ Primary Test)
# # * **Mechanism:** Entangle a single superconducting qubit with a high-Q cavity prepared in a continuous coherent state $|\alpha\rangle$ (Module 03, Exercise 3).
# # * **$\mathcal{C}_{\text{max}}$ Signature:** As $|\alpha|^2 \to \mathcal{C}_{\text{max}}$, the state capacity saturates. Instead of standard exponential decay $V = e^{-2|\alpha|^2}$, the non-linear suppression factor forces an abrupt, discontinuous drop in Ramsey fringe visibility $V(\theta)$ *before* classical thermalization time $T_1/T_2$.
# #
# # ---
# #
# # ### Protocol 2: Optomechanical Mirror Delocalization (Penrose-Diósi vs $\mathcal{C}_{\text{max}}$)
# # * **Mechanism:** Prepare a macroscopic mechanical oscillator (e.g., a $10^{-14}\text{ kg}$ nanobeam or micro-mirror) in a spatial superposition $|\psi\rangle = \frac{1}{\sqrt{2}}(|x_1\rangle + |x_2\rangle)$.
# # * **Penrose Criterion:** Gravitational self-energy time $\tau \approx \frac{\hbar}{\Delta E_G}$.
# # * **$\mathcal{C}_{\text{max}}$ Difference:** While Penrose collapse depends strictly on gravitational mass distribution $\Delta E_G$, $\mathcal{C}_{\text{max}}$ depends on the **entanglement entropy** accumulated with the reflective optical field. Measuring collapse as a function of field entropy rather than mirror mass distinguishes $\mathcal{C}_{\text{max}}$ from Penrose collapse.
# #
# # ---
# #
# # ### Protocol 3: Coherent Uncomputation ($U^\dagger$) Saturation
# # * **Mechanism:** Using a gate-based QPU (IBM/Quantinuum), build a GHZ state across $N$ qubits: $|GHZ_N\rangle = \frac{1}{\sqrt{2}}(|0\rangle^{\otimes N} + |1\rangle^{\otimes N})$.
# # * **Test:** Apply full coherent uncomputation $U^\dagger$ to restore state $|0\rangle^{\otimes N}$.
# # * **$\mathcal{C}_{\text{max}}$ Signature:** Linear QM predicts $100\%$ fidelity (minus standard gate noise). Under $\mathcal{C}_{\text{max}}$, as subsystem entropy $S(\rho_A)$ reaches the capacity limit during intermediate steps, uncomputation fidelity drops non-linearly:
# #   $$\mathcal{F}_{U^\dagger}(N) \propto \exp\left(-\int (S(t) - \mathcal{C}_{\text{max}}) \, dt\right)$$
# #
# # ---
# #
# # ### Protocol 4: High-Dimensional Photonic Orbital Angular Momentum (OAM)
# # * **Mechanism:** Prepare single photons in high-dimensional qudit states ($d \gg 2$) using spatial light modulators (SLM).
# # * **Test:** Measure double-slit visibility as $d$ (dimension count) scales.
# # * **$\mathcal{C}_{\text{max}}$ Signature:** A sharp cutoff in quantum state visibility at a critical dimension $d_{\text{crit}} = 2^{\mathcal{C}_{\text{max}}}$, setting a strict limit on continuous-variable Hilbert space capacity.
#
# # ### Student Exercise 5.2: Designing a $\mathcal{C}_{\text{max}}$ Discrimination Test
# # > 1. Distinguish between **Environmental Decoherence** ($T_2$ noise), **Penrose Gravitational Collapse** ($\Delta E_G$), and **$\mathcal{C}_{\text{max}}$ Capacity Saturation** in a table comparing their scaling variables ($t$, mass $m$, or entropy $S$).
# # > 2. Using `src/collapse_model.py`, modify `evaluate_collapse_threshold()` to include a Penrose mass-dependent decay parameter $\Gamma_G = \Delta E_G / \hbar$ alongside $\mathcal{C}_{\text{max}}$.
# # > 3. Plot the predicted fringe visibility $V$ versus qubit number $N$ to show how a $\mathcal{C}_{\text{max}}$ cutoff differs visually from standard exponential noise decay.
#
# # ## 5.5 Antimatter Tests & Cosmic Observational Limits on $\mathcal{C}_{\text{max}}$
# #
# # Beyond terrestrial table-top circuits and cavity QED systems, fundamental spacetime capacity limits ($\mathcal{C}_{\text{max}}$) can be probed at extreme energy scales and across astrophysical distances.
# #
# # ---
# #
# # ### 1. Antimatter Interferometry & CPT Violation Tests
# # * **Mechanism:** Experiments at CERN (AEgIS, ALPHA-g, GBAR) perform precision interferometry on cold antihydrogen ($\bar{\text{H}}$) in Earth's gravitational field.
# # * **The Gravitational Connection:** If non-linear $\mathcal{C}_{\text{max}}$ collapse is linked to spacetime geometry or quantum gravity, the coupling strength could differ between matter and antimatter states, breaking CPT symmetry at extreme superposition bounds.
# # * **Observational Metric:** Measuring the decoherence rate $\Gamma_{\bar{\text{H}}}$ of antihydrogen spatial superpositions against matter hydrogen ($\Gamma_{\text{H}}$):
# #   $$\Delta \Gamma = |\Gamma_{\bar{\text{H}}} - \Gamma_{\text{H}}|$$
# #   A non-zero $\Delta \Gamma$ beyond standard environmental gas-scattering backgrounds would signal a fundamental asymmetry in how curvature bounds state capacity for antimatter.
# #
# # ---
# #
# # ### 2. Cosmic Wavefunction Coherence (Cosmological Gamma-Ray Bursts & Blazars)
# # * **Mechanism:** Photons emitted by distant astronomical sources (e.g., Gamma-Ray Bursts at redshift $z > 1$) travel billions of light-years while entangled across continuous spatial degrees of freedom.
# # * **Vacuum Spacetime Foam & $\mathcal{C}_{\text{max}}$:** As multi-photon or high-OAM wavepackets propagate across cosmological distances, interaction with Planck-scale spacetime fluctuations induces continuous phase diffusion.
# # * **Upper Bound Test:** If $\mathcal{C}_{\text{max}}$ imposes a hard limit on continuous Hilbert space dimensions ($d_{\text{crit}} = 2^{\mathcal{C}_{\text{max}}}$), high-energy cosmic photons ($E > 100 \text{ GeV}$) should exhibit a sharp loss of polarization entanglement over cosmological baselines.
# # * **Observational Limit:** Polarimetric data from space observatories (e.g., IXPE, Fermi LAT) set a strong empirical lower bound on the maximum capacity scale $\mathcal{C}_{\text{max}}$.
# #
# # ---
# #
# # ### 3. Black Hole Information Paradox & Horizon Saturated States
# # * **Mechanism:** Near the event horizon of a Kerr black hole, Hawking radiation pairs are entangled across the horizon boundary.
# # * **Capacity Saturation:** As the black hole evaporates, the internal entanglement entropy approaches the Bekenstein-Hawking bound $S_{\text{BH}} = \frac{A}{4 l_P^2}$.
# # * **$\mathcal{C}_{\text{max}}$ Resolution:** Rather than forming an unphysical "firewall" or violating unitarity, the $\mathcal{C}_{\text{max}}$ non-linear suppression term kicks in precisely when $S(\rho_{\text{int}}) \to \mathcal{C}_{\text{max}}$. This forces deterministic branch pruning, releasing information back into external Hawking radiation along the Page curve without requiring trans-Planckian energy densities.
# #
# # ---
# #
# # ### Student Exercise 5.3: Cosmic Entanglement Bounds
# # > 1. Given a gamma-ray photon ($E = 100 \text{ GeV}$) traveling over a redshift distance $d = 1 \text{ Gpc}$, calculate the Planck-scale phase uncertainty $\Delta \phi \approx \frac{E}{E_P} \frac{d}{l_P}$ (where $E_P \approx 1.22 \times 10^{19} \text{ GeV}$).
# # > 2. Use this value to estimate the maximum number of entangled photon modes $N_{\text{max}}$ that can remain coherent across cosmological distances before $\mathcal{C}_{\text{max}}$ capacity is saturated.
#
# # ## Protocol 5.1: High-Energy Positronium ($e^+ e^-$) Gamma-Ray Entanglement Test
# #
# # This protocol outlines an experimental test of the $\mathcal{C}_{\text{max}}$ (State-Capacity) hypothesis using maximally entangled $511\text{ keV}$ photon pairs produced via parapositronium ($p\text{-Ps}$) annihilation.
# #
# # ---
# #
# # ### 1. Theoretical Motivation & Mechanics
# # When parapositronium in the ground singlet state ($^1S_0$) annihilates, it decays into two $511\text{ keV}$ gamma photons emitted in back-to-back opposite directions to conserve linear momentum. 
# #
# # Deduction from conservation of angular momentum and parity requires the linear polarization vectors of the two gamma photons to be mutually orthogonal:
# #
# # $$\vert{}\Psi_{\gamma\gamma}\rangle = \frac{1}{\sqrt{2}} \Big( \vert{}H\rangle_1 \vert{}V\rangle_2 - \vert{}V\rangle_1 \vert{}H\rangle_2 \Big)$$
# #
# # * **High Energy Density:** The relativistic energy-to-mass conversion yields a high-momentum entanglement pair where thermal environmental decoherence is negligible.
# # * **$\mathcal{C}_{\text{max}}$ Signal:** Under linear QM, polarization correlations follow standard Klein-Nishina cross-section dynamics. If $\mathcal{C}_{\text{max}}$ imposes a hard continuous-capacity limit at high energy scales, gamma-ray polarization entanglement will exhibit non-linear fringe suppression over extended spatial baselines $L$.
# #
# # ---
# #
# # ### 2. Experimental Setup & Pipeline
# #
# # 1. **Positron Source & Target:**
# #    * A $a\text{-}\text{Na}^{22}$ radioactive source emits positrons ($e^+$) into a porous silica target.
# #    * Positrons thermalize and capture electrons ($e^-$) to form $p\text{-Ps}$ with a mean lifetime of $\tau \approx 125\text{ ps}$.
# # 2. **Coincidence Detection & Collimation:**
# #    * Opposing lead collimators select back-to-back gamma pairs along a precise baseline path ($L$).
# # 3. **Polarimetry via Compton Scattering:**
# #    * Gamma rays undergo Compton scattering off primary scatterers (plastic scintillators) into secondary detectors ($\text{LaBr}_3(\text{Ce})$ or segmented HPGe detectors).
# #    * The relative azimuthal scattering angle $\Delta \phi = \phi_A - \phi_B$ measures the polarization correlation function:
# #      $$N(\Delta \phi) \propto 1 - A \cos(2\Delta \phi)$$
# #
# # ---
# #
# # ### 3. Measuring $\mathcal{C}_{\text{max}}$ Suppression
# #
# # To evaluate whether state capacity scales non-linearly with baseline length $L$ or photon flux density $\Phi$:
#
# # 1. **Calculate Modulation Depth (Visibility):**
# #    $$V = \frac{N(90^\circ) - N(0^\circ)}{N(90^\circ) + N(0^\circ)}$$
# # 2. **Evaluate Capacity Threshold Bound:**
# #    * Compare measured visibility $V_{\text{exp}}(L)$ against the linear QED prediction $V_{\text{QED}} \approx 0.53$ (accounting for finite detector solid angles).
# #    * The $\mathcal{C}_{\text{max}}$ model predicts a non-linear cutoff at critical distance $L_{\text{crit}}$:
# #      $$V_{\text{predicted}}(L) = V_{\text{QED}} \times \exp\left(-\max\left(0, S(\rho_A) - \mathcal{C}_{\text{max}}(L)\right)\right)$$
# #
# # ---
# #
# # ### 4. Student Exercise: Analyzing Compton Polarimetry Data
# #
# # ```python
# # import numpy as np
# #
# # def predict_positronium_visibility(baseline_meters, c_max_threshold=100.0):
# #     """
# #     Computes expected polarization correlation visibility for p-Ps gamma pairs
# #     under C_max capacity constraints vs. standard QED bounds.
# #     """
# #     # Standard Klein-Nishina QED visibility limit (geometric factor applied)
# #     v_qed = 0.53 
# #     
# #     # Phenomenological entropy buildup along path L
# #     accumulated_entropy = 0.8 * baseline_meters  # arbitrary path-entropy factor
# #     
# #     if accumulated_entropy > c_max_threshold:
# #         suppression = np.exp(-(accumulated_entropy - c_max_threshold))
# #     else:
# #         suppression = 1.0
# #         
# #     return v_qed * suppression
# #
# # # Example: Sweep baseline distance L from 0 to 200 meters
# # distances = np.linspace(0, 200, 50)
# # visibilities = [predict_positronium_visibility(L, c_max_threshold=80.0) for L in distances]
#
# # ## 5.6 Macroscopic Quantum Tunneling (MQT) & State Capacity Saturation
# #
# # Beyond single-particle barrier transmission, Macroscopic Quantum Tunneling in superconducting Josephson junctions involves trillions of Cooper pairs acting as a single collective degree of freedom—the phase difference $\phi$.
# #
# # ---
# #
# # ### 1. The Washboard Potential & Phase Superposition
# # A current-biased Josephson junction operates in a tilted-washboard potential:
# #
# # $$U(\phi) = -E_J \cos\phi - E_J \left(\frac{I}{I_c}\right)\phi$$
# #
# # As the bias current approaches the critical current ($I \to I_c$), the potential barrier height vanishes. The phase variable $\phi$ undergoes tunneling from the metastable trapped state $\vert{}\phi_{\text{trapped}}\rangle$ to the running voltage state $\vert{}\phi_{\text{running}}\rangle$:
# #
# # $$\vert{}\Psi_{\text{MQT}}\rangle = \sqrt{1 - \mathcal{T}_{\text{MQT}}} \, \vert{}\phi_{\text{trapped}}\rangle + \sqrt{\mathcal{T}_{\text{MQT}}} \, \vert{}\phi_{\text{running}}\rangle$$
# #
# # ---
# #
# # ### 2. $\mathcal{C}_{\text{max}}$ Non-Linear Barrier Suppression
# # As $\mathcal{T}_{\text{MQT}} \to 0.5$, the spatial/phase branch entropy reaches a maximum $S(\rho_\phi) \approx 1.0\text{ bit}$. 
# #
# # If the capacity threshold $\mathcal{C}_{\text{max}}$ is set lower than the accumulated entanglement entropy between the junction and the external bias environment, non-linear state suppression activates:
# #
# # $$\Gamma_{\text{effective}} = \Gamma_{\text{WKB}} \times \exp\left(-\max\left(0, S(\rho_\phi) - \mathcal{C}_{\text{max}}\right)\right)$$
# #
# # * **Standard QM Prediction:** Smooth exponential temperature dependence ($\Gamma \propto e^{-\Delta U / k_B T}$) transitioning to a temperature-independent quantum tunneling plateau at low temperatures ($T < T^*$).
# # * **$\mathcal{C}_{\text{max}}$ Signature:** A sharp non-linear drop in escape rate $\Gamma_{\text{effective}}$ below the expected WKB tunneling plateau, occurring strictly when the phase superposition entropy saturates local capacity limits.
# #
# # ---
# #
# # ### 3. Student Exercise 5.4: Simulating Josephson MQT Escape Rates
# #
# # > 1. Derive the WKB phase escape rate $\Gamma_{\text{WKB}} = \frac{\omega_p}{2\pi} \exp\left(-\frac{36}{5} \frac{E_J}{\hbar \omega_p} \left(1 - \frac{I}{I_c}\right)^{5/4}\right)$ where $\omega_p$ is the plasma frequency.
# # > 2. Implement a Python function calculating the transition from thermal activation to MQT, and evaluate how $\mathcal{C}_{\text{max}}$ truncates the tunneling plateau.
# #
# # ```python
# # import numpy as np
# #
# # def simulate_josephson_cmax_plateau(i_bias_ratio=0.98, ej_ec_ratio=80.0, c_max_bound=0.4):
# #     """
# #     Computes WKB MQT phase tunneling rate and evaluates C_max non-linear suppression.
# #     """
# #     # WKB tunneling transmission factor
# #     barrier_factor = (1.0 - i_bias_ratio)**(1.25)
# #     t_wkb = np.exp(-12.0 * np.sqrt(ej_ec_ratio) * barrier_factor)
# #     
# #     # Subsystem entropy of trapped vs tunneled phase branches
# #     if 0.0 < t_wkb < 1.0:
# #         s_phase = -(t_wkb * np.log2(t_wkb) + (1.0 - t_wkb) * np.log2(1.0 - t_wkb))
# #     else:
# #         s_phase = 0.0
# #         
# #     # Non-linear capacity suppression
# #     delta_s = max(0.0, s_phase - c_max_bound)
# #     suppression = np.exp(-delta_s)
# #     
# #     return {
# #         "t_wkb": t_wkb,
# #         "entropy_bits": s_phase,
# #         "c_max_suppressed_rate": t_wkb * suppression
# #     }
#
# # +
# ## 5.7 Discriminating Non-Linear Dynamics: Gross-Pitaevskii Mean-Field vs. $\mathcal{C}_{\text{max}}$ Collapse
#
# A fundamental challenge in experimental tests of state-capacity limits ($\mathcal{C}_{\text{max}}$) is distinguishing true non-unitary wavefunction collapse from emergent non-linearities governed by standard linear quantum mechanics. 
#
# Bose-Einstein Condensates (BECs) tunneling through optical lattice barriers exhibit pronounced non-exponential decay and self-trapping. However, this behavior stems from classical mean-field interactions rather than a fundamental breach of Hilbert space capacity.
#
# ---
#
# ### 1. Mathematical Comparison of Non-Linear Frameworks
#
# | Parameter / Feature | Gross-Pitaevskii (GP) Mean-Field | $\mathcal{C}_{\text{max}}$ State-Capacity Collapse |
# | :--- | :--- | :--- |
# | **Physical Origin** | Inter-particle $s$-wave scattering ($g = \frac{4\pi\hbar^2 a_s}{m}$) | Local entanglement entropy saturation ($S(\rho_{\text{sub}}) \to \mathcal{C}_{\text{max}}$) |
# | **Governing Equation** | $i\hbar \frac{\partial \psi}{\partial t} = \left(-\frac{\hbar^2}{2m}\nabla^2 + V_{\text{ext}} + g|\psi|^2\right)\psi$ | $i\hbar \frac{\partial |\psi\rangle}{\partial t} = \hat{H}|\psi\rangle - i\hbar \gamma \max(0, S - \mathcal{C}_{\text{max}})|\psi\rangle$ |
# | **Unitary / Reversible?** | **Unitary** (Conserves total particle number $\int |\psi|^2 d^3r = N$) | **Non-Unitary** (Prunes non-viable state branches) |
# | **Scaling Variable** | Local spatial particle density $n(\mathbf{r}) = |\psi(\mathbf{r})|^2$ | Reduced subsystem von Neumann entropy $S(\rho_A) = -\text{Tr}(\rho_A \log_2 \rho_A)$ |
# | **Mechanism** | Dynamic modulation of the effective barrier height $V_{\text{eff}} = V_{\text{ext}} + g|\psi|^2$ | Non-linear suppression factor $F = \exp\left(-\max(0, S - \mathcal{C}_{\text{max}})\right)$ |
#
# ---
#
# ### 2. Dynamical Behaviors in Barrier Tunneling
#
# #### A. Gross-Pitaevskii Self-Trapping
# In a double-well potential, the $g|\psi|^2$ interaction term introduces an energy shift between the wells proportional to the population difference $\Delta N = N_L - N_R$. 
#
# * **Macroscopic Quantum Self-Trapping (MQST):** When the initial population imbalance exceeds a critical threshold ($\Delta N > \Delta N_{\text{crit}}$), the mean-field energy shift renders tunneling off-resonant. The condensate becomes "trapped" in one well.
# * **Key Signature:** The dynamics remain conservative. Reversing the potential barrier parameters or applying an oscillating drive restores full coherence and tunneling oscillations.
#
# #### B. $\mathcal{C}_{\text{max}}$ Non-Unitary State Pruning
# In contrast, $\mathcal{C}_{\text{max}}$ suppression is insensitive to mere particle density $n(\mathbf{r})$ unless that density generates entanglement entropy across a subsystem boundary.
#
# * **Entropy Saturation:** When a BEC in spatial superposition entangles with an external optical or cavity field, $S(\rho_A)$ scales. Crossing $\mathcal{C}_{\text{max}}$ triggers exponential damping of spatial interference fringes.
# * **Key Signature:** Uncomputation ($U^\dagger$) fails to recover the initial state vector. The loss of fringe visibility is irreversible and leads directly to decoherence without altering the underlying single-particle Hamiltonian $V_{\text{ext}}$.
#
# ---
#
# ### 3. Experimental Protocol for Disambiguation
#
# To rule out Gross-Pitaevskii mean-field artifacts when searching for $\mathcal{C}_{\text{max}}$ collapse in ultra-cold atom experiments:
#
# 1. **Feshbach Resonance Tuning ($g \to 0$):**
#    Apply an external magnetic field near a Feshbach resonance to adjust the $s$-wave scattering length $a_s$ precisely to zero. 
#    * If non-linear tunneling decay vanishes when $g = 0$, the effect was entirely **GP mean-field interaction**.
#    * If non-linear suppression persists while $g = 0$ as subsystem entanglement $S(\rho_A)$ scales, it indicates a **fundamental capacity limit ($\mathcal{C}_{\text{max}}$)**.
#
# 2. **Entanglement vs. Density Isolation:**
#    Compare a high-density, non-entangled condensate against a low-density, highly entangled atom-cavity system. $\mathcal{C}_{\text{max}}$ collapse will strictly select for elevated $S(\rho_A)$, whereas GP dynamics strictly select for high density $|\psi|^2$.
#
# ---
#
# ### 4. Student Exercise 5.5: Disambiguating Non-Linearities
#
# > 1. Write a Python function comparing the decay profile of a 1D Gross-Pitaevskii non-linear Schrödinger equation against a linear Schrödinger equation modified by the $\mathcal{C}_{\text{max}}$ suppression term $F_{\text{suppression}}$.
# > 2. Calculate the critical scattering length $a_s^*$ at which GP mean-field energy shifts match a hypothetical $\mathcal{C}_{\text{max}}$ damping rate $\gamma$.
# # -


# %% [markdown]
# ## 5.7 Discriminating Non-Linear Dynamics: Gross-Pitaevskii Mean-Field vs. $\mathcal{C}_{\text{max}}$ Collapse
#
# A fundamental challenge in experimental tests of state-capacity limits ($\mathcal{C}_{\text{max}}$) is distinguishing true non-unitary wavefunction collapse from emergent non-linearities governed by standard linear quantum mechanics. 
#
# Bose-Einstein Condensates (BECs) tunneling through optical lattice barriers exhibit pronounced non-exponential decay and self-trapping. However, this behavior stems from classical mean-field interactions rather than a fundamental breach of Hilbert space capacity.
#
# ---
#
# ### 1. Mathematical Comparison of Non-Linear Frameworks
#
# | Parameter / Feature | Gross-Pitaevskii (GP) Mean-Field | $\mathcal{C}_{\text{max}}$ State-Capacity Collapse |
# | :--- | :--- | :--- |
# | **Physical Origin** | Inter-particle $s$-wave scattering ($g = \frac{4\pi\hbar^2 a_s}{m}$) | Local entanglement entropy saturation ($S(\rho_{\text{sub}}) \to \mathcal{C}_{\text{max}}$) |
# | **Governing Equation** | $i\hbar \frac{\partial \psi}{\partial t} = \left(-\frac{\hbar^2}{2m}\nabla^2 + V_{\text{ext}} + g\|\psi\|^2\right)\psi$ | $i\hbar \frac{\partial \|\psi\rangle}{\partial t} = \hat{H}\|\psi\rangle - i\hbar \gamma \max(0, S - \mathcal{C}_{\text{max}})\|\psi\rangle$ |
# | **Unitary / Reversible?** | **Unitary** (Conserves total particle number $\int \|\psi\|^2 d^3r = N$) | **Non-Unitary** (Prunes non-viable state branches) |
# | **Scaling Variable** | Local spatial particle density $n(\mathbf{r}) = \|\psi(\mathbf{r})\|^2$ | Reduced subsystem von Neumann entropy $S(\rho_A) = -\text{Tr}(\rho_A \log_2 \rho_A)$ |
# | **Mechanism** | Dynamic modulation of effective barrier height $V_{\text{eff}} = V_{\text{ext}} + g\|\psi\|^2$ | Non-linear suppression factor $F = \exp\left(-\max(0, S - \mathcal{C}_{\text{max}})\right)$ |
#
# ---
#
# ### 2. Dynamical Behaviors in Barrier Tunneling
#
# #### A. Gross-Pitaevskii Self-Trapping
# In a double-well potential, the $g\|\psi\|^2$ interaction term introduces an energy shift between the wells proportional to the population difference $\Delta N = N_L - N_R$. 
#
# * **Macroscopic Quantum Self-Trapping (MQST):** When the initial population imbalance exceeds a critical threshold ($\Delta N > \Delta N_{\text{crit}}$), the mean-field energy shift renders tunneling off-resonant. The condensate becomes "trapped" in one well.
# * **Key Signature:** The dynamics remain conservative. Reversing potential barrier parameters or applying an oscillating drive restores full coherence and tunneling oscillations.
#
# #### B. $\mathcal{C}_{\text{max}}$ Non-Unitary State Pruning
# In contrast, $\mathcal{C}_{\text{max}}$ suppression is insensitive to mere particle density $n(\mathbf{r})$ unless that density generates entanglement entropy across a subsystem boundary.
#
# * **Entropy Saturation:** When a BEC in spatial superposition entangles with an external optical or cavity field, $S(\rho_A)$ scales. Crossing $\mathcal{C}_{\text{max}}$ triggers exponential damping of spatial interference fringes.
# * **Key Signature:** Uncomputation ($U^\dagger$) fails to recover the initial state vector. The loss of fringe visibility is irreversible and leads directly to decoherence without altering the underlying single-particle Hamiltonian $V_{\text{ext}}$.
#
# ---
#
# ### 3. Experimental Protocol for Disambiguation
#
# To rule out Gross-Pitaevskii mean-field artifacts when searching for $\mathcal{C}_{\text{max}}$ collapse in ultra-cold atom experiments:
#
# 1. **Feshbach Resonance Tuning ($g \to 0$):**
#    Apply an external magnetic field near a Feshbach resonance to adjust the $s$-wave scattering length $a_s$ precisely to zero. 
#    * If non-linear tunneling decay vanishes when $g = 0$, the effect was entirely **GP mean-field interaction**.
#    * If non-linear suppression persists while $g = 0$ as subsystem entanglement $S(\rho_A)$ scales, it indicates a **fundamental capacity limit ($\mathcal{C}_{\text{max}}$)**.
#
# 2. **Entanglement vs. Density Isolation:**
#    Compare a high-density, non-entangled condensate against a low-density, highly entangled atom-cavity system. $\mathcal{C}_{\text{max}}$ collapse will strictly select for elevated $S(\rho_A)$, whereas GP dynamics strictly select for high density $\|\psi\|^2$.

# %%
import numpy as np

def compare_gp_vs_cmax_decay(
    t_steps: np.ndarray, 
    g_interaction: float = 0.5, 
    c_max_bound: float = 0.8, 
    subsystem_entropy: float = 1.2
) -> dict:
    """
    Simulates the contrasting decay dynamics between Gross-Pitaevskii (GP) mean-field 
    density shifts and C_max state-capacity non-linear branch suppression.
    """
    # 1. Linear baseline transmission amplitude
    linear_amplitude = np.exp(-0.1 * t_steps)
    
    # 2. Gross-Pitaevskii (GP) conservative phase/density modulation
    # Interaction parameter g causes oscillatory self-trapping phase modulation
    gp_density = linear_amplitude**2
    gp_amplitude = linear_amplitude * np.cos(g_interaction * gp_density * t_steps)
    
    # 3. C_max Non-Unitary State-Capacity Branch Suppression
    # Activates strictly when subsystem_entropy > c_max_bound
    delta_s = max(0.0, subsystem_entropy - c_max_bound)
    cmax_suppression_factor = np.exp(-delta_s * t_steps)
    cmax_amplitude = linear_amplitude * cmax_suppression_factor
    
    return {
        "time": t_steps,
        "linear": linear_amplitude,
        "gp_mean_field": gp_amplitude,
        "cmax_suppressed": cmax_amplitude
    }

# Quick validation check of execution
t = np.linspace(0, 5, 50)
results = compare_gp_vs_cmax_decay(t_steps=t, g_interaction=0.8, c_max_bound=0.5, subsystem_entropy=1.0)

print(f"Time Step t=5.0 s Amplitude Comparison:")
print(f"  -> Linear QM Baseline:      {results['linear'][-1]:.4f}")
print(f"  -> GP Mean-Field (g=0.8):   {results['gp_mean_field'][-1]:.4f}")
print(f"  -> C_max Collapse (S=1.0):   {results['cmax_suppressed'][-1]:.4f}")

# %%
