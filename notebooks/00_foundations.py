# Module 00: Classical Foundations — Action Principles & Phase Space

# ## 0.1 Principle of Least Action & Lagrangian Mechanics
# For a system with generalized coordinates $q_i$ and velocities $\dot{q}_i$, the Lagrangian is defined as $L(q, \dot{q}, t) = T - V$.

# The physical trajectory minimizes the action $S = \int L \, dt$, yielding the Euler-Lagrange equations:

# $$\frac{d}{dt}\left(\frac{\partial L}{\partial \dot{q}_i}\right) - \frac{\partial L}{\partial q_i} = 0$$

# ## 0.2 Canonical Quantization via Hamiltonians
# 1. **Conjugate Momenta:** Define $p_i = \frac{\partial L}{\partial \dot{q}_i}$
# 2. **Hamiltonian Formulation:** Perform a Legendre transformation $H(q, p, t) = \sum p_i \dot{q}_i - L$
# 3. **Canonical Commutation:** Transition from Poisson Brackets to Quantum Commutators:
#    $$\{A, B\}_{\text{classical}} \longrightarrow \frac{1}{i\hbar}[\hat{A}, \hat{B}]_{\text{quantum}}$$

# ### Student Exercise 0.1: Harmonic Oscillator Transition
# > Derive the classical Hamiltonian for a harmonic oscillator $H = \frac{p^2}{2m} + \frac{1}{2}m\omega^2 q^2$, promote $q$ and $p$ to operators $[\hat{q}, \hat{p}] = i\hbar$, and show how ladder operators $a, a^\dagger$ diagonalize the Hamiltonian into $H = \hbar\omega(a^\dagger a + \frac{1}{2})$.


