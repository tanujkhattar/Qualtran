#  Copyright 2024 Google LLC
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
import abc
from functools import cached_property
from typing import Dict

import attrs

from qualtran import Bloq, QFxp, Register, Signature
from qualtran.bloqs.basic_gates import Hadamard, OnEach
from qualtran.symbolics import ceil, log2, pi, SymbolicFloat, SymbolicInt


@attrs.frozen
class QPEWindowStateBase(Bloq, metaclass=abc.ABCMeta):
    """Base class to construct window states"""

    @cached_property
    def m_register(self) -> 'Register':
        return Register('qpe_reg', QFxp(self.m_bits, self.m_bits))

    @property
    @abc.abstractmethod
    def m_bits(self) -> SymbolicInt:
        ...


@attrs.frozen
class RectangularWindowState(QPEWindowStateBase):
    """Window state used in Textbook version of QPE."""

    bitsize: SymbolicInt

    @property
    def m_bits(self) -> SymbolicInt:
        return self.bitsize

    @cached_property
    def signature(self) -> 'Signature':
        return Signature([self.m_register])

    @classmethod
    def from_precision_and_delta(cls, precision: SymbolicInt, delta: SymbolicFloat):
        r"""Estimate $\varphi$ to $precision$ bits with $1-\delta$ success probability.

        Uses Eq 5.35 from Neilson and Chuang to estimate the size of phase register s.t. we can
        estimate the phase $\varphi$ to $precision$ bits of accuracy with probability at least
        $1 - \delta$. See the class docstring for more details.

        ```
            m = n + ceil(log2(2 + 1/(2*delta)))
        ```

        Args:
            precision: Number of bits of precision
            delta: Probability of success.
        """
        return cls(precision + ceil(log2(2 + 1 / (2 * delta))))

    @classmethod
    def from_standard_deviation_eps(cls, eps: SymbolicFloat):
        r"""Estimate the phase $\phi$ with uncertainty in standard deviation bounded by $\epsilon$.

        The standard deviation of textbook phase estimation scales as $\frac{2\pi}{\sqrt{2^{m}}}$.
        This bound can be used to estimate the size of the phase register s.t. the estimated phase
        has a standard deviation of at-most $\epsilon$. See the class docstring for more details.

        ```
            m = ceil(2*log2(pi/eps))
        ```

        Args:
            unitary: Unitary operation to obtain phase estimate of.
            eps: Maximum standard deviation of the estimated phase.
        """
        return cls(ceil(2 * log2(pi(eps) / eps)))

    def build_composite_bloq(
        self, bb: 'BloqBuilder', *, qpe_reg: 'SoquetT'
    ) -> Dict[str, 'SoquetT']:
        qpe_reg = bb.add(OnEach(self.m_bits, Hadamard()), q=qpe_reg)
        return {'qpe_reg': qpe_reg}
