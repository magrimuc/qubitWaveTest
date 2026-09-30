import math
import pytest
import numpy as np
from MinimalQubit import MinimalQubit, QAntPhotonicQubit, QubitRegister
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import XGate

@pytest.fixture
def qubit():
    """Fixture, die für jeden Test ein frisches Qubit in Zustand |0> bereitstellt."""
    return MinimalQubit()

def test_initialization(qubit):
    """Prüft, ob das Qubit korrekt im Zustand |0> startet ([1, 0])."""
    state = qubit.statevector
    assert state[0] == 1.0 + 0j
    assert state[1] == 0.0 + 0j

def test_pauli_x(qubit):
    # PARALLEL QISKIT AND THEORETICAL CALCULATION 
    state_vector = Statevector(qubit.statevector)
    result_vector = state_vector.evolve(XGate())
    assert result_vector == Statevector([0.0 + 0j, 1.0 + 0j])

    """Pauli-X sollte |0> gegen |1> tauschen (NOT-Gatter)."""
    qubit.x()
    state = qubit.statevector
    assert state[0] == 0.0 + 0j
    assert state[1] == 1.0 + 0j

def test_pauli_z(qubit):
    """Pauli-Z sollte das Vorzeichen von |1> flippen. Bei |0> passiert nichts."""
    qubit.z()
    assert qubit.statevector[0] == 1.0 + 0j
    
    qubit.x()  # in |1> versetzen
    qubit.z()  # Z anwenden -> sollte -1.0 für |1> ergeben
    assert qubit.statevector[1] == -1.0 + 0j

def test_pauli_y(qubit):
    """Pauli-Y auf |0> sollte i*|1> ergeben."""
    qubit.y()
    state = qubit.statevector
    assert state[0] == 0.0 + 0j
    assert state[1] == 0.0 + 1j

def test_hadamard(qubit):
    """Hadamard auf |0> sollte den Plus-Zustand (1/sqrt(2), 1/sqrt(2)) ergeben."""
    qubit.h()
    state = qubit.statevector
    expected = 1 / math.sqrt(2)
    
    assert state[0].real == pytest.approx(expected)
    assert state[0].imag == pytest.approx(0.0)
    assert state[1].real == pytest.approx(expected)
    assert state[1].imag == pytest.approx(0.0)

def test_hadamard_twice(qubit):
    """Zweimal Hadamard sollte wieder den Ausgangszustand herstellen (H * H = I)."""
    qubit.h().h()
    state = qubit.statevector
    assert state[0].real == pytest.approx(1.0)
    assert state[1].real == pytest.approx(0.0)

def test_chained_gates(qubit):
    """Testet eine Kette von Operationen: H -> Z -> H (Sollte das Gleiche wie X tun)."""
    qubit.h().z().h()
    state = qubit.statevector
    assert state[0].real == pytest.approx(0.0)
    assert state[1].real == pytest.approx(1.0)

def test_probability_conservation(qubit):
    """Prüft, ob die Gesamtwahrscheinlichkeit |alpha|^2 + |beta|^2 nach Gattern immer 1 ist."""
    def total_prob(q):
        alpha = q.statevector[0]
        beta = q.statevector[1]
        return abs(alpha)**2 + abs(beta)**2

    assert total_prob(qubit) == pytest.approx(1.0)
    qubit.h()
    assert total_prob(qubit) == pytest.approx(1.0)
    qubit.y()
    assert total_prob(qubit) == pytest.approx(1.0)
    qubit.z()
    assert total_prob(qubit) == pytest.approx(1.0)
    qubit.x()
    assert total_prob(qubit) == pytest.approx(1.0)

# --- Q.ANT PHOTONICS & QFT TESTS ---

def test_qant_phase_shift(qubit):
    """Testet den optischen Phasenverschieber R(pi/2)."""
    qubit.x()  # in |1> versetzen
    qubit.apply_phase_shift(math.pi / 2)
    assert qubit.statevector[0] == 0.0 + 0j
    assert qubit.statevector[1].real == pytest.approx(0.0)
    assert qubit.statevector[1].imag == pytest.approx(1.0)

def test_qant_beam_splitter(qubit):
    """Testet einen 50:50 Strahlteiler (theta = pi/4). Erhält Unitarität."""
    qubit.apply_beam_splitter(math.pi / 4, 0.0)
    prob = abs(qubit.statevector[0])**2 + abs(qubit.statevector[1])**2
    assert prob == pytest.approx(1.0)

def test_qant_photonic_voltage():
    """Testet elektro-optische Spannungseinstellung bei QAntPhotonicQubit."""
    qant = QAntPhotonicQubit(v_pi=3.3)
    qant.x()
    qant.apply_voltage_phase_shift(3.3)  # V_pi entspricht pi Phase -> Vorzeichenwechsel bei |1>
    assert qant.statevector[1].real == pytest.approx(-1.0)

def test_dual_rail_representation(qubit):
    """Prüft die Ausgabe der photonischen Dual-Rail Moden."""
    qubit.h()
    modes = qubit.to_dual_rail_modes()
    assert modes["mode_0_power"] == pytest.approx(0.5)
    assert modes["mode_1_power"] == pytest.approx(0.5)

def test_qiskit_circuit_conversion(qubit):
    """Prüft die Konvertierung in einen Qiskit QuantumCircuit."""
    qubit.h()
    qc = qubit.to_qiskit_circuit()
    assert qc.num_qubits == 1

# --- GROVER ALGORITHM TESTS ---

@pytest.mark.parametrize("target_idx, expected_bitstring", [
    (0, "00"),
    (1, "01"),
    (2, "10"),
    (3, "11")
])
def test_grover_search_2qubit(target_idx, expected_bitstring):
    """Testet den Grover-Algorithmus für alle 4 möglichen Zustände auf 2 Qubits."""
    reg = QubitRegister(num_qubits=2)
    reg.grover_search(target_index=target_idx, iterations=1)
    
    # Prüfe, dass die Wahrscheinlichkeit für das Ziel 100% (1.0) beträgt
    probs = np.abs(reg.statevector) ** 2
    assert probs[target_idx] == pytest.approx(1.0)
    
    bitstring, _ = reg.measure()
    assert bitstring == expected_bitstring
