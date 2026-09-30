# Q.Ant Qubit Wave Test & Photonic Quantum Simulation

Ein Python-Framework zur Simulation von Quantenzuständen, Standard-Quantengattern ($X, Y, Z, H$) sowie **integrierter Quantenphotonik (Q.Ant TFLN Technologie)**.

---

## 🚀 Übersicht & Highlights

- **Standard-Qubit-Simulation:** Zustand Vektor $|\psi\rangle = \alpha |0\rangle + \beta |1\rangle$ mit Pauli-X, Y, Z und Hadamard Gattern.
- **Q.Ant Quantum Photonics Integration:** Simulation von **Thin-Film Lithium Niobate (TFLN)** photonischen Komponenten:
  - **Electro-Optic Phase Shifter:** $R(\phi) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\phi} \end{pmatrix}$
  - **Integrated Optical Beam Splitter:** $BS(\theta, \phi) = \begin{pmatrix} \cos\theta & -i e^{i\phi}\sin\theta \\ -i e^{-i\phi}\sin\theta & \cos\theta \end{pmatrix}$
  - **Mach-Zehnder Interferometer (MZI):** Spannungsgesteuerte optische Interferometer-Module ($V_\phi, V_\theta$).
  - **Dual-Rail Mode Mapping:** Übersetzung in optische Moden-Amplituden ($|1,0\rangle_{spatial}$ & $|0,1\rangle_{spatial}$).
- **Qiskit Interoperabilität:** Direkte Konvertierung des Zustandsvektors in ein Qiskit `QuantumCircuit`-Objekt.
- **Quantum Fourier Transform (QFT):** Einbindung von QFT-Transformationen und Spektralanalyse für generative Quantenmodelle.

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

## 🔬 Code-Beispiel: Standard Qubit & Q.Ant Photonic Qubit

```python
from MinimalQubit import MinimalQubit, QAntPhotonicQubit

# 1. Standard Qubit mit Hadamard & Z-Gatter
qubit = MinimalQubit()
qubit.h().z()
print("Zustandsvektor:", qubit.statevector)
print("Dual-Rail Moden:", qubit.to_dual_rail_modes())

# 2. Q.Ant TFLN Photonisches Qubit mit Spannungssteuerung
qant_qubit = QAntPhotonicQubit(v_pi=3.3)
qant_qubit.apply_voltage_phase_shift(1.65)  # V_pi/2 steuert Phase pi/2
print("Photonischer Zustand nach 1.65 V Modulation:", qant_qubit.statevector)
```

---

## 📘 NotebookLM Einbindung

Dieses Repository ist optimiert für die Verknüpfung mit **Google NotebookLM**:
- **Notebook Link:** [Google NotebookLM Workspace](https://notebook.google.com/notebook/fe6fdd55-fb14-4bc1-be46-3d4eba5a2077)
- **Anleitung:** Siehe [`NOTEBOOKLM_GUIDE.md`](./NOTEBOOKLM_GUIDE.md) für Schritt-für-Schritt Anweisungen zum Importieren der Quellcodes und Dokumente in NotebookLM.

---

## 📜 Lizenz
MIT License
