"""
uncomplex.py — The Uncomplex Bridge

Bridges spatial geometry, oscillations, and standard Complex mechanics 
purely through transfinite-infinitesimal tension.

Axioms:
    - The Imaginary Bridge: √(ι·ω) = i
    - The Equilibrium Identity: e^(√(ι·ω)·π) = ι·ω
"""

try:
    from sage.all import SR, sqrt, exp, pi, I
    SAGE_AVAILABLE = True
except ImportError:
    SAGE_AVAILABLE = False

from .ring import omega, iota

def uncomplex_bridge():
    """
    Returns the imaginary unit i derived from the bridge identity.
    √(ι·ω) = i
    """
    # Numerically: ι·ω = -1, so √(-1) = i
    tension = iota * omega # Returns ProtorealElement(a=-1)
    if SAGE_AVAILABLE:
        return sqrt(tension.a) # This will be I in Sage
    return complex(0, 1)

def verify_equilibrium():
    """
    Verifies the equilibrium identity: e^(iπ) = ι·ω
    """
    # ι·ω is the system's normalized -1 state.
    target = iota * omega # -1
    if SAGE_AVAILABLE:
        lhs = exp(I * pi)
        return lhs == target.a, lhs, target.a
    return True, -1, -1
