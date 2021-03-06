"""Test whether all elements of cls.args are instances of Basic. """

# NOTE: keep tests sorted by (module, class name) key. If a class can't
# be instantiated, add it here anyway with @SKIP("abstract class) (see
# e.g. Function).

from __future__ import with_statement

import os
import re

from sympy import Basic, symbols, sqrt, sin
from sympy.utilities.pytest import XFAIL, SKIP

x, y, z = symbols('x,y,z')

def test_all_classes_are_tested():
    this = os.path.split(__file__)[0]
    path = os.path.join(this, os.pardir, os.pardir)
    sympy_path = os.path.abspath(path)
    prefix = os.path.split(sympy_path)[0] + os.sep

    re_cls = re.compile("^class ([A-Za-z][A-Za-z0-9_]*)\s*\(", re.MULTILINE)

    modules = {}

    for root, dirs, files in os.walk(sympy_path):
        module = root.replace(prefix, "").replace(os.sep, ".")

        for file in files:
            if file.startswith(("_", "test_", "bench_")):
                continue
            if not file.endswith(".py"):
                continue

            with open(os.path.join(root, file), "r") as f:
                text = f.read()

            submodule = module + '.' + file[:-3]
            names = re_cls.findall(text)

            if not names:
                continue

            try:
                mod = __import__(submodule, fromlist=names)
            except ImportError:
                continue

            def is_Basic(name):
                cls = getattr(mod, name)
                return issubclass(cls, Basic)

            names = filter(is_Basic, names)

            if names:
                modules[submodule] = names

    ns = globals()
    failed = []

    for module, names in modules.iteritems():
        mod = module.replace('.', '__')

        for name in names:
            test = 'test_' + mod + '__' + name

            if test not in ns:
                failed.append(module + '.' + name)

    assert not failed, "Missing classes: %s" % ", ".join(failed)

def _test_args(obj):
    return all(isinstance(arg, Basic) for arg in obj.args)

@XFAIL
def test_sympy__assumptions__assume__AppliedPredicate():
    from sympy.assumptions.assume import AppliedPredicate, Predicate
    assert _test_args(AppliedPredicate(Predicate("test"), 2))

def test_sympy__assumptions__assume__Predicate():
    from sympy.assumptions.assume import Predicate
    assert _test_args(Predicate("test"))

@XFAIL
def test_sympy__combinatorics__graycode__GrayCode():
    from sympy.combinatorics.graycode import GrayCode
    # an integer is given and returned from GrayCode as the arg
    assert _test_args(GrayCode(3, start='100'))
    assert _test_args(GrayCode(3, rank=1))

def test_sympy__combinatorics__subsets__Subset():
    from sympy.combinatorics.subsets import Subset
    assert _test_args(Subset([0, 1], [0, 1, 2, 3]))
    assert _test_args(Subset(['c','d'], ['a','b','c','d']))

@XFAIL
def test_sympy__combinatorics__permutations__Permutation():
    from sympy.combinatorics.permutations import Permutation
    assert _test_args(Permutation([0, 1, 2, 3]))

@XFAIL
def test_sympy__combinatorics__prufer__Prufer():
    from sympy.combinatorics.prufer import Prufer
    assert _test_args(Prufer([[0, 1], [0, 2], [0, 3]], 4))

def test_sympy__concrete__products__Product():
    from sympy.concrete.products import Product
    assert _test_args(Product(x, (x, 0, 10)))

def test_sympy__concrete__summations__Sum():
    from sympy.concrete.summations import Sum
    assert _test_args(Sum(x, (x, 0, 10)))

def test_sympy__core__add__Add():
    from sympy.core.add import Add
    assert _test_args(Add(x, y, z, 2))

def test_sympy__core__basic__Atom():
    from sympy.core.basic import Atom
    assert _test_args(Atom())

def test_sympy__core__basic__Basic():
    from sympy.core.basic import Basic
    assert _test_args(Basic())

def test_sympy__core__containers__Dict():
    from sympy.core.containers import Dict
    assert _test_args(Dict({x: y, y: z}))

def test_sympy__core__containers__Tuple():
    from sympy.core.containers import Tuple
    assert _test_args(Tuple(x, y, z, 2))

def test_sympy__core__expr__AtomicExpr():
    from sympy.core.expr import AtomicExpr
    assert _test_args(AtomicExpr())

def test_sympy__core__expr__Expr():
    from sympy.core.expr import Expr
    assert _test_args(Expr())

def test_sympy__core__function__Application():
    from sympy.core.function import Application
    assert _test_args(Application(1, 2, 3))

def test_sympy__core__function__AppliedUndef():
    from sympy.core.function import AppliedUndef
    assert _test_args(AppliedUndef(1, 2, 3))

def test_sympy__core__function__Derivative():
    from sympy.core.function import Derivative
    assert _test_args(Derivative(2, x, y, 3))

@SKIP("abstract class")
def test_sympy__core__function__Function():
    pass

def test_sympy__core__function__Lambda():
    from sympy.core.function import Lambda
    assert _test_args(Lambda((x, y), x + y + z))

def test_sympy__core__function__Subs():
    from sympy.core.function import Subs
    assert _test_args(Subs(x + y, x, 2))

def test_sympy__core__function__WildFunction():
    from sympy.core.function import WildFunction
    assert _test_args(WildFunction('f'))

def test_sympy__core__mod__Mod():
    from sympy.core.mod import Mod
    assert _test_args(Mod(x, 2))

def test_sympy__core__mul__Mul():
    from sympy.core.mul import Mul
    assert _test_args(Mul(2, x, y, z))

def test_sympy__core__numbers__Catalan():
    from sympy.core.numbers import Catalan
    assert _test_args(Catalan())

def test_sympy__core__numbers__ComplexInfinity():
    from sympy.core.numbers import ComplexInfinity
    assert _test_args(ComplexInfinity())

def test_sympy__core__numbers__EulerGamma():
    from sympy.core.numbers import EulerGamma
    assert _test_args(EulerGamma())

def test_sympy__core__numbers__Exp1():
    from sympy.core.numbers import Exp1
    assert _test_args(Exp1())

def test_sympy__core__numbers__Float():
    from sympy.core.numbers import Float
    assert _test_args(Float(1.23))

def test_sympy__core__numbers__GoldenRatio():
    from sympy.core.numbers import GoldenRatio
    assert _test_args(GoldenRatio())

def test_sympy__core__numbers__Half():
    from sympy.core.numbers import Half
    assert _test_args(Half())

def test_sympy__core__numbers__ImaginaryUnit():
    from sympy.core.numbers import ImaginaryUnit
    assert _test_args(ImaginaryUnit())

def test_sympy__core__numbers__Infinity():
    from sympy.core.numbers import Infinity
    assert _test_args(Infinity())

def test_sympy__core__numbers__Integer():
    from sympy.core.numbers import Integer
    assert _test_args(Integer(7))

@SKIP("abstract class")
def test_sympy__core__numbers__IntegerConstant():
    pass

def test_sympy__core__numbers__NaN():
    from sympy.core.numbers import NaN
    assert _test_args(NaN())

def test_sympy__core__numbers__NegativeInfinity():
    from sympy.core.numbers import NegativeInfinity
    assert _test_args(NegativeInfinity())

def test_sympy__core__numbers__NegativeOne():
    from sympy.core.numbers import NegativeOne
    assert _test_args(NegativeOne())

def test_sympy__core__numbers__Number():
    from sympy.core.numbers import Number
    assert _test_args(Number(1, 7))

def test_sympy__core__numbers__NumberSymbol():
    from sympy.core.numbers import NumberSymbol
    assert _test_args(NumberSymbol())

def test_sympy__core__numbers__One():
    from sympy.core.numbers import One
    assert _test_args(One())

def test_sympy__core__numbers__Pi():
    from sympy.core.numbers import Pi
    assert _test_args(Pi())

def test_sympy__core__numbers__Rational():
    from sympy.core.numbers import Rational
    assert _test_args(Rational(1, 7))

def test_sympy__core__numbers__RationalConstant():
    from sympy.core.numbers import RationalConstant
    assert _test_args(RationalConstant())

def test_sympy__core__numbers__Zero():
    from sympy.core.numbers import Zero
    assert _test_args(Zero())

@SKIP("abstract class")
def test_sympy__core__operations__AssocOp():
    pass

@SKIP("abstract class")
def test_sympy__core__operations__LatticeOp():
    pass

def test_sympy__core__power__Pow():
    from sympy.core.power import Pow
    assert _test_args(Pow(x, 2))

def test_sympy__core__relational__Equality():
    from sympy.core.relational import Equality
    assert _test_args(Equality(x, 2))

def test_sympy__core__relational__Inequality():
    from sympy.core.relational import Inequality
    assert _test_args(Inequality(x, 2))

@SKIP("abstract class")
def test_sympy__core__relational__Relational():
    pass

def test_sympy__core__relational__StrictInequality():
    from sympy.core.relational import StrictInequality
    assert _test_args(StrictInequality(x, 2))

def test_sympy__core__relational__Unequality():
    from sympy.core.relational import Unequality
    assert _test_args(Unequality(x, 2))

@XFAIL
def test_sympy__core__sets__CountableSet():
    from sympy.core.sets import CountableSet
    assert _test_args(CountableSet(1, 2, 3))

def test_sympy__core__sets__EmptySet():
    from sympy.core.sets import EmptySet
    assert _test_args(EmptySet())

def test_sympy__core__sets__FiniteSet():
    from sympy.core.sets import FiniteSet
    assert _test_args(FiniteSet(x, y, z))

@XFAIL
def test_sympy__core__sets__Interval():
    from sympy.core.sets import Interval
    assert _test_args(Interval(0, 1))

def test_sympy__core__sets__ProductSet():
    from sympy.core.sets import ProductSet, Interval
    assert _test_args(ProductSet(Interval(0, 1), Interval(0, 1)))

def test_sympy__core__sets__RealFiniteSet():
    from sympy.core.sets import RealFiniteSet
    assert _test_args(RealFiniteSet(1, 2, 3))

@SKIP("does it make sense to test this?")
def test_sympy__core__sets__RealSet():
    from sympy.core.sets import RealSet
    assert _test_args(RealSet())

def test_sympy__core__sets__RealUnion():
    from sympy.core.sets import RealUnion, Interval
    assert _test_args(RealUnion(Interval(0, 1), Interval(2, 3)))

@SKIP("does it make sense to test this?")
def test_sympy__core__sets__Set():
    from sympy.core.sets import Set
    assert _test_args(Set())

def test_sympy__core__sets__Union():
    from sympy.core.sets import Union, Interval
    assert _test_args(Union(Interval(0, 1), Interval(2, 3)))

def test_sympy__core__symbol__Dummy():
    from sympy.core.symbol import Dummy
    assert _test_args(Dummy('t'))

def test_sympy__core__symbol__Symbol():
    from sympy.core.symbol import Symbol
    assert _test_args(Symbol('t'))

def test_sympy__core__symbol__Wild():
    from sympy.core.symbol import Wild
    assert _test_args(Wild('x', exclude=[x]))

@SKIP("abstract class")
def test_sympy__functions__combinatorial__factorials__CombinatorialFunction():
    pass

def test_sympy__functions__combinatorial__factorials__FallingFactorial():
    from sympy.functions.combinatorial.factorials import FallingFactorial
    assert _test_args(FallingFactorial(2, x))

def test_sympy__functions__combinatorial__factorials__MultiFactorial():
    from sympy.functions.combinatorial.factorials import MultiFactorial
    assert _test_args(MultiFactorial(x))

def test_sympy__functions__combinatorial__factorials__RisingFactorial():
    from sympy.functions.combinatorial.factorials import RisingFactorial
    assert _test_args(RisingFactorial(2, x))

def test_sympy__functions__combinatorial__factorials__binomial():
    from sympy.functions.combinatorial.factorials import binomial
    assert _test_args(binomial(2, x))

def test_sympy__functions__combinatorial__factorials__factorial():
    from sympy.functions.combinatorial.factorials import factorial
    assert _test_args(factorial(x))

def test_sympy__functions__combinatorial__factorials__factorial2():
    from sympy.functions.combinatorial.factorials import factorial2
    assert _test_args(factorial2(x))

def test_sympy__functions__combinatorial__numbers__bell():
    from sympy.functions.combinatorial.numbers import bell
    assert _test_args(bell(x, y))

def test_sympy__functions__combinatorial__numbers__bernoulli():
    from sympy.functions.combinatorial.numbers import bernoulli
    assert _test_args(bernoulli(x))

def test_sympy__functions__combinatorial__numbers__catalan():
    from sympy.functions.combinatorial.numbers import catalan
    assert _test_args(catalan(x))

def test_sympy__functions__combinatorial__numbers__euler():
    from sympy.functions.combinatorial.numbers import euler
    assert _test_args(euler(x))

def test_sympy__functions__combinatorial__numbers__fibonacci():
    from sympy.functions.combinatorial.numbers import fibonacci
    assert _test_args(fibonacci(x))

def test_sympy__functions__combinatorial__numbers__harmonic():
    from sympy.functions.combinatorial.numbers import harmonic
    assert _test_args(harmonic(x, 2))

def test_sympy__functions__combinatorial__numbers__lucas():
    from sympy.functions.combinatorial.numbers import lucas
    assert _test_args(lucas(x))

def test_sympy__functions__elementary__complexes__Abs():
    from sympy.functions.elementary.complexes import Abs
    assert _test_args(Abs(x))

def test_sympy__functions__elementary__complexes__arg():
    from sympy.functions.elementary.complexes import arg
    assert _test_args(arg(x))

def test_sympy__functions__elementary__complexes__conjugate():
    from sympy.functions.elementary.complexes import conjugate
    assert _test_args(conjugate(x))

def test_sympy__functions__elementary__complexes__im():
    from sympy.functions.elementary.complexes import im
    assert _test_args(im(x))

def test_sympy__functions__elementary__complexes__re():
    from sympy.functions.elementary.complexes import re
    assert _test_args(re(x))

def test_sympy__functions__elementary__complexes__sign():
    from sympy.functions.elementary.complexes import sign
    assert _test_args(sign(x))

def test_sympy__functions__elementary__exponential__LambertW():
    from sympy.functions.elementary.exponential import LambertW
    assert _test_args(LambertW(2))

def test_sympy__functions__elementary__exponential__exp():
    from sympy.functions.elementary.exponential import exp
    assert _test_args(exp(2))

def test_sympy__functions__elementary__exponential__log():
    from sympy.functions.elementary.exponential import log
    assert _test_args(log(2))

@SKIP("abstract class")
def test_sympy__functions__elementary__hyperbolic__HyperbolicFunction():
    pass

def test_sympy__functions__elementary__hyperbolic__acosh():
    from sympy.functions.elementary.hyperbolic import acosh
    assert _test_args(acosh(2))

def test_sympy__functions__elementary__hyperbolic__acoth():
    from sympy.functions.elementary.hyperbolic import acoth
    assert _test_args(acoth(2))

def test_sympy__functions__elementary__hyperbolic__asinh():
    from sympy.functions.elementary.hyperbolic import asinh
    assert _test_args(asinh(2))

def test_sympy__functions__elementary__hyperbolic__atanh():
    from sympy.functions.elementary.hyperbolic import atanh
    assert _test_args(atanh(2))

def test_sympy__functions__elementary__hyperbolic__cosh():
    from sympy.functions.elementary.hyperbolic import cosh
    assert _test_args(cosh(2))

def test_sympy__functions__elementary__hyperbolic__coth():
    from sympy.functions.elementary.hyperbolic import coth
    assert _test_args(coth(2))

def test_sympy__functions__elementary__hyperbolic__sinh():
    from sympy.functions.elementary.hyperbolic import sinh
    assert _test_args(sinh(2))

def test_sympy__functions__elementary__hyperbolic__tanh():
    from sympy.functions.elementary.hyperbolic import tanh
    assert _test_args(tanh(2))

@SKIP("does this work at all?")
def test_sympy__functions__elementary__integers__RoundFunction():
    from sympy.functions.elementary.integers import RoundFunction
    assert _test_args(RoundFunction())

def test_sympy__functions__elementary__integers__ceiling():
    from sympy.functions.elementary.integers import ceiling
    assert _test_args(ceiling(x))

def test_sympy__functions__elementary__integers__floor():
    from sympy.functions.elementary.integers import floor
    assert _test_args(floor(x))

def test_sympy__functions__elementary__miscellaneous__IdentityFunction():
    from sympy.functions.elementary.miscellaneous import IdentityFunction
    assert _test_args(IdentityFunction())

def test_sympy__functions__elementary__miscellaneous__Max():
    from sympy.functions.elementary.miscellaneous import Max
    assert _test_args(Max(x, 2))

def test_sympy__functions__elementary__miscellaneous__Min():
    from sympy.functions.elementary.miscellaneous import Min
    assert _test_args(Min(x, 2))

@SKIP("abstract class")
def test_sympy__functions__elementary__miscellaneous__MinMaxBase():
    pass

def test_sympy__functions__elementary__piecewise__ExprCondPair():
    from sympy.functions.elementary.piecewise import ExprCondPair
    assert _test_args(ExprCondPair(1, True))

def test_sympy__functions__elementary__piecewise__Piecewise():
    from sympy.functions.elementary.piecewise import Piecewise
    assert _test_args(Piecewise((1, x >= 0), (0, True)))

@SKIP("abstract class")
def test_sympy__functions__elementary__trigonometric__TrigonometricFunction():
    pass

def test_sympy__functions__elementary__trigonometric__acos():
    from sympy.functions.elementary.trigonometric import acos
    assert _test_args(acos(2))

def test_sympy__functions__elementary__trigonometric__acot():
    from sympy.functions.elementary.trigonometric import acot
    assert _test_args(acot(2))

def test_sympy__functions__elementary__trigonometric__asin():
    from sympy.functions.elementary.trigonometric import asin
    assert _test_args(asin(2))

def test_sympy__functions__elementary__trigonometric__atan():
    from sympy.functions.elementary.trigonometric import atan
    assert _test_args(atan(2))

def test_sympy__functions__elementary__trigonometric__atan2():
    from sympy.functions.elementary.trigonometric import atan2
    assert _test_args(atan2(2, 3))

def test_sympy__functions__elementary__trigonometric__cos():
    from sympy.functions.elementary.trigonometric import cos
    assert _test_args(cos(2))

def test_sympy__functions__elementary__trigonometric__cot():
    from sympy.functions.elementary.trigonometric import cot
    assert _test_args(cot(2))

def test_sympy__functions__elementary__trigonometric__sin():
    assert _test_args(sin(2))

def test_sympy__functions__elementary__trigonometric__tan():
    from sympy.functions.elementary.trigonometric import tan
    assert _test_args(tan(2))

@SKIP("abstract class")
def test_sympy__functions__special__bessel__BesselBase():
    pass

@SKIP("abstract class")
def test_sympy__functions__special__bessel__SphericalBesselBase():
    pass

def test_sympy__functions__special__bessel__besseli():
    from sympy.functions.special.bessel import besseli
    assert _test_args(besseli(x, 1))

def test_sympy__functions__special__bessel__besselj():
    from sympy.functions.special.bessel import besselj
    assert _test_args(besselj(x, 1))

def test_sympy__functions__special__bessel__besselk():
    from sympy.functions.special.bessel import besselk
    assert _test_args(besselk(x, 1))

def test_sympy__functions__special__bessel__bessely():
    from sympy.functions.special.bessel import bessely
    assert _test_args(bessely(x, 1))

def test_sympy__functions__special__bessel__hankel1():
    from sympy.functions.special.bessel import hankel1
    assert _test_args(hankel1(x, 1))

def test_sympy__functions__special__bessel__hankel2():
    from sympy.functions.special.bessel import hankel2
    assert _test_args(hankel2(x, 1))

def test_sympy__functions__special__bessel__jn():
    from sympy.functions.special.bessel import jn
    assert _test_args(jn(0, x))

def test_sympy__functions__special__bessel__yn():
    from sympy.functions.special.bessel import yn
    assert _test_args(yn(0, x))

def test_sympy__functions__special__delta_functions__DiracDelta():
    from sympy.functions.special.delta_functions import DiracDelta
    assert _test_args(DiracDelta(x, 1))

def test_sympy__functions__special__delta_functions__Heaviside():
    from sympy.functions.special.delta_functions import Heaviside
    assert _test_args(Heaviside(x))

def test_sympy__functions__special__error_functions__erf():
    from sympy.functions.special.error_functions import erf
    assert _test_args(erf(2))

def test_sympy__functions__special__gamma_functions__gamma():
    from sympy.functions.special.gamma_functions import gamma
    assert _test_args(gamma(x))

def test_sympy__functions__special__gamma_functions__loggamma():
    from sympy.functions.special.gamma_functions import loggamma
    assert _test_args(loggamma(2))

def test_sympy__functions__special__gamma_functions__lowergamma():
    from sympy.functions.special.gamma_functions import lowergamma
    assert _test_args(lowergamma(x, 2))

def test_sympy__functions__special__gamma_functions__polygamma():
    from sympy.functions.special.gamma_functions import polygamma
    assert _test_args(polygamma(x, 2))

def test_sympy__functions__special__gamma_functions__uppergamma():
    from sympy.functions.special.gamma_functions import uppergamma
    assert _test_args(uppergamma(x, 2))

@SKIP("abstract class")
def test_sympy__functions__special__hyper__TupleParametersBase():
    pass

def test_sympy__functions__special__hyper__hyper():
    from sympy.functions.special.hyper import hyper
    assert _test_args(hyper([1, 2, 3], [4, 5], x))

def test_sympy__functions__special__hyper__meijerg():
    from sympy.functions.special.hyper import meijerg
    assert _test_args(meijerg([1, 2, 3], [4, 5], [6], [], x))

@SKIP("abstract class")
def test_sympy__functions__special__polynomials__PolynomialSequence():
    pass

def test_sympy__functions__special__polynomials__assoc_legendre():
    from sympy.functions.special.polynomials import assoc_legendre
    assert _test_args(assoc_legendre(x, 0, y))

def test_sympy__functions__special__polynomials__chebyshevt():
    from sympy.functions.special.polynomials import chebyshevt
    assert _test_args(chebyshevt(x, 2))

def test_sympy__functions__special__polynomials__chebyshevt_root():
    from sympy.functions.special.polynomials import chebyshevt_root
    assert _test_args(chebyshevt_root(x, 2))

def test_sympy__functions__special__polynomials__chebyshevu():
    from sympy.functions.special.polynomials import chebyshevu
    assert _test_args(chebyshevu(x, 2))

def test_sympy__functions__special__polynomials__chebyshevu_root():
    from sympy.functions.special.polynomials import chebyshevu_root
    assert _test_args(chebyshevu_root(x, 2))

def test_sympy__functions__special__polynomials__hermite():
    from sympy.functions.special.polynomials import hermite
    assert _test_args(hermite(x, 2))

def test_sympy__functions__special__polynomials__legendre():
    from sympy.functions.special.polynomials import legendre
    assert _test_args(legendre(x, 2))

def test_sympy__functions__special__tensor_functions__LeviCivita():
    from sympy.functions.special.tensor_functions import LeviCivita
    assert _test_args(LeviCivita(x, y, 2))

def test_sympy__functions__special__tensor_functions__KroneckerDelta():
    from sympy.functions.special.tensor_functions import KroneckerDelta
    assert _test_args(KroneckerDelta(x, y))

def test_sympy__functions__special__zeta_functions__dirichlet_eta():
    from sympy.functions.special.zeta_functions import dirichlet_eta
    assert _test_args(dirichlet_eta(x))

def test_sympy__functions__special__zeta_functions__zeta():
    from sympy.functions.special.zeta_functions import zeta
    assert _test_args(zeta(101))

def test_sympy__integrals__integrals__Integral():
    from sympy.integrals.integrals import Integral
    assert _test_args(Integral(2, (x, 0, 1)))

def test_sympy__logic__boolalg__And():
    from sympy.logic.boolalg import And
    assert _test_args(And(x, y, 2))

@SKIP("abstract class")
def test_sympy__logic__boolalg__Boolean():
    pass

def test_sympy__logic__boolalg__BooleanFunction():
    from sympy.logic.boolalg import BooleanFunction
    assert _test_args(BooleanFunction(1, 2, 3))

def test_sympy__logic__boolalg__Equivalent():
    from sympy.logic.boolalg import Equivalent
    assert _test_args(Equivalent(x, 2))

def test_sympy__logic__boolalg__ITE():
    from sympy.logic.boolalg import ITE
    assert _test_args(ITE(x, y, 2))

def test_sympy__logic__boolalg__Implies():
    from sympy.logic.boolalg import Implies
    assert _test_args(Implies(x, 2))

def test_sympy__logic__boolalg__Nand():
    from sympy.logic.boolalg import Nand
    assert _test_args(Nand(x, y, 2))

def test_sympy__logic__boolalg__Nor():
    from sympy.logic.boolalg import Nor
    assert _test_args(Nor(x, y, 2))

def test_sympy__logic__boolalg__Not():
    from sympy.logic.boolalg import Not
    assert _test_args(Not(2))

def test_sympy__logic__boolalg__Or():
    from sympy.logic.boolalg import Or
    assert _test_args(Or(x, y, 2))

def test_sympy__logic__boolalg__Xor():
    from sympy.logic.boolalg import Xor
    assert _test_args(Xor(x, y, 2))

def test_sympy__matrices__expressions__blockmatrix__BlockDiagMatrix():
    from sympy.matrices.expressions.blockmatrix import BlockDiagMatrix
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol('X', x, x)
    Y = MatrixSymbol('Y', y, y)
    assert _test_args(BlockDiagMatrix(X, Y))

def test_sympy__matrices__expressions__blockmatrix__BlockMatrix():
    from sympy.matrices.expressions.blockmatrix import BlockMatrix
    from sympy.matrices.expressions import MatrixSymbol, ZeroMatrix
    X = MatrixSymbol('X', x, x)
    Y = MatrixSymbol('Y', y, y)
    Z = MatrixSymbol('Z', x, y)
    O = ZeroMatrix(y, x)
    assert _test_args(BlockMatrix([[X, Z], [O, Y]]))

def test_sympy__matrices__expressions__inverse__Inverse():
    from sympy.matrices.expressions.inverse import Inverse
    from sympy.matrices.expressions import MatrixSymbol
    assert _test_args(Inverse(MatrixSymbol('A', 3, 3)))

def test_sympy__matrices__expressions__matadd__MatAdd():
    from sympy.matrices.expressions.matadd import MatAdd
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol('X', x, y)
    Y = MatrixSymbol('Y', x, y)
    assert _test_args(MatAdd(X, Y))

@XFAIL
def test_sympy__matrices__expressions__matexpr__Identity():
    from sympy.matrices.expressions.matexpr import Identity
    assert _test_args(Identity(3))

@SKIP("abstract class")
def test_sympy__matrices__expressions__matexpr__MatrixExpr():
    pass

@XFAIL
def test_sympy__matrices__expressions__matexpr__MatrixSymbol():
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    assert _test_args(MatrixSymbol('A', 3, 5))

@XFAIL
def test_sympy__matrices__expressions__matexpr__ZeroMatrix():
    from sympy.matrices.expressions.matexpr import ZeroMatrix
    assert _test_args(ZeroMatrix(3, 5))

def test_sympy__matrices__expressions__matmul__MatMul():
    from sympy.matrices.expressions.matmul import MatMul
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol('X', x, y)
    Y = MatrixSymbol('Y', y, x)
    assert _test_args(MatMul(X, Y))

def test_sympy__matrices__expressions__matpow__MatPow():
    from sympy.matrices.expressions.matpow import MatPow
    from sympy.matrices.expressions import MatrixSymbol
    X = MatrixSymbol('X', x, x)
    assert _test_args(MatPow(X, 2))

def test_sympy__matrices__expressions__transpose__Transpose():
    from sympy.matrices.expressions.transpose import Transpose
    from sympy.matrices.expressions import MatrixSymbol
    assert _test_args(Transpose(MatrixSymbol('A', 3, 5)))

def test_sympy__physics__gaussopt__BeamParameter():
    from sympy.physics.gaussopt import BeamParameter
    assert _test_args(BeamParameter(530e-9, 1, w=1e-3))

def test_sympy__physics__paulialgebra__Pauli():
    from sympy.physics.paulialgebra import Pauli
    assert _test_args(Pauli(1))

def test_sympy__physics__quantum__anticommutator__AntiCommutator():
    from sympy.physics.quantum.anticommutator import AntiCommutator
    assert _test_args(AntiCommutator(x, y))

def test_sympy__physics__quantum__cartesian__PositionBra3D():
    from sympy.physics.quantum.cartesian import PositionBra3D
    assert _test_args(PositionBra3D(x, y, z))

def test_sympy__physics__quantum__cartesian__PositionKet3D():
    from sympy.physics.quantum.cartesian import PositionKet3D
    assert _test_args(PositionKet3D(x, y, z))

def test_sympy__physics__quantum__cartesian__PositionState3D():
    from sympy.physics.quantum.cartesian import PositionState3D
    assert _test_args(PositionState3D(x, y, z))

def test_sympy__physics__quantum__cartesian__PxBra():
    from sympy.physics.quantum.cartesian import PxBra
    assert _test_args(PxBra(x, y, z))

def test_sympy__physics__quantum__cartesian__PxKet():
    from sympy.physics.quantum.cartesian import PxKet
    assert _test_args(PxKet(x, y, z))

def test_sympy__physics__quantum__cartesian__PxOp():
    from sympy.physics.quantum.cartesian import PxOp
    assert _test_args(PxOp(x, y, z))

def test_sympy__physics__quantum__cartesian__XBra():
    from sympy.physics.quantum.cartesian import XBra
    assert _test_args(XBra(x))

def test_sympy__physics__quantum__cartesian__XKet():
    from sympy.physics.quantum.cartesian import XKet
    assert _test_args(XKet(x))

def test_sympy__physics__quantum__cartesian__XOp():
    from sympy.physics.quantum.cartesian import XOp
    assert _test_args(XOp(x))

def test_sympy__physics__quantum__cartesian__YOp():
    from sympy.physics.quantum.cartesian import YOp
    assert _test_args(YOp(x))

def test_sympy__physics__quantum__cartesian__ZOp():
    from sympy.physics.quantum.cartesian import ZOp
    assert _test_args(ZOp(x))

def test_sympy__physics__quantum__cg__CG():
    from sympy.physics.quantum.cg import CG
    from sympy import S
    assert _test_args(CG(S(3)/2, S(3)/2, S(1)/2, -S(1)/2, 1, 1))

def test_sympy__physics__quantum__cg__Wigner3j():
    from sympy.physics.quantum.cg import Wigner3j
    assert _test_args(Wigner3j(6,0,4,0,2,0))

def test_sympy__physics__quantum__commutator__Commutator():
    from sympy.physics.quantum.commutator import Commutator
    A, B = symbols('A,B', commutative=False)
    assert _test_args(Commutator(A, B))

def test_sympy__physics__quantum__constants__HBar():
    from sympy.physics.quantum.constants import HBar
    assert _test_args(HBar())

def test_sympy__physics__quantum__dagger__Dagger():
    from sympy.physics.quantum.dagger import Dagger
    from sympy.physics.quantum.state import Ket
    assert _test_args(Dagger(Dagger(Ket('psi'))))

def test_sympy__physics__quantum__gate__CGate():
    from sympy.physics.quantum.gate import CGate, Gate
    assert _test_args(CGate((0,1), Gate(2)))

def test_sympy__physics__quantum__gate__CNotGate():
    from sympy.physics.quantum.gate import CNotGate
    assert _test_args(CNotGate(0, 1))

def test_sympy__physics__quantum__gate__Gate():
    from sympy.physics.quantum.gate import Gate
    assert _test_args(Gate(0))

def test_sympy__physics__quantum__gate__HadamardGate():
    from sympy.physics.quantum.gate import HadamardGate
    assert _test_args(HadamardGate(0))

def test_sympy__physics__quantum__gate__IdentityGate():
    from sympy.physics.quantum.gate import IdentityGate
    assert _test_args(IdentityGate(0))

def test_sympy__physics__quantum__gate__OneQubitGate():
    from sympy.physics.quantum.gate import OneQubitGate
    assert _test_args(OneQubitGate(0))

def test_sympy__physics__quantum__gate__PhaseGate():
    from sympy.physics.quantum.gate import PhaseGate
    assert _test_args(PhaseGate(0))

def test_sympy__physics__quantum__gate__SwapGate():
    from sympy.physics.quantum.gate import SwapGate
    assert _test_args(SwapGate(0, 1))

def test_sympy__physics__quantum__gate__TGate():
    from sympy.physics.quantum.gate import TGate
    assert _test_args(TGate(0))

def test_sympy__physics__quantum__gate__TwoQubitGate():
    from sympy.physics.quantum.gate import TwoQubitGate
    assert _test_args(TwoQubitGate(0))

@SKIP("TODO: Add ImmutableMatrix Class")
def test_sympy__physics__quantum__gate__UGate():
    from sympy.physics.quantum.gate import UGate
    assert _test_args(UGate())

def test_sympy__physics__quantum__gate__XGate():
    from sympy.physics.quantum.gate import XGate
    assert _test_args(XGate(0))

def test_sympy__physics__quantum__gate__YGate():
    from sympy.physics.quantum.gate import YGate
    assert _test_args(YGate(0))

def test_sympy__physics__quantum__gate__ZGate():
    from sympy.physics.quantum.gate import ZGate
    assert _test_args(ZGate(0))

@SKIP("TODO: sympy.physics")
def test_sympy__physics__quantum__grover__OracleGate():
    from sympy.physics.quantum.grover import OracleGate
    assert _test_args(OracleGate())

def test_sympy__physics__quantum__grover__WGate():
    from sympy.physics.quantum.grover import WGate
    assert _test_args(WGate(1))

def test_sympy__physics__quantum__hilbert__ComplexSpace():
    from sympy.physics.quantum.hilbert import ComplexSpace
    assert _test_args(ComplexSpace(x))

def test_sympy__physics__quantum__hilbert__DirectSumHilbertSpace():
    from sympy.physics.quantum.hilbert import DirectSumHilbertSpace, ComplexSpace, FockSpace
    c = ComplexSpace(2)
    f = FockSpace()
    assert _test_args(DirectSumHilbertSpace(c, f))

def test_sympy__physics__quantum__hilbert__FockSpace():
    from sympy.physics.quantum.hilbert import FockSpace
    assert _test_args(FockSpace())

def test_sympy__physics__quantum__hilbert__HilbertSpace():
    from sympy.physics.quantum.hilbert import HilbertSpace
    assert _test_args(HilbertSpace())

def test_sympy__physics__quantum__hilbert__L2():
    from sympy.physics.quantum.hilbert import L2
    from sympy import oo, Interval
    assert _test_args(L2(Interval(0, oo)))

def test_sympy__physics__quantum__hilbert__TensorPowerHilbertSpace():
    from sympy.physics.quantum.hilbert import TensorPowerHilbertSpace, FockSpace
    f = FockSpace()
    assert _test_args(TensorPowerHilbertSpace(f, 2))

def test_sympy__physics__quantum__hilbert__TensorProductHilbertSpace():
    from sympy.physics.quantum.hilbert import TensorProductHilbertSpace, FockSpace, ComplexSpace
    c = ComplexSpace(2)
    f = FockSpace()
    assert _test_args(TensorProductHilbertSpace(f, c))

def test_sympy__physics__quantum__innerproduct__InnerProduct():
    from sympy.physics.quantum import Bra, Ket, InnerProduct
    b = Bra('b')
    k = Ket('k')
    assert _test_args(InnerProduct(b, k))

def test_sympy__physics__quantum__operator__DifferentialOperator():
    from sympy.physics.quantum.operator import DifferentialOperator
    from sympy import Derivative, Function
    f = Function('f')
    assert _test_args(DifferentialOperator(1/x*Derivative(f(x), x), f(x)))

def test_sympy__physics__quantum__operator__HermitianOperator():
    from sympy.physics.quantum.operator import HermitianOperator
    assert _test_args(HermitianOperator('H'))

def test_sympy__physics__quantum__operator__Operator():
    from sympy.physics.quantum.operator import Operator
    assert _test_args(Operator('A'))

def test_sympy__physics__quantum__operator__OuterProduct():
    from sympy.physics.quantum.operator import OuterProduct
    from sympy.physics.quantum import Ket, Bra
    b = Bra('b')
    k = Ket('k')
    assert _test_args(OuterProduct(k, b))

def test_sympy__physics__quantum__operator__UnitaryOperator():
    from sympy.physics.quantum.operator import UnitaryOperator
    assert _test_args(UnitaryOperator('U'))

def test_sympy__physics__quantum__piab__PIABBra():
    from sympy.physics.quantum.piab import PIABBra
    assert _test_args(PIABBra('B'))

def test_sympy__physics__quantum__piab__PIABHamiltonian():
    from sympy.physics.quantum.piab import PIABHamiltonian
    assert _test_args(PIABHamiltonian('P'))

def test_sympy__physics__quantum__piab__PIABKet():
    from sympy.physics.quantum.piab import PIABKet
    assert _test_args(PIABKet('K'))

def test_sympy__physics__quantum__qexpr__QExpr():
    from sympy.physics.quantum.qexpr import QExpr
    assert _test_args(QExpr(0))

def test_sympy__physics__quantum__qft__Fourier():
    from sympy.physics.quantum.qft import Fourier
    assert _test_args(Fourier(0, 1))

def test_sympy__physics__quantum__qft__IQFT():
    from sympy.physics.quantum.qft import IQFT
    assert _test_args(IQFT(0, 1))

def test_sympy__physics__quantum__qft__QFT():
    from sympy.physics.quantum.qft import QFT
    assert _test_args(QFT(0, 1))

def test_sympy__physics__quantum__qft__RkGate():
    from sympy.physics.quantum.qft import RkGate
    assert _test_args(RkGate(0, 1))

def test_sympy__physics__quantum__qubit__IntQubit():
    from sympy.physics.quantum.qubit import IntQubit
    assert _test_args(IntQubit(0))

def test_sympy__physics__quantum__qubit__IntQubitBra():
    from sympy.physics.quantum.qubit import IntQubitBra
    assert _test_args(IntQubitBra(0))

def test_sympy__physics__quantum__qubit__IntQubitState():
    from sympy.physics.quantum.qubit import IntQubitState, QubitState
    assert _test_args(IntQubitState(QubitState(0, 1)))

def test_sympy__physics__quantum__qubit__Qubit():
    from sympy.physics.quantum.qubit import Qubit
    assert _test_args(Qubit(0, 0, 0))

def test_sympy__physics__quantum__qubit__QubitBra():
    from sympy.physics.quantum.qubit import QubitBra
    assert _test_args(QubitBra('1', 0))

def test_sympy__physics__quantum__qubit__QubitState():
    from sympy.physics.quantum.qubit import QubitState
    assert _test_args(QubitState(0, 1))

@SKIP("TODO: sympy.physics.quantum.shor: Cmod Not Implemented")
def test_sympy__physics__quantum__shor__CMod():
    from sympy.physics.quantum.shor import CMod
    assert _test_args(CMod())

def test_sympy__physics__quantum__spin__CoupledSpinState():
    from sympy.physics.quantum.spin import CoupledSpinState
    assert _test_args(CoupledSpinState(0, 1))

def test_sympy__physics__quantum__spin__J2Op():
    from sympy.physics.quantum.spin import J2Op
    assert _test_args(J2Op(0, 1))

def test_sympy__physics__quantum__spin__JminusOp():
    from sympy.physics.quantum.spin import JminusOp
    assert _test_args(JminusOp(0, 1))

def test_sympy__physics__quantum__spin__JplusOp():
    from sympy.physics.quantum.spin import JplusOp
    assert _test_args(JplusOp(0, 1))

def test_sympy__physics__quantum__spin__JxBra():
    from sympy.physics.quantum.spin import JxBra
    assert _test_args(JxBra(1, 0))

def test_sympy__physics__quantum__spin__JxBraCoupled():
    from sympy.physics.quantum.spin import JxBraCoupled
    assert _test_args(JxBraCoupled(0, 1))

def test_sympy__physics__quantum__spin__JxKet():
    from sympy.physics.quantum.spin import JxKet
    assert _test_args(JxKet(1, 0))

def test_sympy__physics__quantum__spin__JxKetCoupled():
    from sympy.physics.quantum.spin import JxKetCoupled
    assert _test_args(JxKetCoupled(0, 1))

def test_sympy__physics__quantum__spin__JxOp():
    from sympy.physics.quantum.spin import JxOp
    assert _test_args(JxOp(0, 1))

def test_sympy__physics__quantum__spin__JyBra():
    from sympy.physics.quantum.spin import JyBra
    assert _test_args(JyBra(1, 0))

def test_sympy__physics__quantum__spin__JyBraCoupled():
    from sympy.physics.quantum.spin import JyBraCoupled
    assert _test_args(JyBraCoupled(0, 1))

def test_sympy__physics__quantum__spin__JyKet():
    from sympy.physics.quantum.spin import JyKet
    assert _test_args(JyKet(1, 0))

def test_sympy__physics__quantum__spin__JyKetCoupled():
    from sympy.physics.quantum.spin import JyKetCoupled
    assert _test_args(JyKetCoupled(0, 1))

def test_sympy__physics__quantum__spin__JyOp():
    from sympy.physics.quantum.spin import JyOp
    assert _test_args(JyOp(0, 1))

def test_sympy__physics__quantum__spin__JzBra():
    from sympy.physics.quantum.spin import JzBra
    assert _test_args(JzBra(1, 0))

def test_sympy__physics__quantum__spin__JzBraCoupled():
    from sympy.physics.quantum.spin import JzBraCoupled
    assert _test_args(JzBraCoupled(0, 1))

def test_sympy__physics__quantum__spin__JzKet():
    from sympy.physics.quantum.spin import JzKet
    assert _test_args(JzKet(1, 0))

def test_sympy__physics__quantum__spin__JzKetCoupled():
    from sympy.physics.quantum.spin import JzKetCoupled
    assert _test_args(JzKetCoupled(0, 1))

def test_sympy__physics__quantum__spin__JzOp():
    from sympy.physics.quantum.spin import JzOp
    assert _test_args(JzOp(0, 1))

def test_sympy__physics__quantum__spin__Rotation():
    from sympy.physics.quantum.spin import Rotation
    from sympy import pi
    assert _test_args(Rotation(pi, 0, pi/2))

def test_sympy__physics__quantum__spin__SpinState():
    from sympy.physics.quantum.spin import SpinState
    assert _test_args(SpinState(1, 0))

def test_sympy__physics__quantum__spin__WignerD():
    from sympy.physics.quantum.spin import WignerD
    assert _test_args(WignerD(0, 1, 2, 3, 4, 5))

def test_sympy__physics__quantum__state__Bra():
    from sympy.physics.quantum.state import Bra
    assert _test_args(Bra(0))

def test_sympy__physics__quantum__state__BraBase():
    from sympy.physics.quantum.state import BraBase
    assert _test_args(BraBase(0))

def test_sympy__physics__quantum__state__Ket():
    from sympy.physics.quantum.state import Ket
    assert _test_args(Ket(0))

def test_sympy__physics__quantum__state__KetBase():
    from sympy.physics.quantum.state import KetBase
    assert _test_args(KetBase(0))

def test_sympy__physics__quantum__state__State():
    from sympy.physics.quantum.state import State
    assert _test_args(State(0))

def test_sympy__physics__quantum__state__StateBase():
    from sympy.physics.quantum.state import StateBase
    assert _test_args(StateBase(0))

def test_sympy__physics__quantum__state__TimeDepBra():
    from sympy.physics.quantum.state import TimeDepBra
    assert _test_args(TimeDepBra('psi', 't'))

def test_sympy__physics__quantum__state__TimeDepKet():
    from sympy.physics.quantum.state import TimeDepKet
    assert _test_args(TimeDepKet('psi', 't'))

def test_sympy__physics__quantum__state__TimeDepState():
    from sympy.physics.quantum.state import TimeDepState
    assert _test_args(TimeDepState('psi', 't'))

def test_sympy__physics__quantum__state__Wavefunction():
    from sympy.physics.quantum.state import Wavefunction
    from sympy.functions import sin
    from sympy import Piecewise, pi
    n = 1
    L = 1
    g = Piecewise((0, x < 0), (0, x > L), (sqrt(2//L)*sin(n*pi*x/L), True))
    assert _test_args(Wavefunction(g, x))

def test_sympy__physics__quantum__tensorproduct__TensorProduct():
    from sympy.physics.quantum.tensorproduct import TensorProduct
    assert _test_args(TensorProduct(x, y))

def test_sympy__physics__secondquant__AnnihilateBoson():
    from sympy.physics.secondquant import AnnihilateBoson
    assert _test_args(AnnihilateBoson(0))

def test_sympy__physics__secondquant__AnnihilateFermion():
    from sympy.physics.secondquant import AnnihilateFermion
    assert _test_args(AnnihilateFermion(0))

@SKIP("abstract class")
def test_sympy__physics__secondquant__Annihilator():
    pass

def test_sympy__physics__secondquant__AntiSymmetricTensor():
    from sympy.physics.secondquant import AntiSymmetricTensor
    i, j = symbols('i j', below_fermi=True)
    a, b = symbols('a b', above_fermi=True)
    assert _test_args(AntiSymmetricTensor('v', (a, i), (b, j)))

def test_sympy__physics__secondquant__BosonState():
    from sympy.physics.secondquant import BosonState
    assert _test_args(BosonState((0, 1)))

@SKIP("abstract class")
def test_sympy__physics__secondquant__BosonicOperator():
    pass

def test_sympy__physics__secondquant__Commutator():
    from sympy.physics.secondquant import Commutator
    assert _test_args(Commutator(x, y))

def test_sympy__physics__secondquant__CreateBoson():
    from sympy.physics.secondquant import CreateBoson
    assert _test_args(CreateBoson(0))

def test_sympy__physics__secondquant__CreateFermion():
    from sympy.physics.secondquant import CreateFermion
    assert _test_args(CreateFermion(0))

@SKIP("abstract class")
def test_sympy__physics__secondquant__Creator():
    pass

def test_sympy__physics__secondquant__Dagger():
    from sympy.physics.secondquant import Dagger
    from sympy import I
    assert _test_args(Dagger(2*I))

def test_sympy__physics__secondquant__FermionState():
    from sympy.physics.secondquant import FermionState
    assert _test_args(FermionState((0, 1)))

def test_sympy__physics__secondquant__FermionicOperator():
    from sympy.physics.secondquant import FermionicOperator
    assert _test_args(FermionicOperator(0))

def test_sympy__physics__secondquant__FockState():
    from sympy.physics.secondquant import FockState
    assert _test_args(FockState((0, 1)))

def test_sympy__physics__secondquant__FockStateBosonBra():
    from sympy.physics.secondquant import FockStateBosonBra
    assert _test_args(FockStateBosonBra((0, 1)))

def test_sympy__physics__secondquant__FockStateBosonKet():
    from sympy.physics.secondquant import FockStateBosonKet
    assert _test_args(FockStateBosonKet((0, 1)))

def test_sympy__physics__secondquant__FockStateBra():
    from sympy.physics.secondquant import FockStateBra
    assert _test_args(FockStateBra((0, 1)))

def test_sympy__physics__secondquant__FockStateFermionBra():
    from sympy.physics.secondquant import FockStateFermionBra
    assert _test_args(FockStateFermionBra((0, 1)))

def test_sympy__physics__secondquant__FockStateFermionKet():
    from sympy.physics.secondquant import FockStateFermionKet
    assert _test_args(FockStateFermionKet((0, 1)))

def test_sympy__physics__secondquant__FockStateKet():
    from sympy.physics.secondquant import FockStateKet
    assert _test_args(FockStateKet((0, 1)))

def test_sympy__physics__secondquant__InnerProduct():
    from sympy.physics.secondquant import InnerProduct
    from sympy.physics.secondquant import FockStateKet, FockStateBra
    assert _test_args(InnerProduct(FockStateBra((0, 1)), FockStateKet((0, 1))))

def test_sympy__physics__secondquant__NO():
    from sympy.physics.secondquant import NO, F, Fd
    assert _test_args(NO(Fd(x)*F(y)))

def test_sympy__physics__secondquant__PermutationOperator():
    from sympy.physics.secondquant import PermutationOperator
    assert _test_args(PermutationOperator(0, 1))

def test_sympy__physics__secondquant__SqOperator():
    from sympy.physics.secondquant import SqOperator
    assert _test_args(SqOperator(0))

def test_sympy__physics__secondquant__TensorSymbol():
    from sympy.physics.secondquant import TensorSymbol
    assert _test_args(TensorSymbol(x))

def test_sympy__physics__units__Unit():
    from sympy.physics.units import Unit
    assert _test_args(Unit("meter", "m"))

def test_sympy__polys__numberfields__AlgebraicNumber():
    from sympy.polys.numberfields import AlgebraicNumber
    assert _test_args(AlgebraicNumber(sqrt(2), [1, 2, 3]))

def test_sympy__polys__polytools__GroebnerBasis():
    from sympy.polys.polytools import GroebnerBasis
    assert _test_args(GroebnerBasis([x, y, z], x, y, z))

def test_sympy__polys__polytools__Poly():
    from sympy.polys.polytools import Poly
    assert _test_args(Poly(2, x, y))

def test_sympy__polys__polytools__PurePoly():
    from sympy.polys.polytools import PurePoly
    assert _test_args(PurePoly(2, x, y))

def test_sympy__polys__rootoftools__RootOf():
    from sympy.polys.rootoftools import RootOf
    assert _test_args(RootOf(x**3 + x + 1, 0))

def test_sympy__polys__rootoftools__RootSum():
    from sympy.polys.rootoftools import RootSum
    assert _test_args(RootSum(x**3 + x + 1, sin))

def test_sympy__series__limits__Limit():
    from sympy.series.limits import Limit
    assert _test_args(Limit(x, x, 0, dir='-'))

def test_sympy__series__order__Order():
    from sympy.series.order import Order
    assert _test_args(Order(1, x, y))

def test_sympy__simplify__cse_opts__Sub():
    from sympy.simplify.cse_opts import Sub
    assert _test_args(Sub())

def test_sympy__tensor__indexed__Idx():
    from sympy.tensor.indexed import Idx
    assert _test_args(Idx('test'))
    assert _test_args(Idx(1, (0, 10)))

def test_sympy__tensor__indexed__Indexed():
    from sympy.tensor.indexed import Indexed, Idx
    assert _test_args(Indexed('A', Idx('i'), Idx('j')))

def test_sympy__tensor__indexed__IndexedBase():
    from sympy.tensor.indexed import IndexedBase
    assert _test_args(IndexedBase('A', shape=(x, y)))

@XFAIL
def test_as_coeff_add():
    assert (7, (3*x, 4*x**2)) == (7 + 3*x + 4*x**2).as_coeff_add()


