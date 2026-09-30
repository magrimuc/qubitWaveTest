# Q.Ant Qubit Wave Test, Photonic Quantum Simulation & Grover Search

Ein Python-Framework zur Simulation von Quantenzuständen, Standard-Quantengattern ($X, Y, Z, H$), **integrierter Quantenphotonik (Q.Ant TFLN Technologie)** sowie dem **Grover-Suchalgorithmus**.

---

## 🚀 Übersicht & Highlights

- **Standard-Qubit-Simulation:** Zustandsvektor $|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$ mit Pauli-X, Y, Z und Hadamard Gattern.
- **Q.Ant Quantum Photonics Integration:** Simulation von **Thin-Film Lithium Niobate (TFLN)** photonischen Komponenten:
  - **Electro-Optic Phase Shifter:** $R(\phi) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\phi} \end{pmatrix}$
  - **Integrated Optical Beam Splitter:** $BS(\theta, \phi) = \begin{pmatrix} \cos\theta & -i e^{i\phi}\sin\theta \\ -i e^{-i\phi}\sin\theta & \cos\theta \end{pmatrix}$
  - **Mach-Zehnder Interferometer (MZI):** Spannungsgesteuerte optische Interferometer-Module ($V_\phi, V_\theta$).
  - **Dual-Rail Mode Mapping:** Übersetzung in optische Moden-Amplituden ($|1,0\rangle_{spatial}$ & $|0,1\rangle_{spatial}$).
- **Mehr-Qubit-Register & Grover-Algorithmus:**
  - $N$-Qubit Zustandsraum ($2^N$ Dimensionen)
  - Phasen-Orakel & Grover-Diffusor ("Inversion um den Mittelwert")
  - Exakte 2-Qubit Grover-Suche mit 100% Erfolgsquote
  - Projektive Quantenmessung (`measure()`)
- **Qiskit Interoperabilität:** Direkte Konvertierung in Qiskit `QuantumCircuit`-Objekte.

---

## 🛠️ Installation & Tests

### Voraussetzungen
Python 3.9+ und Pytest:
```bash
pip install numpy qiskit pytest
```

### Tests ausführen
```bash
python3 -m pytest
```

---

## 🔬 Code-Beispiele

### 1. Q.Ant TFLN Photonisches Qubit
```python
from MinimalQubit import QAntPhotonicQubit

qant_qubit = QAntPhotonicQubit(v_pi=3.3)
qant_qubit.apply_voltage_phase_shift(1.65)  # V_pi/2 steuert Phase pi/2
print("Photonischer Zustand:", qant_qubit.statevector)
```

### 2. Grover-Algorithmus (2 Qubits, Suche nach |11>)
```python
from MinimalQubit import QubitRegister

# Erstelle 2-Qubit Register und suche nach Zustand |11> (Index 3)
reg = QubitRegister(num_qubits=2)
reg.grover_search(target_index=3, iterations=1)

bitstring, probs = reg.measure()
print(f"Ergebnis der Grover-Suche: Gemessen = |{bitstring}> mit P = {probs[3]:.1%}")
```

---

## 📘 NotebookLM Einbindung

Dieses Repository ist optimiert für die Verknüpfung mit **Google NotebookLM**:
- **Notebook Link:** [Google NotebookLM Workspace](https://notebook.google.com/notebook/fe6fdd55-fb14-4bc1-be46-3d4eba5a2077)
- **Anleitung:** Siehe [`NOTEBOOKLM_GUIDE.md`](./NOTEBOOKLM_GUIDE.md) für Schritt-für-Schritt Anweisungen zum Importieren der Quellcodes und Dokumente in NotebookLM.

---

## 📜 Lizenz
MIT License
