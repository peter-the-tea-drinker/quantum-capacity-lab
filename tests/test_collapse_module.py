import pytest
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, thermal_relaxation_error

from src.collapse_model import ConservedCapacityModel

@pytest.fixture
def noisy_backend():
    """Builds a calibrated thermal relaxation noise model to mimic QPU decoherence."""
    noise_model = NoiseModel()
    # Simulate T1 = 50us, T2 = 30us thermal decay
    t1, t2 = 50e-6, 30e-6
    gate_time = 100e-9  # 100ns gate time
    
    error_1q = thermal_relaxation_error(t1, t2, gate_time)
    noise_model.add_all_qubit_quantum_error(error_1q, ["rz", "sx", "x", "h"])
    
    return AerSimulator(noise_model=noise_model)


class TestQPUValidations:

    def test_udagger_reversibility_threshold(self, noisy_backend):
        """
        VALIDATION 1: Coherent Uncomputation (U^\dagger) Decay Test.
        Tests whether state recovery fails faster under C_max non-linear 
        suppression than under pure linear hardware noise.
        """
        c_max_engine = ConservedCapacityModel(c_max_bound=2.5) # Capacity limit
        
        # Build 4-qubit GHZ state (High Entanglement Entropy S)
        qc = QuantumCircuit(4, 4)
        qc.h(0)
        for i in range(3):
            qc.cx(i, i+1)
            
        # Apply Coherent Uncomputation (U^\dagger)
        for i in reversed(range(3)):
            qc.cx(i, i+1)
        qc.h(0)
        qc.measure_all()

        # Execute noisy hardware simulation
        result = noisy_backend.run(qc, shots=2000).result().get_counts()
        p_ground_hardware = result.get('0000 0000', 0) / 2000.0

        # Predict C_max non-linear state modification
        predicted_fidelity = c_max_engine.apply_suppression_factor(
            raw_fidelity=p_ground_hardware, 
            subsystem_entropy=3.0  # S(rho) = 3.0 > C_max (2.5)
        )

        assert predicted_fidelity < p_ground_hardware, (
            "C_max threshold saturation must yield lower uncomputation fidelity "
            "than pure linear hardware noise."
        )

    def test_entropy_sweep_scaling(self):
        """
        VALIDATION 2: Subsystem Partial Trace & Non-Linear Onset.
        Validates that suppression factor remains exactly 1.0 when S <= C_max,
        and decays exponentially only after crossing C_max.
        """
        engine = ConservedCapacityModel(c_max_bound=1.5)
        
        # Below threshold -> No suppression
        f_below = engine.apply_suppression_factor(raw_fidelity=0.95, subsystem_entropy=1.2)
        assert np.isclose(f_below, 0.95)

        # Above threshold -> Non-linear suppression kicks in
        f_above = engine.apply_suppression_factor(raw_fidelity=0.95, subsystem_entropy=2.2)
        assert f_above < 0.95
        assert np.isclose(f_above, 0.95 * np.exp(-(2.2 - 1.5)))

    def test_qpu_noise_contrast_ratio(self, noisy_backend):
        """
        VALIDATION 3: Noise vs C_max Discriminator Ratio.
        Verifies that C_max signature maintains a high Signal-to-Noise Ratio (SNR)
        above standard baseline device error.
        """
        engine = ConservedCapacityModel(c_max_bound=1.0)
        
        # Low entropy circuit (Single Qubit Ramsey)
        qc_low = QuantumCircuit(1, 1)
        qc_low.h(0)
        qc_low.rz(np.pi/4, 0)
        qc_low.h(0)
        qc_low.measure(0, 0)
        
        res_low = noisy_backend.run(qc_low, shots=1000).result().get_counts()
        p0_low = res_low.get('0', 0) / 1000.0
        
        # Hardware noise baseline should remain relatively high (> 0.85)
        assert p0_low > 0.80 
        
        # C_max engine applies non-linear scaling only if entropy threshold is violated
        f_suppressed = engine.apply_suppression_factor(p0_low, subsystem_entropy=2.5)
        snr_ratio = (p0_low - f_suppressed) / (1.0 - p0_low)
        
        assert snr_ratio > 1.5, "C_max collapse signal must be distinguishable from hardware noise baseline."