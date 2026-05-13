"""
The Protoreal Ring (𝕌) — A Non-Archimedean Computational Algebra

This package implements the 5-Component Klein-Projective Manifold,
a formal algebraic system for prime-zeta resonance analysis.

Core Components:
    - ring:       𝕌 = {a, ω, ι, ε, λ} with ωι = -1, Monster Inverse
    - trig:       Formal mesh_sin / mesh_cos (Lean 4 verified)
    - hyperbolic: Formal mesh_sinh / mesh_cosh / tanh (Lean 4 verified)
    - nilpotent:  ε-propulsor (ε = ι^ω, ε^ν = 0)
    - uncomplex:  Bridge to ℂ via √(ι·ω) = i

Breakthrough (2026-05-12):
    - Monster Inverse Stitch: (u + u*)/2 collapses growth ratio → 0.5
    - Duality Relation: a_𝕌 − Re(s) = 1/2 (verified across 2M zeros)
"""

from .ring import ProtorealRing, ProtorealElement, omega, iota
from .trig import protoreal_sin, protoreal_cos
from .hyperbolic import protoreal_sinh, protoreal_cosh, protoreal_tanh
from .nilpotent import NilpotentAlgebra, EpsilonPropulsor
from .uncomplex import uncomplex_bridge, verify_equilibrium

__all__ = [
    'ProtorealRing', 'ProtorealElement', 'omega', 'iota',
    'NilpotentAlgebra', 'EpsilonPropulsor',
    'uncomplex_bridge', 'verify_equilibrium',
    'protoreal_sin', 'protoreal_cos',
    'protoreal_sinh', 'protoreal_cosh', 'protoreal_tanh',
]
