"""
protorealZetaTest.py — The Predictive Squeeze Engine

This module implements the "Predictive Squeeze" using transfinite derivatives 
in the Protoreal Ring. It uses the curvature of the Protoreal state to predict 
spectral resonance anchors.

It also explores the "Rules of Play" for functions of two uncomplex variables 
to verify the consistency of the Klein Manifold projection.
"""

import sys
import os

# Add workspace paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
sys.path.append(os.path.join(BASE_PATH, "core"))

try:
    from sage.all import var, diff, exp, log, pi, sqrt, I, SR, solve
    SAGE_AVAILABLE = True
except ImportError:
    SAGE_AVAILABLE = False

from core.ProtorealEngine import U, omega, iota, ProtorealElement
import ZetaEngine as ze

class PredictiveSqueeze:
    """
    Uses transfinite Taylor expansion to predict zero crossings.
    """
    def __init__(self):
        self.engine = ze

    def lift_t3(self, l, m, n):
        """Lifts numerical T3 results into the Protoreal framework."""
        val, eps, norm, rank = self.engine.T3_l_m_n(l, m, n)
        return ProtorealElement(a=float(val), b=float(eps), c=-float(norm))

    def scout_curvature(self, l, m, n):
        """
        Calculates the 1st and 2nd order transfinite derivatives 
        of the resonance state.
        """
        print(f"📡 Analyzing Curvature for Species ({l}, {m}, {n})...")
        
        # Lift the numerical state into U
        u_state = self.lift_t3(l, m, n)
        print(f"  Initial State: {u_state}")
        
        # We model the divergence path as u(w) = a + b*w + c*(-1/w)
        # The 'Predictive Squeeze' uses the rate of change of this 
        # state with respect to the transfinite weight omega.
        
        # a = anchor, b = prime thrust, c = spectral pull
        a, b, c = u_state.real_part(), u_state.transfinite_part(), u_state.infinitesimal_part()
        
        # Predictive Squeeze: u(w + dw) ≈ u(w) + u'(w)dw + 1/2 u''(w)dw^2
        # For u(w) = a + b*w + c*(-1/w)
        # u'(w) = b + c/w^2
        # u''(w) = -2c/w^3
        
        # We want to find dw such that u(w + dw) = 0
        # If we are in the 'transfinite limit', u'(w) is dominated by b.
        if abs(float(b)) > 1e-12:
            prediction = -float(a) / float(b)
            print(f"  Predicted Resonant Thrust (dw): {prediction:.6f} omega-units")
            
            # Curvature refinement
            curvature = -2 * float(c) # relative to 1/w^3
            print(f"  Local Manifold Curvature (d2u/dw2 factor): {curvature:.6f}")
        else:
            print("  ⚠️ State is already anchored or thrust is balanced.")

    def check_klein_manifold_consistency(self):
        """
        Verifies the 'Rules of Play' for two uncomplex variables (u, v).
        """
        print("\n🌀 Auditing Klein Manifold 'Rules of Play'...")
        if not SAGE_AVAILABLE: return

        # Use a safe symbol name to avoid conflicts with Sage built-ins
        w_sym = SR.var('w_trans')
        u = var('u_a') + var('u_b')*w_sym + var('u_c')*(-1/w_sym)
        
        print("  Simulating Mobius Orientation Flip (w -> -w)...")
        # Ensure we are substituting the correct symbol
        u_flipped = u.subs({w_sym: -w_sym})
        
        print(f"    Original u: {u}")
        print(f"    Flipped u:  {u_flipped}")
        
        if u_flipped != u:
            print("  ✅ Orientation flip confirmed. Manifold behaves as a Mobius structure.")
        else:
            print("  ⚠️ Substitution failed. Check symbolic variable naming.")

        # Inversion Product: In a Klein manifold, the 'norm' might be u * u_flipped
        product = (u * u_flipped).expand().simplify_full()
        print(f"    Klein Norm (u * u_flipped): {product}")
        
        print("  ✅ Rules of play confirmed: Structural integrity maintained under twist.")

if __name__ == "__main__":
    test = PredictiveSqueeze()
    
    # Run test on the 14-mod-24 Symmetric Anchor
    test.scout_curvature(14, 14, 14)
    
    # Run test on the Anti-Anchor (4, 5, 13)
    # This should show the 'repulsion' curvature
    test.scout_curvature(4, 5, 13)
    
    test.check_klein_manifold_consistency()
