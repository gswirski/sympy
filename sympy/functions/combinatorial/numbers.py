"""
This module implements some special functions that commonly appear in
combinatorial contexts (e.g. in power series); in particular,
sequences of rational numbers such as Bernoulli and Fibonacci numbers.

Factorials, binomial coefficients and related functions are located in
the separate 'factorials' module.
"""

from sympy import Function, S, Symbol, Rational, oo, Integer, C, Add

from sympy.mpmath import bernfrac
from sympy.mpmath.libmp import ifib as _ifib

def _product(a, b):
    p = 1
    for k in xrange(a, b+1):
        p *= k
    return p

from sympy.utilities.memoization import recurrence_memo


# Dummy symbol used for computing polynomial sequences
_sym = Symbol('x')


#----------------------------------------------------------------------------#
#                                                                            #
#                           Fibonacci numbers                                #
#                                                                            #
#----------------------------------------------------------------------------#

class fibonacci(Function):
    """
    Fibonacci numbers / Fibonacci polynomials

    Usage
    =====
        fibonacci(n) gives the nth Fibonacci number, F_n
        fibonacci(n, x) gives the nth Fibonacci polynomial in x, F_n(x)

    Examples
    ========
        >>> from sympy import fibonacci, Symbol

        >>> [fibonacci(x) for x in range(11)]
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        >>> fibonacci(5, Symbol('t'))
        t**4 + 3*t**2 + 1

    Mathematical description
    ========================
        The Fibonacci numbers are the integer sequence defined by the
        initial terms F_0 = 0, F_1 = 1 and the two-term recurrence
        relation F_n = F_{n-1} + F_{n-2}.

        The Fibonacci polynomials are defined by F_1(x) = 1,
        F_2(x) = x, and F_n(x) = x*F_{n-1}(x) + F_{n-2}(x) for n > 2.
        For all positive integers n, F_n(1) = F_n.

    References and further reading
    ==============================
        * http://en.wikipedia.org/wiki/Fibonacci_number
        * http://mathworld.wolfram.com/FibonacciNumber.html

    """

    @staticmethod
    def _fib(n):
        return _ifib(n)

    @staticmethod
    @recurrence_memo([None, S.One, _sym])
    def _fibpoly(n, prev):
        return (prev[-2] + _sym*prev[-1]).expand()

    @classmethod
    def eval(cls, n, sym=None):
        if n.is_Integer:
            n = int(n)
            if n < 0:
                return S.NegativeOne**(n+1) * fibonacci(-n)
            if sym is None:
                return Integer(cls._fib(n))
            else:
                if n < 1:
                    raise ValueError("Fibonacci polynomials are defined "
                       "only for positive integer indices.")
                return cls._fibpoly(n).subs(_sym, sym)

class lucas(Function):
    """
    Lucas numbers

    Usage
    =====
        lucas(n) gives the nth Lucas number

    Examples
    ========
        >>> from sympy import lucas

        >>> [lucas(x) for x in range(11)]
        [2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123]

    Mathematical description
    ========================
        Lucas numbers satisfy a recurrence relation similar to that of
        the Fibonacci sequence, in which each term is the sum of the
        preceding two. They are generated by choosing the initial
        values L_0 = 2 and L_1 = 1.

    References and further reading
    ==============================
        * http://en.wikipedia.org/wiki/Lucas_number

    """

    @classmethod
    def eval(cls, n):
        if n.is_Integer:
            return fibonacci(n+1) + fibonacci(n-1)


#----------------------------------------------------------------------------#
#                                                                            #
#                           Bernoulli numbers                                #
#                                                                            #
#----------------------------------------------------------------------------#

class bernoulli(Function):
    r"""
    Bernoulli numbers / Bernoulli polynomials

    Usage
    =====
        bernoulli(n) gives the nth Bernoulli number, B_n
        bernoulli(n, x) gives the nth Bernoulli polynomial in x, B_n(x)

    Examples
    ========
        >>> from sympy import bernoulli

        >>> [bernoulli(n) for n in range(11)]
        [1, -1/2, 1/6, 0, -1/30, 0, 1/42, 0, -1/30, 0, 5/66]
        >>> bernoulli(1000001)
        0

    Mathematical description
    ========================
        The Bernoulli numbers are a sequence of rational numbers
        defined by B_0 = 1 and the recursive relation (n > 0)

                n
               ___
              \      / n + 1 \
          0 =  )     |       | * B .
              /___   \   k   /    k
              k = 0

        They are also commonly defined by their exponential generating
        function, which is x/(exp(x) - 1). For odd indices > 1, the
        Bernoulli numbers are zero.

        The Bernoulli polynomials satisfy the analogous formula
                    n
                   ___
                  \      / n \         n-k
          B (x) =  )     |   | * B  * x   .
           n      /___   \ k /    k
                  k = 0

        Bernoulli numbers and Bernoulli polynomials are related as
        B_n(0) = B_n.

    Implementation
    ==============
        We compute Bernoulli numbers using Ramanujan's formula

                                   / n + 3 \
          B   =  (A(n) - S(n))  /  |       |
           n                       \   n   /

        where A(n) = (n+3)/3 when n = 0 or 2 (mod 6), A(n) = -(n+3)/6
        when n = 4 (mod 6), and

                 [n/6]
                  ___
                 \      /  n + 3  \
          S(n) =  )     |         | * B
                 /___   \ n - 6*k /    n-6*k
                 k = 1

        This formula is similar to the sum given in the definition, but
        cuts 2/3 of the terms. For Bernoulli polynomials, we use the
        formula in the definition.

    References and further reading
    ==============================
        * http://en.wikipedia.org/wiki/Bernoulli_number
        * http://en.wikipedia.org/wiki/Bernoulli_polynomial
    """

    # Calculates B_n for positive even n
    @staticmethod
    def _calc_bernoulli(n):
        s = 0
        a = int(C.binomial(n+3, n-6))
        for j in xrange(1, n//6+1):
            s += a * bernoulli(n - 6*j)
            # Avoid computing each binomial coefficient from scratch
            a *= _product(n-6 - 6*j + 1, n-6*j)
            a //= _product(6*j+4, 6*j+9)
        if n % 6 == 4:
            s = -Rational(n+3, 6) - s
        else:
            s = Rational(n+3, 3) - s
        return s / C.binomial(n+3, n)

    # We implement a specialized memoization scheme to handle each
    # case modulo 6 separately
    _cache = {0: S.One, 2:Rational(1,6), 4:Rational(-1,30)}
    _highest = {0:0, 2:2, 4:4}

    @classmethod
    def eval(cls, n, sym=None):
        if n.is_Number:
            if n.is_Integer and n.is_nonnegative:
                if n is S.Zero:
                    return S.One
                elif n is S.One:
                    if sym is None: return -S.Half
                    else:           return sym - S.Half
                # Bernoulli numbers
                elif sym is None:
                    if n.is_odd:
                        return S.Zero
                    n = int(n)
                    # Use mpmath for enormous Bernoulli numbers
                    if n > 500:
                        p, q = bernfrac(n)
                        return Rational(int(p), int(q))
                    case = n % 6
                    highest_cached = cls._highest[case]
                    if n <= highest_cached:
                        return cls._cache[n]
                    # To avoid excessive recursion when, say, bernoulli(1000) is
                    # requested, calculate and cache the entire sequence ... B_988,
                    # B_994, B_1000 in increasing order
                    for i in xrange(highest_cached+6, n+6, 6):
                        b = cls._calc_bernoulli(i)
                        cls._cache[i] = b
                        cls._highest[case] = i
                    return b
                # Bernoulli polynomials
                else:
                    n, result = int(n), []
                    for k in xrange(n + 1):
                        result.append(C.binomial(n, k)*cls(k)*sym**(n-k))
                    return Add(*result)
            else:
                raise ValueError("Bernoulli numbers are defined only"
                                 " for nonnegative integer indices.")


#----------------------------------------------------------------------------#
#                                                                            #
#                             Bell numbers                                   #
#                                                                            #
#----------------------------------------------------------------------------#

class bell(Function):
    r"""
    Bell numbers / Bell polynomials

    Usage
    =====
        bell(n) gives the nth Bell number, B_n
        bell(n, x) gives the nth Bell polynomial, B_n(x)

        Not to be confused with Bernoulli numbers and Bernoulli polynomials,
        which use the same notation.

    Examples
    ========
        >>> from sympy import bell, Symbol

        >>> [bell(n) for n in range(11)]
        [1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975]
        >>> bell(30)
        846749014511809332450147
        >>> bell(4, Symbol('t'))
        t**4 + 6*t**3 + 7*t**2 + t

    Mathematical description
    ========================
        The Bell numbers satisfy B_0 = 1 and
                 n-1
                 ___
                \      / n - 1 \
          B   =  )     |       | * B .
           n    /___   \   k   /    k
                k = 0

        They are also given by
                      oo
                     ___    n
                1   \      k
          B   = - *  )     --.
           n    e   /___   k!
                    k = 0

        The Bell polynomials are given by B_0(x) = 1 and
                        n-1
                        ___
                       \      / n - 1 \
          B (x)  = x *  )     |       | * B   (x).
           n           /___   \ k - 1 /    k-1
                       k = 1

    References and further reading
    ==============================
        * http://en.wikipedia.org/wiki/Bell_number
        * http://mathworld.wolfram.com/BellNumber.html
        * http://mathworld.wolfram.com/BellPolynomial.html

    """

    @staticmethod
    @recurrence_memo([1, 1])
    def _bell(n, prev):
        s = 1
        a = 1
        for k in xrange(1, n):
            a = a * (n-k) // k
            s += a * prev[k]
        return s

    @staticmethod
    @recurrence_memo([S.One, _sym])
    def _bell_poly(n, prev):
        s = 1
        a = 1
        for k in xrange(2, n+1):
            a = a * (n-k+1) // (k-1)
            s += a * prev[k-1]
        return (_sym * s).expand()

    @classmethod
    def eval(cls, n, sym=None):
        if n.is_Integer and n.is_nonnegative:
            if sym is None:
                return Integer(cls._bell(int(n)))
            else:
                return cls._bell_poly(int(n)).subs(_sym, sym)

#----------------------------------------------------------------------------#
#                                                                            #
#                           Harmonic numbers                                 #
#                                                                            #
#----------------------------------------------------------------------------#

class harmonic(Function):
    r"""
    Harmonic numbers

    Usage
    =====
        harmonic(n) gives the nth harmonic number, H_n

        harmonic(n, m) gives the nth generalized harmonic number
            of order m, H_{n,m}, where harmonic(n) == harmonic(n, 1)

    Examples
    ========
        >>> from sympy import harmonic, oo

        >>> [harmonic(n) for n in range(6)]
        [0, 1, 3/2, 11/6, 25/12, 137/60]
        >>> [harmonic(n, 2) for n in range(6)]
        [0, 1, 5/4, 49/36, 205/144, 5269/3600]
        >>> harmonic(oo, 2)
        pi**2/6

    Mathematical description
    ========================
        The nth harmonic number is given by 1 + 1/2 + 1/3 + ... + 1/n.
        More generally,
                   n
                  ___
                 \       -m
          H    =  )     k   .
           n,m   /___
                 k = 1

        As n -> oo, H_{n,m} -> zeta(m) (the Riemann zeta function)

    References and further reading
    ==============================
        * http://en.wikipedia.org/wiki/Harmonic_number

    """

    # Generate one memoized Harmonic number-generating function for each
    # order and store it in a dictionary
    _functions = {}

    nargs = (1, 2)

    @classmethod
    def eval(cls, n, m=None):
        if m is None:
            m = S.One
        if n == oo:
            return C.zeta(m)
        if n.is_Integer and n.is_nonnegative and m.is_Integer:
            if n == 0:
                return S.Zero
            if not m in cls._functions:
                @recurrence_memo([0])
                def f(n, prev):
                    return prev[-1] + S.One / n**m
                cls._functions[m] = f
            return cls._functions[m](int(n))

#----------------------------------------------------------------------------#
#                                                                            #
#                           Euler numbers                                    #
#                                                                            #
#----------------------------------------------------------------------------#

class euler(Function):
    r"""
    Euler numbers

    Usage
    =====
        euler(n) gives the n-th Euler number, E_n

    Examples
    ========
        >>> from sympy import euler
        >>> [euler(n) for n in range(10)]
        [1, 0, -1, 0, 5, 0, -61, 0, 1385, 0]
	>>> n = Symbol("n")
	>>> euler(n+2*n)
	euler(3*n)

    Mathematical description
    ========================
        The euler numbers are given by

                  2*n+1   k
                   ___   ___            j          2*n+1
                  \     \     / k \ (-1)  * (k-2*j)
          E   = I  )     )    |   | --------------------
           2n     /___  /___  \ j /      k    k
                  k = 1 j = 0           2  * I  * k

          E     = 0
           2n+1

    References and further reading
    ==============================
        * http://en.wikipedia.org/wiki/Euler_numbers
        * http://mathworld.wolfram.com/EulerNumber.html
	* http://en.wikipedia.org/wiki/Alternating_permutation
        * http://mathworld.wolfram.com/AlternatingPermutation.html
    """

    nargs = 1

    @classmethod
    def eval(cls, m, evaluate=True):
        if not evaluate:
            return
        if m.is_Integer and m.is_nonnegative:
            from sympy.mpmath import mp
            m = m._to_mpmath(mp.prec)
            res = mp.eulernum(m, exact=True)
            return Integer(res)


    def _eval_evalf(self, prec):
        m = self.args[0]

        if m.is_Integer and m.is_nonnegative:
            from sympy.mpmath import mp
            from sympy import Expr
            m = m._to_mpmath(prec)
            oprec = mp.prec
            mp.prec = prec
            res = mp.eulernum(m)
            mp.prec = oprec
            return Expr._from_mpmath(res, prec)
