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

import random
import numpy as np
import pytest
from qualtran.bloqs.controlled_state_preparation import (
    ControlledStatePreparationUsingRotations,
)
from qualtran.drawing import show_bloq
from qualtran import BloqBuilder
from qualtran.bloqs.basic_gates import PlusState, OneEffect, OneState, ZeroEffect, ZeroState
from qualtran.bloqs.rotations.phase_gradient import PhaseGradientState
from qualtran.testing import assert_valid_bloq_decomposition, execute_notebook


def accuracy(state1, state2):
    return abs(np.dot(state1, state2.conj()))


# these states can be approximated exactly with the given rot_reg_size
@pytest.mark.parametrize(
    "n_qubits, rot_reg_size, state_coefs",
    [
        [1, 2, ((-0.5 - 0.5j), (0.5 - 0.5j))],
        [
            1,
            4,
            (
                (-0.8154931568489165 - 0.16221167441072862j),
                (-0.46193976625564304 - 0.30865828381745486j),
            ),
        ],
        [
            3,
            3,
            (
                (-0.42677669529663675 - 0.1767766952966366j),
                (0.17677669529663664 - 0.4267766952966367j),
                (0.17677669529663675 - 0.1767766952966368j),
                (0.07322330470336305 - 0.07322330470336309j),
                (0.4267766952966366 - 0.17677669529663692j),
                (0.42677669529663664 + 0.17677669529663675j),
                (0.0732233047033631 + 0.17677669529663678j),
                (-0.07322330470336308 - 0.17677669529663678j),
            ),
        ],
    ],
)
def test_exact_controlled_state_preparation_via_rotation(
    n_qubits, rot_reg_size, state_coefs
):
    qsp = ControlledStatePreparationUsingRotations(
        n_qubits=n_qubits, rot_reg_size=rot_reg_size, state=tuple(state_coefs)
    )
    assert_valid_bloq_decomposition(qsp)
    bb = BloqBuilder()
    control = bb.add(OneState())
    state = bb.join(np.array([bb.add(ZeroState()) for _ in range(n_qubits)]))
    phase_gradient = bb.add(PhaseGradientState(rot_reg_size))
    control, state, phase_gradient = bb.add(
        qsp, control=control, target_state=state, phase_gradient=phase_gradient
    )
    bb.add(OneEffect(), q=control)
    bb.add(
        PhaseGradientState(bitsize=rot_reg_size, adjoint=True),
        phase_grad=phase_gradient,
    )
    network = bb.finalize(state=state)
    result = network.tensor_contract()
    assert np.isclose(accuracy(result, np.array(state_coefs)), 1)


@pytest.mark.parametrize(
    "n_qubits, rot_reg_size, state_coefs",
    [
        [
            1,
            4,
            (
                (-0.8154931568489165 - 0.16221167441072862j),
                (-0.46193976625564304 - 0.30865828381745486j),
            ),
        ],
        [
            2,
            3,
            (
                (0.3535533905932734 - 0.35355339059327373j),
                (0.3535533905932735 - 0.3535533905932736j),
                (-0.4999999999999997 + 1.1102230246251563e-16j),
                (0.35355339059327356 + 0.35355339059327356j),
            ),
        ],
    ],
)
def test_controlled_state_preparation_via_rotation_adjoint(
    n_qubits, rot_reg_size, state_coefs
):
    qsp = ControlledStatePreparationUsingRotations(
        n_qubits=n_qubits, rot_reg_size=rot_reg_size, state=tuple(state_coefs)
    )
    qsp_adj = ControlledStatePreparationUsingRotations(
        n_qubits=n_qubits,
        rot_reg_size=rot_reg_size,
        state=tuple(state_coefs),
        adjoint=True,
    )

    bb = BloqBuilder()
    control = bb.add(OneState())
    state = bb.join(np.array([bb.add(ZeroState()) for _ in range(n_qubits)]))
    phase_gradient = bb.add(PhaseGradientState(rot_reg_size))
    control, state, phase_gradient = bb.add(
        qsp, control=control, target_state=state, phase_gradient=phase_gradient
    )
    control, state, phase_gradient = bb.add(
        qsp_adj, control=control, target_state=state, phase_gradient=phase_gradient
    )
    bb.add(OneEffect(), q=control)
    bb.add(
        PhaseGradientState(bitsize=rot_reg_size, adjoint=True),
        phase_grad=phase_gradient,
    )
    network = bb.finalize(state=state)
    result = network.tensor_contract()
    assert np.isclose(result[0], 1)  # test that |result> = |0>


#  these states can't be approximated exactly with the given rot_reg_size, check they are close enough
@pytest.mark.parametrize(
    "n_qubits, rot_reg_size, state_coefs",
    [
        [
            1,
            3,
            (
                (0.481145088606368 - 0.47950088720913586j),
                (-0.41617865941997106 - 0.604461434931144j),
            ),
        ],
        [
            2,
            3,
            (
                (-0.45832126811131957 - 0.18416419776558368j),
                (0.17057042949351137 + 0.24581249575498615j),
                (-0.6048757470423172 - 0.5250403822076705j),
                (-0.13534197956156918 - 0.08153272490768977j),
            ),
        ],
    ],
)
def test_approximate_controlled_state_preparation_via_rotation(
    n_qubits, rot_reg_size, state_coefs
):
    qsp = ControlledStatePreparationUsingRotations(
        n_qubits=n_qubits, rot_reg_size=rot_reg_size, state=tuple(state_coefs)
    )
    assert_valid_bloq_decomposition(qsp)
    bb = BloqBuilder()
    control = bb.add(OneState())
    state = bb.join(np.array([bb.add(ZeroState()) for _ in range(n_qubits)]))
    phase_gradient = bb.add(PhaseGradientState(rot_reg_size))
    control, state, phase_gradient = bb.add(
        qsp, control=control, target_state=state, phase_gradient=phase_gradient
    )
    bb.add(OneEffect(), q=control)
    bb.add(
        PhaseGradientState(bitsize=rot_reg_size, adjoint=True),
        phase_grad=phase_gradient,
    )
    network = bb.finalize(state=state)
    result = network.tensor_contract()
    assert accuracy(result, np.array(state_coefs)) >= 0.95


@pytest.mark.parametrize(
    "n_qubits, rot_reg_size, state_coefs",
    [
        [
            2,
            2,
            (
                (-0.45832126811131957 - 0.18416419776558368j),
                (0.17057042949351137 + 0.24581249575498615j),
                (-0.6048757470423172 - 0.5250403822076705j),
                (-0.13534197956156918 - 0.08153272490768977j),
            ),
        ]
    ],
)
def test_controlled_state_preparation_via_rotation_do_not_prepare(
    n_qubits, rot_reg_size, state_coefs
):
    qsp = ControlledStatePreparationUsingRotations(
        n_qubits=n_qubits, rot_reg_size=rot_reg_size, state=tuple(state_coefs)
    )
    assert_valid_bloq_decomposition(qsp)
    bb = BloqBuilder()
    control = bb.add(ZeroState())
    state = bb.join(np.array([bb.add(ZeroState()) for _ in range(n_qubits)]))
    phase_gradient = bb.add(PhaseGradientState(rot_reg_size))
    control, state, phase_gradient = bb.add(
        qsp, control=control, target_state=state, phase_gradient=phase_gradient
    )
    bb.add(ZeroEffect(), q=control)
    bb.add(
        PhaseGradientState(bitsize=rot_reg_size, adjoint=True),
        phase_grad=phase_gradient,
    )
    network = bb.finalize(state=state)
    result = network.tensor_contract()
    assert np.allclose(
        result, np.array([1] + [0] * (2**n_qubits - 1))
    )  # assert result = |0>


@pytest.mark.parametrize(
    "n_qubits, rot_reg_size, state_coefs",
    [[2, 2, ((-0.5 - 0.5j), 0, 0.5, -0.5)]],
)
def test_controlled_state_preparation_via_rotation_superposition_ctrl(
    n_qubits, rot_reg_size, state_coefs
):
    qsp = ControlledStatePreparationUsingRotations(
        n_qubits=n_qubits, rot_reg_size=rot_reg_size, state=tuple(state_coefs)
    )
    assert_valid_bloq_decomposition(qsp)
    bb = BloqBuilder()
    control = bb.add(PlusState())
    state = bb.join(np.array([bb.add(ZeroState()) for _ in range(n_qubits)]))
    phase_gradient = bb.add(PhaseGradientState(rot_reg_size))
    control, state, phase_gradient = bb.add(
        qsp, control=control, target_state=state, phase_gradient=phase_gradient
    )
    bb.add(
        PhaseGradientState(bitsize=rot_reg_size, adjoint=True),
        phase_grad=phase_gradient,
    )
    network = bb.finalize(control=control, state=state)
    result = network.tensor_contract()
    correct = (
        1 / np.sqrt(2) * np.array([1] + [0] * (2**n_qubits - 1) + list(state_coefs))
    )
    # assert result = 1/sqrt(2)*(|0, 0> + |1, state>)
    assert np.allclose(result, correct)


def test_notebook():
    execute_notebook("controlled_state_preparation")