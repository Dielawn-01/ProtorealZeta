"""
nilpotent.py — The ε-Propulsor & Nilradical Calculus

Handles computational tolerances and differentials using the nilradical 
element ε = ι^ω.

Axioms:
    - Definition: ε = ι^ω (where ε ≠ 0)
    - Nilpotency: ε^ν = 0, where ν is the grade of the nilradical ideal.
    - Logarithmic Scaling:
        ω^ε = 1 + ε·ln(ω)
        ω^ι = 1 + ι·ln(ω)
"""

try:
    from sage.all import SR, log, exp
    SAGE_AVAILABLE = True
except ImportError:
    SAGE_AVAILABLE = False
    import math

class NilpotentAlgebra:
    """
    Implements the calculus of the ε-propulsor.
    """
    def __init__(self, grade=3):
        self.grade = grade
        self.epsilon = EpsilonPropulsor(grade=grade)

    def omega_pow_epsilon(self, omega_sym):
        """ω^ε = 1 + ε·ln(ω)"""
        if SAGE_AVAILABLE:
            ln_w = log(omega_sym)
        else:
            ln_w = f"ln({omega_sym})" # Symbolic fallback
        return 1 + self.epsilon * ln_w

    def omega_pow_iota(self, iota_sym, omega_sym):
        """ω^ι = 1 + ι·ln(ω)"""
        if SAGE_AVAILABLE:
            ln_w = log(omega_sym)
        else:
            ln_w = f"ln({omega_sym})"
        return 1 + iota_sym * ln_w

class EpsilonPropulsor:
    """
    The nilradical element ε with ε^ν = 0.
    """
    def __init__(self, coefficient=1, grade=3):
        self.coeff = coefficient
        self.grade = grade

    def __repr__(self):
        if self.coeff == 1: return "ε"
        if self.coeff == -1: return "-ε"
        return f"{self.coeff}ε"

    def __mul__(self, other):
        if isinstance(other, (int, float, str)):
            # Handle scalar or symbolic scaling
            return EpsilonPropulsor(self.coeff * other, self.grade)
        if isinstance(other, EpsilonPropulsor):
            # ε * ε = ε^2, if 2 >= grade, it becomes 0
            # For simplicity in this first version, we just track the power
            # but usually we use this as a first-order differential.
            # If the user wants higher grades, we would return a 'HigherOrderEpsilon'.
            if self.grade <= 2:
                return 0
            # Placeholder for higher order behavior if needed
            return 0 # Defaulting to first-order nilpotency for now
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        return f"{other} + {self}" if self.coeff > 0 else f"{other} - {abs(self.coeff)}ε"

    def __pow__(self, n):
        if n >= self.grade:
            return 0
        return f"ε^{n}" # Symbolic
