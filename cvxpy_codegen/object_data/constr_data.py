"""
Copyright 2017 Nicholas Moehle

This file is part of CVXPY-CODEGEN.

CVXPY-CODEGEN is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY-CODEGEN is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY-CODEGEN.  If not, see <http://www.gnu.org/licenses/>.
"""

from cvxpy_codegen.utils.utils import Counter
import scipy.sparse as sp

CONSTR_COUNT = Counter()


class ConstrData():
    
    def __init__(self, constr, exprs, vert_offset):
        self.name = 'constr%d' % CONSTR_COUNT.get_count()
        self.exprs = exprs
        # self.shape = exprs[0].shape[0] * exprs[0].shape[1] # TODO generalize
        self.vert_offset = vert_offset
        self.constr = constr

    def get_matrix(self, x_length, var_offsets):
        return self.exprs[0].get_matrix(x_length, var_offsets) # TODO horribly wrong


class ZeroData(ConstrData):
    def __init__(self, constr, exprs, vert_offset):
        ConstrData.__init__(self, constr, exprs, vert_offset)


class NonPosData(ConstrData):
    def __init__(self, constr, exprs, vert_offset):
        ConstrData.__init__(self, constr, exprs, vert_offset)


class SocData(ConstrData):
    def __init__(self, constr, exprs, vert_offset):
        ConstrData.__init__(self, constr, exprs, vert_offset)


class ExpConeData(ConstrData):
    def __init__(self, constr, exprs, vert_offset):
        ConstrData.__init__(self, constr, exprs, vert_offset)
