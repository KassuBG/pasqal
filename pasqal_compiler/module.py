from pyqir import SimpleModule, BasicQisBuilder, PYQIR_GATES

class QdToQirModule:
    """
    PyQir module extension to account for a custom defined input gate set.
    """

    def __init__(self, name: str, num_qubits: int, num_results: int) -> None:
        self.module = SimpleModule(name, num_qubits, num_results)
        self.builder = self.module.builder
        self.context = self.module.context
        self.qis = BasicQisBuilder(self.builder)
        self.gateset = PYQIR_GATES

    def _add_gate(self, gate, qubit):
        """Add a gate to the module."""
        self.qis.add_gate(gate, qubit)

    def h(self, qubit):
        """Add an H gate to the module."""
        self._add_gate("h", qubit)

    def x(self, qubit):
        """Add an X gate to the module."""
        self._add_gate("x", qubit)

    def y(self, qubit):
        """Add a Y gate to the module."""
        self._add_gate("y", qubit)

    def z(self, qubit):
        """Add a Z gate to the module."""
        self._add_gate("z", qubit)

    def measure(self, qubit, target_bit):
        """Measure a qubit and store the result in a target bit."""
        self.qis.measure(qubit, target_bit)






