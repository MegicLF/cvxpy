"""
Copyright 2017 Robin Verschueren

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np

from cvxpy.tests.base_test import BaseTest
from cvxpy.problems.problem import Problem
from cvxpy.problems.objective import Minimize
from cvxpy.atoms.quad_form import QuadForm
from cvxpy.expressions.variables.variable import Variable
from cvxpy.problems.problem_analyzer import ProblemAnalyzer
from cvxpy.constraints import NonPos
from cvxpy.reductions.qp2quad_form.qp2symbolic_qp import Qp2SymbolicQp


class TestProblemAnalyzer(BaseTest):
    """Unit tests for problem analysis and reduction path construction"""

    def setUp(self):
        self.x = Variable(2, name='x')
        Q = np.eye(2)
        self.problem = Problem(Minimize(QuadForm(self.x, Q)), [self.x <= -1])

    def test_quadratic_program(self):
        pa = ProblemAnalyzer(self.problem)
        self.assertEquals(True, (Minimize, 'is_quadratic') in pa.type)
        self.assertEquals(True, (NonPos, 'is_affine') in pa.type)

    def test_quadratic_program_reduction(self):
        self.assertEquals(True, Qp2SymbolicQp().accepts(self.problem))
