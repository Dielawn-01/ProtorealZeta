import goait
from .zetaspace import ZetaPoint, ZetaLine

class DeductiveProtorealDatabase:
    """
    Symbolic Deduction Engine for ZetaSpace.
    Mimics AlphaGeometry's DD but with non-associative manifold logic.
    """
    def __init__(self):
        self.points = {}
        self.lines = {}
        self.facts = [] # List of deduced geometric identities

    def add_point(self, name, x, y):
        u_x = goait.ProtorealFull(x, 0, 0)
        u_y = goait.ProtorealFull(y, 0, 0)
        p = ZetaPoint(u_x, u_y, name=name)
        self.points[name] = p
        return p

    def deduce_collinearity(self, p1_name, p2_name, p3_name):
        """Check if three points are collinear in the manifold."""
        p1 = self.points[p1_name]
        p2 = self.points[p2_name]
        p3 = self.points[p3_name]
        
        line = ZetaLine(p1, p2)
        if line.contains(p3):
            self.facts.append(f"Collinear({p1_name}, {p2_name}, {p3_name})")
            return True
        return False

    def check_moebius_stability(self, p_name):
        """
        Check if a point is stable under R4 reflection.
        A point is stable if its 'Polarizing Field' is Resonance.
        """
        p = self.points[p_name]
        # Resonance if c >= 0 (from PolarizingField.lean)
        if p.x.c >= 0 and p.y.c >= 0:
            return "Resonance"
        return "Repulsion"

    def run_inference(self):
        """
        Perform exhaustive deduction across the known points.
        This is a 'Squeeze' operation that stabilizes the geometry.
        """
        point_names = list(self.points.keys())
        for i in range(len(point_names)):
            for j in range(i + 1, len(point_names)):
                for k in range(j + 1, len(point_names)):
                    self.deduce_collinearity(point_names[i], point_names[j], point_names[k])
        
        return self.facts
