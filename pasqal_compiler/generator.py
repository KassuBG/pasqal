from pyqir import IntType, PointerType
import pyqir
from qadence import QuantumCircuit
from module import QdToQirModule


class QirGenerator:
    """Generate QIR from a pytket circuit."""

    def __init__(
        self,
        circuit: QuantumCircuit,
        module: QdToQirModule,
        qir_int_type: int,
    ) -> None:
        self.circuit = circuit
        self.module = module
        self.qir_int_type = IntType(module.context, qir_int_type)
        self.qir_i1p_type = PointerType(IntType(module.context, 1))
        self.qir_bool_type = IntType(module.context, 1)
        self.qubit_type = pyqir.qubit_type(module.context)
        self.result_type = pyqir.result_type(module.context)

    def _to_qis_qubits(self, qubits: tuple[int]) -> list[int]:
        """Convert qubits to QIS qubits."""
        return [self.module.module.qubits[qubit] for qubit in qubits]

    def _get_gate(self, gate_name: str) -> callable:
        """Get a gate function from the module."""
        return getattr(self.module.qis, gate_name)

    def circuit_to_module(
        self, circuit: QuantumCircuit, module: QdToQirModule, record_output: bool = False
    ) -> QdToQirModule:
        """Populate a PyQir module from a qadence circuit."""
        for block in circuit.blocks:
            qubits = self._to_qis_qubits(block.qubits)
            gate_name = self.module.gateset.qd_to_gateset(block.name)
            gate_func = self._get_gate(gate_name)
            gate_func(*qubits)
            
        return module


