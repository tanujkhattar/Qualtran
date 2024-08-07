#  Copyright 2023 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Dict

import cirq
import numpy as np
import pytest
from attrs import frozen
from numpy.typing import NDArray

from qualtran import Bloq, BloqBuilder, QAny, QBit, Register, Side, Signature, Soquet
from qualtran.bloqs.basic_gates import CNOT
from qualtran.simulation.classical_sim import (
    _update_assign_from_vals,
    bits_to_ints,
    call_cbloq_classically,
    ClassicalValT,
    ints_to_bits,
)
from qualtran.testing import execute_notebook


def test_bits_to_int():
    rs = np.random.RandomState(52)
    bitstrings = rs.choice([0, 1], size=(100, 23))

    nums = bits_to_ints(bitstrings)
    assert nums.dtype == np.uint64
    assert nums.shape == (100,)

    for num, bs in zip(nums, bitstrings):
        ref_num = cirq.big_endian_bits_to_int(bs.tolist())
        assert num == ref_num

    # check one input bitstring instead of array of input bitstrings.
    (num,) = bits_to_ints([1, 0])
    assert num == 2


def test_int_to_bits():
    rs = np.random.RandomState(52)
    nums = rs.randint(0, 2**23 - 1, size=(100,), dtype=np.uint64)
    bitstrings = ints_to_bits(nums, w=23)
    assert bitstrings.shape == (100, 23)

    nums = rs.randint(-(2**22), 2**22, size=(100,), dtype=np.int64)
    bitstrings = ints_to_bits(nums, w=23)
    assert bitstrings.shape == (100, 23)

    for num, bs in zip(nums, bitstrings):
        ref_bs = cirq.big_endian_int_to_bits(int(num), bit_count=23)
        np.testing.assert_array_equal(ref_bs, bs)

    # check one input int
    (bitstring,) = ints_to_bits(2, w=8)
    assert bitstring.tolist() == [0, 0, 0, 0, 0, 0, 1, 0]

    bitstring = ints_to_bits([31, -1], w=6)
    assert bitstring.tolist() == [[0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]


def test_dtype_validation():
    # set up mocks for `_update_assign_from_vals`
    soq_assign: Dict[Soquet, ClassicalValT] = {}  # gets assigned to; we discard in this test.
    binst = 'MyBinst'  # binst is only used for error messages, so we can mock with a string

    # set up different register dtypes
    regs = [
        Register('one_bit_int', QBit()),
        Register('int', QAny(5)),
        Register('bit_arr', QBit(), shape=(5,)),
        Register('int_arr', QAny(32), shape=(5,)),
    ]

    # base case: vals are as-expected.
    vals = {
        'one_bit_int': 1,
        'int': 5,
        'bit_arr': np.array([1, 0, 1, 0, 1], dtype=np.uint8),
        'int_arr': np.arange(5),
    }
    _update_assign_from_vals(regs, binst, vals, soq_assign)  # type: ignore[arg-type]

    # bad integer
    vals2 = {**vals, 'one_bit_int': 2}
    with pytest.raises(ValueError, match=r'Bad QBit().*one_bit_int'):
        _update_assign_from_vals(regs, binst, vals2, soq_assign)  # type: ignore[arg-type]

    # int is a numpy int
    vals3 = {**vals, 'int': np.arange(5, dtype=np.uint8)[4]}
    _update_assign_from_vals(regs, binst, vals3, soq_assign)  # type: ignore[arg-type]

    # wrong shape
    vals4 = {**vals, 'int_arr': np.arange(6)}
    with pytest.raises(ValueError, match=r'Incorrect shape.*Want \(5,\)\.'):
        _update_assign_from_vals(regs, binst, vals4, soq_assign)  # type: ignore[arg-type]


@frozen
class ApplyClassicalTest(Bloq):
    @property
    def signature(self) -> 'Signature':
        return Signature(
            [Register('x', QBit(), shape=(5,)), Register('z', QBit(), shape=(5,), side=Side.RIGHT)]
        )

    def on_classical_vals(self, *, x: NDArray[np.uint8]) -> Dict[str, NDArray[np.uint8]]:
        const = np.array([1, 0, 1, 0, 1], dtype=np.uint8)
        z = np.logical_xor(x, const).astype(np.uint8)
        return {'x': x, 'z': z}


def test_apply_classical():
    bloq = ApplyClassicalTest()
    x, z = bloq.call_classically(x=np.zeros(5, dtype=np.uint8))
    np.testing.assert_array_equal(x, np.zeros(5))
    assert not isinstance(x, int)
    assert not isinstance(z, int)
    assert x.dtype == np.uint8
    assert z.dtype == np.uint8
    np.testing.assert_array_equal(z, [1, 0, 1, 0, 1])

    x2, z2 = bloq.call_classically(x=np.ones(5, dtype=np.uint8))
    assert not isinstance(x2, int)
    assert not isinstance(z2, int)
    assert x2.dtype == np.uint8
    assert z2.dtype == np.uint8
    np.testing.assert_array_equal(x2, np.ones(5))
    np.testing.assert_array_equal(z2, [0, 1, 0, 1, 0])


def test_cnot_assign_dict():
    cbloq = CNOT().as_composite_bloq()
    binst_graph = cbloq._binst_graph  # pylint: disable=protected-access
    vals = dict(ctrl=1, target=0)
    out_vals, soq_assign = call_cbloq_classically(cbloq.signature, vals, binst_graph)
    assert out_vals == {'ctrl': 1, 'target': 1}
    # left-dangle, regs, right-dangle
    assert len(soq_assign) == 2 + 2 + 2
    for soq in cbloq.all_soquets:
        assert soq in soq_assign.keys()


def test_apply_classical_cbloq():
    bb = BloqBuilder()
    x = bb.add_register(Register('x', QBit(), shape=(5,)))
    assert x is not None
    x, y = bb.add(ApplyClassicalTest(), x=x)
    y, z = bb.add(ApplyClassicalTest(), x=y)
    cbloq = bb.finalize(x=x, y=y, z=z)

    xarr = np.zeros(5, dtype=np.intc)
    x, y, z = cbloq.call_classically(x=xarr)
    np.testing.assert_array_equal(x, xarr)
    np.testing.assert_array_equal(y, [1, 0, 1, 0, 1])
    np.testing.assert_array_equal(z, xarr)


@pytest.mark.notebook
def test_notebook():
    execute_notebook('classical_sim')
