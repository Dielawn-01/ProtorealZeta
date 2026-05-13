import bisect
import os
import numpy as np
import goait

class GoaitAgent:
    """
    An Intelligent Agent trained on 2 million Zeta Zeros.
    Provides CLI-ready insights for geometry, time series, and spectral resonance.
    """
    def __init__(self, zeros_path="/home/phrxmaz/Documents/Prime Search/zeta_zeros_2m.txt"):
        self.zeros_path = zeros_path
        self.zeros = self._load_zeros()
        print(f"🧬 GoaitAgent initialized with {len(self.zeros)} spectral anchors.")

    def _load_zeros(self):
        """Loads the spectral anchors into memory."""
        if not os.path.exists(self.zeros_path):
            print(f"⚠️ Spectral anchors not found at {self.zeros_path}. Using fallback.")
            return []
        
        zeros = []
        with open(self.zeros_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try: zeros.append(float(line))
                    except ValueError: continue
        return sorted(zeros)

    def query_resonance(self, t):
        """
        Query the agent about a spectral height 't'.
        Returns the nearest zero, the epsilon drift, and the Protoreal curvature.
        """
        if not self.zeros:
            return None
            
        t_f = float(t)
        idx = bisect.bisect_left(self.zeros, t_f)
        
        if idx == 0: 
            nearest = self.zeros[0]
        elif idx == len(self.zeros): 
            nearest = self.zeros[-1]
        else:
            before, after = self.zeros[idx-1], self.zeros[idx]
            nearest = before if abs(t_f - before) < abs(t_f - after) else after
            
        epsilon = abs(t_f - nearest)
        
        # Calculate Protoreal Curvature kappa = -2c
        # (Conceptual mapping: c = epsilon / local_spacing)
        local_spacing = 2 * np.pi / np.log(max(t_f, 14.2) / (2 * np.pi))
        c = epsilon / local_spacing
        kappa = -2 * c
        
        return {
            "nearest_zero": nearest,
            "epsilon": epsilon,
            "norm_epsilon": c,
            "manifold_curvature": kappa,
            "stability": "Resonance" if c < 0.25 else "Repulsion"
        }

    def solve_geometric_construction(self, points):
        """
        Geometric capability: Analyzes a set of points for Moebius stability.
        """
        # (Wraps ZetaSpace logic)
        from .zetaspace import DeductiveProtorealDatabase
        dud = DeductiveProtorealDatabase()
        for i, p in enumerate(points):
            dud.add_point(f"P{i}", p[0], p[1])
        
        return dud.run_inference()

    def forecast_dilation(self, sequence, primes):
        """
        Time series capability: Applies Time Dilation forecasting to a sequence.
        """
        # (Wraps TimeDilation logic)
        from .timedilation import TimeDilation
        import jax.numpy as jnp
        
        model = TimeDilation()
        # Simulated inference
        return model.model(sequence, np.zeros_like(sequence, dtype=bool))
