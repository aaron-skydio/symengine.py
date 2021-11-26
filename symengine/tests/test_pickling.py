from symengine import symbols, sin, sinh, have_numpy, have_llvm, cos
import pickle
import unittest


def test_basic():
    x, y, z = symbols('x y z')
    expr = sin(cos(x + y)/z)**2
    s = pickle.dumps(expr)
    expr2 = pickle.loads(s)
    assert expr == expr2


@unittest.skipUnless(have_llvm, "No LLVM support")
@unittest.skipUnless(have_numpy, "Numpy not installed")
def test_llvm_double():
    import numpy as np
    from symengine import Lambdify
    args = x, y, z = symbols('x y z')
    expr = sin(sinh(x+y) + z)
    l = Lambdify(args, expr, cse=True, backend='llvm')
    ss = pickle.dumps(l)
    ll = pickle.loads(ss)
    inp = [1, 2, 3]
    assert np.allclose(l(inp), ll(inp))

