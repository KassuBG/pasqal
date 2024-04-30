from __future__ import annotations
from qadence.types import OpType

from dataclasses import dataclass
from enum import Enum
from string import Template
from typing import Any

from qadence import H
from qadence.types import OpName


class FuncNat(Enum):
    QIS = "qis"
    CIS = "cis"
    HYBRID = "hybrid"
    RT = "rt"


class FuncName(Enum):
    H = "h"
    X = "x"
    Y = "y"
    Z = "z"
    S = "s"
    T = "t"
    RESET = "reset"
    CNOT = "cnot"
    CX = "cx"
    CZ = "cz"
    MEASURE = "m"
    MEASUREZ = "mz"
    Rx = "rx"
    Ry = "ry"
    Rz = "rz"
    PHASEDX = "u1q"
    ZZPHASE = "rzz"
    ZZMAX = "zz"
    AND = "and"
    OR = "or"
    XOR = "xor"
    INT = "integer"
    BOOL = "bool"
    RES = "result"
    READ_RES = "read_result"


class FuncSpec(Enum):
    BODY = "body"
    ADJ = "adj"
    CTL = "ctl"
    CTLADJ = "ctladj"
    REC_OUT = "record_output"


@dataclass(frozen=True)
class QirGate:
    func_nat: FuncNat
    func_name: FuncName
    func_spec: FuncSpec


@dataclass(frozen=True)
class CustomQirGate(QirGate):
    function_signature: list
    return_type: Any


@dataclass(frozen=True)
class CustomGateSet:
    name: str
    template: Template
    base_gateset: set
    gateset: dict[str, CustomQirGate]
    qd_to_gateset: callable


_QD_TO_PYQIR = {
    OpName.H: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.H, func_spec=FuncSpec.BODY
    ),
    OpType.X: QirGate(
         func_nat=FuncNat.QIS, func_name=FuncName.X, func_spec=FuncSpec.BODY
     ),
    OpType.Y: QirGate(
         func_nat=FuncNat.QIS, func_name=FuncName.Y, func_spec=FuncSpec.BODY
     ),
     OpType.Z: QirGate(
         func_nat=FuncNat.QIS, func_name=FuncName.Z, func_spec=FuncSpec.BODY
     ),
    OpType.S: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.S, func_spec=FuncSpec.BODY
    ),
    OpType.Sdg: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.S, func_spec=FuncSpec.ADJ
    ),
    OpType.T: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.T, func_spec=FuncSpec.BODY
    ),
    OpType.Tdg: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.T, func_spec=FuncSpec.ADJ
    ),
    OpType.Reset: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.RESET, func_spec=FuncSpec.BODY
    ),
    OpType.CX: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.CX, func_spec=FuncSpec.BODY
    ),
    OpType.CZ: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.CZ, func_spec=FuncSpec.BODY
    ),
    OpType.Measure: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.MEASUREZ, func_spec=FuncSpec.BODY
    ),
    OpType.Rx: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.Rx, func_spec=FuncSpec.BODY
    ),
    OpType.Ry: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.Ry, func_spec=FuncSpec.BODY
    ),
    OpType.Rz: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.Rz, func_spec=FuncSpec.BODY
    ),
    OpType.CopyBits: QirGate(
        func_nat=FuncNat.QIS, func_name=FuncName.READ_RES, func_spec=FuncSpec.BODY
    ),
}


PYQIR_GATES = CustomGateSet(
    name="PyQir",
    template=Template("__quantum__${func_nat}__${func_name}__${func_spec}"),
    base_gateset=set(_QD_TO_PYQIR.keys()),
    gateset={},
    qd_to_gateset=lambda gate: _QD_TO_PYQIR[gate],
)

