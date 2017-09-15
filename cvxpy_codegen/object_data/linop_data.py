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

from cvxpy_codegen.atoms import get_atom_data, get_coeff_data
from cvxpy_codegen.object_data.expr_data import ExprData
from cvxpy_codegen.object_data.const_data import CONST_ID
from cvxpy_codegen.utils.utils import spzeros # TODO rm
import scipy.sparse as sp
from cvxpy_codegen.object_data.linop_coeff_data import LinOpCoeffData
from cvxpy_codegen.utils.utils import Counter

LINOP_COUNT = Counter()




class LinOpData(ExprData):
    def __init__(self, expr, arg_data):
        ExprData.__init__(self, expr, arg_data)
        self.type = 'linop'
        self.opname = type(expr)
        self.name = 'linop%d' % LINOP_COUNT.get_count()
        self.data = expr.get_data()
        self.args = arg_data
        self.coeffs = dict()
        self.var_ids = set().union(*[a.var_ids for a in arg_data])
        if any([a.has_offset for a in arg_data]):
            self.has_offset = True 
        else:
            self.has_offset = False

        # Get the coefficient for each variable.
        for vid in self.var_ids:
            coeff_args = []
            for arg in self.args:
                if vid in arg.var_ids:
                    if isinstance(arg, LinOpData):
                        coeff_args += [arg.coeffs[vid]]
                    else:
                        coeff_args += [arg]
            coeff = get_coeff_data(self, coeff_args, vid) 
            self.coeffs.update({vid : coeff})

        # Get the expression for the offset vector.
        arg_count = 0
        arg_pos = [] # Store the argument positions.
        if self.has_offset:
            offset_args = []
            for arg in self.args:
                if arg.has_offset:
                    arg_pos += [arg_count]
                    if isinstance(arg, LinOpData):
                        offset_args += [arg.offset_expr]
                    else:
                        offset_args += [arg]
                arg_count += 1
            self.offset_expr = get_atom_data(expr, offset_args, arg_pos)


    def get_data(self):
        return self.data



    def force_copy(self):
        for c in self.coeffs:
            c.force_copy()


    def get_matrix(self, x_length, var_offsets):
        coeff_height = self.shape[0] * self.shape[1]
        mat = sp.csc_matrix((coeff_height, x_length), dtype=bool)
        for vid, coeff in self.coeffs.items():
            if not (vid == CONST_ID):
                start = var_offsets[vid]
                coeff_width = coeff.sparsity.shape[1]
                pad_left = start
                pad_right = x_length - coeff_width - pad_left
                #print sp.csc_matrix((coeff_height, pad_left), dtype=bool).shape
                #print coeff.sparsity.shape
                #print sp.csc_matrix((coeff_height, pad_right), dtype=bool).shape

                #print coeff.shape
                #print coeff.sparsity.shape
                #print coeff.args[0].macro_name
                #print coeff.args[0].shape
                #print coeff.args[0].sparsity.shape
                #print coeff.args[0].args[0].macro_name
                #print coeff.args[0].args[0].shape
                #print coeff.args[0].args[0].sparsity.shape
                #print coeff.args[0].args[0].args[0].macro_name
                #print coeff.args[0].args[0].args[0].shape
                #print coeff.args[0].args[0].args[0].sparsity.shape
                mat += sp.hstack([sp.csc_matrix((coeff_height, pad_left), dtype=bool),
                                  coeff.sparsity,
                                  sp.csc_matrix((coeff_height, pad_right), dtype=bool)])
        return mat
