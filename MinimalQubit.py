import math
import numpy as np
import qiskit as qt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

class MinimalQubit:
    """
    MinimalQubit: Simulator für ein einzelnes Qubit mit Unterstützung für 
    Standard-Quantengatter (Pauli X, Y, Z, Hadamard) sowie photonischen
    Gattern basierend auf Q.Ant Thin-Film Lithium Niobate (TFLN) Technologie.
    """

    def __init__(self):
        # Initialisierung im Zustand |0>
        # [alpha, beta] -> entspricht alpha*|0> + beta*|1>
        self.state = np.array([1.0 + 0j, 0.0 + 0j], dtype=complex)

    @property
    def statevector(self):
        """Gibt den aktuellen 2D-komplexen Zustandsvektor zurück."""
        return self.state

    def x(self):
        """Pauli-X Gatter (NOT-Gatter / Optical Mode Swap)"""
        X_gate = np.array([
            [0.0 + 0j, 1.0 + 0j],
            [1.0 + 0j, 0.0 + 0j]
        ])
        self.state = X_gate @ self.state
        return self

    def y(self):
        """Pauli-Y Gatter"""
        Y_gate = np.array([
            [0.0 + 0j, -1.0j],
            [1.0j, 0.0 + 0j]
        ])
        self.state = Y_gate @ self.state
        return self

    def z(self):
        """Pauli-Z Gatter"""
        Z_gate = np.array([
            [1.0 + 0j, 0.0 + 0j],
            [0.0 + 0j, -1.0 + 0j]
        ])
        self.state = Z_gate @ self.state
        return self

    def h(self):
        """Hadamard Gatter (50:50 Optical Beam Splitter + Phase Shift)"""
        norm = 1.0 / math.sqrt(2)
        H_gate = norm * np.array([
            [1.0 + 0j, 1.0 + 0j],
            [1.0 + 0j, -1.0 + 0j]
        ])
        self.state = H_gate @ self.state
        return self

    # --- Q.Ant Photonic Quantum Hardware Extensions ---

    def apply_phase_shift(self, phi: float):
        """
        Optischer Phasenverschieber R(phi) (Electro-Optic Phase Shifter).
        Matrix: [[1, 0], [0, exp(i*phi)]]
        """
        R_gate = np.array([
            [1.0 + 0j, 0.0 + 0j],
            [0.0 + 0j, np.exp(1j * phi)]
        ], dtype=complex)
        self.state = R_gate @ self.state
        return self

    def apply_beam_splitter(self, theta: float, phi: float = 0.0):
        """
        Optischer Strahlteiler BS(theta, phi) in integrierter Photonik.
        Matrix:
        [[ cos(theta),             -i * exp(i*phi) * sin(theta) ],
         [ -i * exp(-i*phi) * sin(theta), cos(theta)            ]]
        """
        BS_gate = np.array([
            [np.cos(theta), -1j * np.exp(1j * phi) * np.sin(theta)],
            [-1j * np.exp(-1j * phi) * np.sin(theta), np.cos(theta)]
        ], dtype=complex)
        self.state = BS_gate @ self.state
        return self

    def apply_mzi(self, theta: float, phi: float):
        """
        Mach-Zehnder Interferometer (MZI) Baustein für Q.Ant TFLN Chips.
        Kombiniert Strahlteiler und elektro-optische Phasenverschiebung.
        """
        self.apply_beam_splitter(np.pi / 4, 0.0)
        self.apply_phase_shift(phi)
        self.apply_beam_splitter(np.pi / 4, 0.0)
        self.apply_phase_shift(theta)
        return self

    def qft(self):
        """Quantum Fourier Transform (QFT) für 1 Qubit (Hadamard-Transformation)."""
        return self.h()

    def to_dual_rail_modes(self):
        """
        Gibt die photonische Dual-Rail Mode-Amplituden zurück:
        |0> -> Mode 0 (oberer Wellenleiter), |1> -> Mode 1 (unterer Wellenleiter)
        """
        return {
            "mode_0_amplitude": self.state[0],
            "mode_1_amplitude": self.state[1],
            "mode_0_power": float(abs(self.state[0])**2),
            "mode_1_power": float(abs(self.state[1])**2),
        }

    def to_qiskit_circuit(self):
        """Konvertiert den aktuellen Zustandsvektor in einen Qiskit QuantumCircuit."""
        qc = QuantumCircuit(1)
        qc.prepare_state(self.state, [0])
        return qc


class QAntPhotonicQubit(MinimalQubit):
    """
    Simulation eines Q.Ant Thin-Film Lithium Niobate (TFLN) Photonischen Qubits.
    Ermöglicht die Ansteuerung über elektro-optische Modulationsspannungen V_phi und V_theta.
    """
    def __init__(self, v_pi: float = 3.3):
        super().__init__()
        self.v_pi = v_pi  # Halbwelle-Spannung V_pi in Volt

    def apply_voltage_phase_shift(self, voltage: float):
        """Steuert den TFLN-Phasenmodulator mit einer Spannung V an. Delta_phi = pi * V / V_pi."""
        phi = np.pi * (voltage / self.v_pi)
        return self.apply_phase_shift(phi)

    def apply_mzi_voltage(self, v_theta: float, v_phi: float):
        """Steuert ein MZI-Gatter über Spannungen an."""
        theta = np.pi * (v_theta / self.v_pi)
        phi = np.pi * (v_phi / self.v_pi)
        return self.apply_mzi(theta, phi)


class QubitRegister:
    """
    QubitRegister: Simuliert ein N-Qubit Quantenregister.
    Ermöglicht Mehr-Qubit-Verschränkung, Orakel-Gatter, Diffusions-Operatoren
    und den Grover-Suchalgorithmus für beliebige Registergrößen (2, 3, 4, ..., N Qubits).
    """
    def __init__(self, num_qubits: int = 2):
        self.num_qubits = num_qubits
        self.dim = 2 ** num_qubits
        # Startzustand |00...0>
        self.state = np.zeros(self.dim, dtype=complex)
        self.state[0] = 1.0 + 0j

    @property
    def statevector(self):
        """Gibt den aktuellen 2^N komplexen Zustandsvektor zurück."""
        return self.state

    def h_all(self):
        """Wendet das Hadamard-Gatter H^(otimes N) auf alle Qubits an (Superposition)."""
        H1 = 1.0 / math.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=complex)
        HN = H1
        for _ in range(self.num_qubits - 1):
            HN = np.kron(HN, H1)
        self.state = HN @ self.state
        return self

    def apply_oracle(self, target_index: int):
        """
        Orakel-Operator U_omega: Invertiert das Vorzeichen des Zielzustands |target_index>.
        """
        oracle_matrix = np.eye(self.dim, dtype=complex)
        oracle_matrix[target_index, target_index] = -1.0 + 0j
        self.state = oracle_matrix @ self.state
        return self

    def apply_diffuser(self):
        """
        Grover-Diffusor-Operator (Inversion um den Mittelwert): U_s = 2|s><s| - I.
        """
        s = np.ones(self.dim, dtype=complex) / math.sqrt(self.dim)
        diffuser_matrix = 2.0 * np.outer(s, s.conj()) - np.eye(self.dim, dtype=complex)
        self.state = diffuser_matrix @ self.state
        return self

    def grover_search(self, target_index: int, iterations: int = None):
        """
        Führt den Grover-Algorithmus aus.
        Wenn iterations=None ist, wird automatisch die optimale Iterationszahl k ~ pi/4 * sqrt(2^N) berechnet.
        """
        if iterations is None:
            iterations = max(1, int(math.floor(math.pi / 4.0 * math.sqrt(self.dim))))

        # 1. Gleichmäßige Superposition erzeugen
        self.h_all()

        # 2. Grover-Iterationen (Orakel + Diffusor)
        for _ in range(iterations):
            self.apply_oracle(target_index)
            self.apply_diffuser()

        return self

    def measure(self):
        """
        Führt eine Quantenmessung durch und gibt den kollabierten Bitstring
        sowie die Wahrscheinlichkeitsverteilung zurück.
        """
        probabilities = np.abs(self.state) ** 2
        outcome_index = np.random.choice(self.dim, p=probabilities)
        bitstring = format(outcome_index, f'0{self.num_qubits}b')
        return bitstring, probabilities


# --- Beispielnutzung ---
if __name__ == "__main__":
    qubit = MinimalQubit()
    qubit.h().z()
    print("Standard Qubit Zustandsvektor:", qubit.statevector)

    # Grover-Suche auf 3 Qubits (8 Elemente: |000> bis |111>) nach Index 5 ("101")
    reg3 = QubitRegister(num_qubits=3)
    reg3.grover_search(target_index=5)
    bitstring, probs = reg3.measure()
    print(f"3-Qubit Grover Suche nach Index 5 ('101'): Gemessen = |{bitstring}>, Wahrscheinlichkeit = {probs[5]:.1%}")