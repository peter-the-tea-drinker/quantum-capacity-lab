"""
src/collapse_model.py

Core non-linear collapse framework for the Conserved Many-Worlds / State-Capacity (C_max) hypothesis.
Includes state tracking, entropy calculation, non-linear threshold testing, and control/manipulation checks.
"""

import os
import pickle
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, partial_trace, entropy


class ConservedCapacityModel:
    """
    Simulates quantum state capacity evolution under the C_max hypothesis.
    
    Attributes:
        num_qubits (int): Number of qubits in the Hilbert space.
        c_max (float): Maximum allowed state capacity threshold (bits).
        circuit (QuantumCircuit): Active Qiskit circuit representation.
    """

    def __init__(self, num_qubits: int = 2, c_max: float = 1.0):
        """
        Initialize the C_max capacity simulation engine.
        
        Args:
            num_qubits (int): Total system size (default: 2 qubits).
            c_max (float): Theoretical entropy/capacity limit in bits (default: 1.0 bit).
        """
        self.num_qubits = num_qubits
        self.c_max = float(c_max)
        self.circuit = QuantumCircuit(self.num_qubits)

    def reset_circuit(self):
        """Reset the internal quantum circuit."""
        self.circuit = QuantumCircuit(self.num_qubits)

    def build_entangled_state(self, theta: float):
        """
        Construct a parameterized entangled state between subsystem A (qubit 0) 
        and subsystem B (qubit 1).
        
        Args:
            theta (float): Rotation angle controlling entanglement strength.
        """
        self.reset_circuit()
        self.circuit.h(0)
        self.circuit.cry(theta, 0, 1)

    def calculate_subsystem_entropy(self, traced_qubit: int = 1) -> float:
        """
        Calculate the von Neumann entropy S(rho_A) of the reduced density matrix.
        
        Args:
            traced_qubit (int): Qubit index to trace out (default: 1).
            
        Returns:
            float: von Neumann entropy in bits.
        """
        sv = Statevector.from_instruction(self.circuit)
        rho_sub = partial_trace(sv, [traced_qubit])
        return float(entropy(rho_sub, base=2))

    def evaluate_collapse_threshold(self, current_entropy: float) -> dict:
        """
        Check whether current state entropy breaches the C_max capacity bound.
        
        Args:
            current_entropy (float): Calculated entropy of the subsystem.
            
        Returns:
            dict: Collapse status, capacity utilization, and effective suppression factor.
        """
        utilization = current_entropy / self.c_max if self.c_max > 0 else 1.0
        is_collapsed = current_entropy >= self.c_max
        
        # Non-linear damping factor (suppression active beyond C_max)
        suppression_factor = np.exp(-max(0.0, current_entropy - self.c_max))

        return {
            "current_entropy": current_entropy,
            "c_max": self.c_max,
            "utilization_pct": min(100.0, utilization * 100.0),
            "is_collapsed": is_collapsed,
            "suppression_factor": suppression_factor
        }

    # -------------------------------------------------------------------
    # Manipulation & Control Checks
    # -------------------------------------------------------------------

    def check_phase_control_manipulation(self, phase_shift: float, theta: float) -> dict:
        """
        Control Check 1: Phase Steering / Coherence Recovery
        Tests if applying a local unit phase rotation Rz(phase_shift) can alter 
        subsystem entropy or bypass the C_max collapse threshold.
        """
        self.build_entangled_state(theta)
        
        # Pre-manipulation entropy
        s_initial = self.calculate_subsystem_entropy(traced_qubit=1)
        
        # Apply local control manipulation on subsystem A
        self.circuit.rz(phase_shift, 0)
        s_post_manipulation = self.calculate_subsystem_entropy(traced_qubit=1)
        
        # Unitary invariance check: Local unitaries MUST NOT alter entanglement entropy
        entropy_invariant = np.isclose(s_initial, s_post_manipulation, atol=1e-7)

        return {
            "test": "Phase Control Manipulation",
            "phase_shift": phase_shift,
            "s_initial": s_initial,
            "s_post_manipulation": s_post_manipulation,
            "entropy_invariant": bool(entropy_invariant),
            "controllable_via_local_phase": not entropy_invariant
        }

    def check_uncomputation_recovery(self, theta: float) -> dict:
        """
        Control Check 2: Uncomputation / Reversibility Check
        Tests whether coherent state uncomputation (applying U^dagger) restores 
        subsystem purity before collapse irreversible decay sets in.
        """
        self.build_entangled_state(theta)
        
        # Apply exact inverse unitary gates (Uncomputation)
        self.circuit.cry(-theta, 0, 1)
        self.circuit.h(0)
        
        s_recovered = self.calculate_subsystem_entropy(traced_qubit=1)
        is_fully_recovered = np.isclose(s_recovered, 0.0, atol=1e-5)

        return {
            "test": "Uncomputation Recovery Check",
            "s_recovered": s_recovered,
            "is_fully_recovered": bool(is_fully_recovered),
            "reversible": bool(is_fully_recovered)
        }

    def run_sweep_and_cache(self, steps: int = 50, cache_path: str = "data/cmax_model_cache.pkl") -> dict:
        """
        Execute a full parameter sweep over entanglement angle theta, 
        evaluating C_max limits and pickling the results.
        """
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        
        if os.path.exists(cache_path):
            with open(cache_path, "rb") as f:
                return pickle.load(f)

        thetas = np.linspace(0, np.pi, steps)
        results = {
            "thetas": thetas,
            "entropies": [],
            "suppression_factors": [],
            "collapse_flags": []
        }

        for th in thetas:
            self.build_entangled_state(th)
            s = self.calculate_subsystem_entropy()
            eval_res = self.evaluate_collapse_threshold(s)
            
            results["entropies"].append(s)
            results["suppression_factors"].append(eval_res["suppression_factor"])
            results["collapse_flags"].append(eval_res["is_collapsed"])

        with open(cache_path, "wb") as f:
            pickle.dump(results, f)

        return results


if __name__ == "__main__":
    # Internal module test script
    model = ConservedCapacityModel(num_qubits=2, c_max=0.8)
    
    print("--- Running C_max Collapse Model Tests ---")
    model.build_entangled_state(theta=np.pi / 2)
    s = model.calculate_subsystem_entropy()
    status = model.evaluate_collapse_threshold(s)
    print(f"Subsystem Entropy S(rho_A): {s:.4f} bits")
    print(f"C_max Status: Collapsed={status['is_collapsed']}, Utilization={status['utilization_pct']:.1f}%")
    
    print("\n--- Running Control / Manipulation Checks ---")
    phase_check = model.check_phase_control_manipulation(phase_shift=np.pi/4, theta=np.pi/2)
    print(f"Phase Control Invariance Check Passed: {phase_check['entropy_invariant']}")
    
    uncomp_check = model.check_uncomputation_recovery(theta=np.pi/2)
    print(f"Uncomputation Reversibility Check Passed: {uncomp_check['is_fully_recovered']}")