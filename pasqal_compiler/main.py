from enum import Enum
from qadence import Register, H, X, Y, Z
from module import QdToQirModule  # Importing QdToQirModule from module.py
from pasqal_compiler.generator import QirGenerator
from dataclasses import dataclass
from typing import Union

class QIRFormat(Enum):
    BINARY = 0
    STRING = 1

@dataclass
class MyMeasure:
    qubit: int
    target: int

class MyQuantumCircuit:
    def __init__(self, num_qubits, operations=None):
        self.register = Register(num_qubits)
        self.custom_operations = operations if operations else []
        self.num_qubits = num_qubits
        self.qubits = list(range(num_qubits))  # Track qubits explicitly

    def add_custom_operation(self, op):
        self.custom_operations.append(op)

    @property
    def ops(self):
        return self.custom_operations

def generate_initial_operations(circuit: MyQuantumCircuit) -> None:
    """Add initial H gates to the circuit."""
    initial_operations = [H(target=i) for i in range(circuit.num_qubits)]
    circuit.custom_operations.extend(initial_operations)

def handle_operation(qir_generator, op) -> None:
    """Handle a single operation."""
    if isinstance(op, MyMeasure):
        qubit = op.qubit
        target_bit = op.target
        qir_generator.module.measure(qubit, target_bit)
    elif isinstance(op, H):
        qubit = op.qubit
        qir_generator.module.h(qubit)
    elif isinstance(op, X):
        qubit = op.qubit
        qir_generator.module.x(qubit)
    elif isinstance(op, Y):
        qubit = op.qubit
        qir_generator.module.y(qubit)
    elif isinstance(op, Z):
        qubit = op.qubit
        qir_generator.module.z(qubit)
    else:
        raise ValueError(f"Operation {op} is not supported.")

def qd_to_qir(
    circ: MyQuantumCircuit,
    name: str = "Generated from input qadence circuit",
    qir_format: QIRFormat = QIRFormat.BINARY,
    int_type: int = 64,
) -> Union[str, bytes]:
    """Convert a given Qadence circuit to QIR."""
    # Create a QdToQirModule instance
    context = ...  # Initialize your context object here
    m = QdToQirModule(
        name=name,
        num_qubits=circ.num_qubits,
        num_results=circ.num_qubits,
        context=context,  # Pass the context object here
    )

    # Create a QirGenerator instance
    qir_generator = QirGenerator(circuit=circ, module=m, qir_int_type=int_type)

    # Add initial operations
    generate_initial_operations(circ)

    # Iterate through the circuit and handle operations
    for op in circ.ops:
        handle_operation(qir_generator, op)

    # Generate the QIR
    populated_module = qir_generator.circuit_to_module(
        qir_generator.circuit, qir_generator.module, True
    )

    if qir_format == QIRFormat.BINARY:
        return populated_module.module.bitcode()
    elif qir_format == QIRFormat.STRING:
        return populated_module.module.get_ir()

    qir = f"Generated QIR from {name}"
    return qir

if __name__ == "__main__":
    try:
        num_qubits = 3  # Number of qubits

        # Create a custom QuantumCircuit subclass with initial operations
        circuit = MyQuantumCircuit(num_qubits)

        # Create a custom measurement operation
        my_measure = MyMeasure(0, 0)

        # Add the custom measurement operation to the circuit
        circuit.add_custom_operation(my_measure)

        print("Starting QIR generation...")

        # Generate QIR
        qir = qd_to_qir(circ=circuit, qir_format=QIRFormat.STRING)

        print("QIR generation complete.")
        print(qir)
    except Exception as e:
        print("An error occurred:", e)

