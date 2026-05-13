"""
zeta_bridge.py — Bridge to Prime Search ZetaEngine

Imports numerical resonance data from the Spectral Observatory and
wraps it in the Protoreal algebraic framework.
"""

import sys
import os

# Add Prime Search to path
PRIME_SEARCH_PATH = "."
sys.path.append(PRIME_SEARCH_PATH)
sys.path.append(os.path.join(PRIME_SEARCH_PATH, "TheLab"))

try:
    import ZetaEngine as ze
except ImportError:
    ze = None

from protoreal.ring import ProtorealElement

class ZetaBridge:
    """
    Translates ZetaEngine outputs into Protoreal Ring elements.
    """
    def __init__(self):
        self.engine = ze

    def lift_t3(self, l, m, n):
        """
        Lifts a T3 Antenna result into U.
        val, epsilon, norm_eps, rank = ze.T3_l_m_n(l, m, n)
        
        Mapping:
            a = nearest zero (the 'anchor')
            b = epsilon (the transfinite divergence)
            c = -norm_eps (the infinitesimal correction)
        """
        if not self.engine:
            raise RuntimeError("ZetaEngine not found in Prime Search path.")
            
        val, eps, norm, rank = self.engine.T3_l_m_n(l, m, n)
        
        # We model the resonant state as:
        # u = nearest_zero + epsilon*ω - norm_eps*ι
        # Finding the nearest zero from val and eps:
        # Since eps = abs(val - nearest), we can infer nearest.
        # For simplicity, we use the engine's 'nearest' logic if we had it,
        # but the engine returns 'rank' which we can use to look up.
        
        # Simplified lifting for the workbench:
        return ProtorealElement(a=float(val), b=float(eps), c=-float(norm))

    def resonance_state(self, m, n, mode='D'):
        """
        General lift for D or T series.
        """
        if mode == 'D':
            val, eps, norm, rank = self.engine.D_m_n(m, n)
        else:
            val, eps, norm, rank = self.engine.T_m_n(m, n)
            
        return ProtorealElement(a=float(val), b=float(eps), c=-float(norm))
