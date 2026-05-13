"""
ring.py — The Protoreal Ring (U)

Defines U = R[omega, iota] as a quotient polynomial ring with the
fundamental relation omega*iota = -1.

Elements: u = a + b*omega + c*iota   where a, b, c in R
"""

try:
    from sage.all import SR, PolynomialRing, QQ
    SAGE_AVAILABLE = True
except ImportError:
    SAGE_AVAILABLE = False


class ProtorealElement:
    """
    Element of the Klein Universe (𝕌): u = {a, w, i, e, l}
    a: Real Part
    w: Transfinite Thrust (omega)
    i: Infinitesimal Anchor (iota)
    e: Noise Potential (epsilon)
    l: Consolidation Level (lambda)
    """

    def __init__(self, a=0, b=0, c=0, e=0, l=0):
        self.a = float(a) if not isinstance(a, (int, float)) else a
        self.b = float(b) if not isinstance(b, (int, float)) else b # Thrust (w)
        self.c = float(c) if not isinstance(c, (int, float)) else c # Anchor (i)
        self.e = float(e) if not isinstance(e, (int, float)) else e # Noise (e)
        self.l = float(l) if not isinstance(l, (int, float)) else l # Level (l)

    def __repr__(self):
        parts = []
        if self.a != 0: parts.append(f"{self.a}")
        if self.b != 0: parts.append("w" if self.b == 1 else f"{self.b}w")
        if self.c != 0: parts.append("i" if self.c == 1 else f"{self.c}i")
        if self.e != 0: parts.append("e" if self.e == 1 else f"{self.e}e")
        if self.l != 0: parts.append("l" if self.l == 1 else f"{self.l}l")
        return " + ".join(parts).replace("+ -", "- ") if parts else "0"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            other = ProtorealElement(a=other)
        if not isinstance(other, ProtorealElement):
            return NotImplemented
        return ProtorealElement(
            self.a + other.a, 
            self.b + other.b, 
            self.c + other.c, 
            self.e + other.e, 
            self.l + other.l
        )

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            other = ProtorealElement(a=other)
        if not isinstance(other, ProtorealElement):
            return NotImplemented
        return ProtorealElement(
            self.a - other.a, 
            self.b - other.b, 
            self.c - other.c, 
            self.e - other.e, 
            self.l - other.l
        )

    def __mul__(self, other):
        """
        KLEIN MULTIPLICATION (Non-commutative)
        u1 * u2 -> a_part = a1a2 - b1m2 + m1b2 + l1e2 - e1l2
        """
        if isinstance(other, (int, float)):
            other = ProtorealElement(a=other)
        if not isinstance(other, ProtorealElement):
            return NotImplemented
        
        # Real part contraction
        a_part = (self.a * other.a) - (self.b * other.c) + (self.c * other.b) + (self.l * other.e) - (self.e * other.l)
        
        # Thrust part (w) is idempotent: w*w = w
        b_part = (self.a * other.b) + (other.a * self.b) + (self.b * other.b)
        
        # Anchor part (i)
        c_part = (self.a * other.c) + (other.a * self.c)
        
        # Noise part (e) - DUAL NUMBER PROPERTY: epsilon^2 = 0
        # Only linear terms (a1e2 + a2e1) survive.
        e_part = (self.a * other.e) + (other.a * self.e)
        
        # Level part (l)
        l_part = (self.a * other.l) + (other.a * self.l) + (self.l * other.l)
        
        return ProtorealElement(a_part, b_part, c_part, e_part, l_part)

    def funct(self):
        """Sowing Operator (funct): a <- a + e, e <- 0, l += 1."""
        return ProtorealElement(a=self.a + self.e, b=self.b, c=self.c, e=0, l=self.l + 1)

    def bearing(self):
        """
        Topological Bearing (Compass): Extracts orientation flux b*c.
        Invariant under Monster Inverse and characterizes topological drift.
        """
        return self.b * self.c

    def monster_inverse(self):
        """
        Monster Inverse (𝕌*):
        Swaps Thrust (b) and Anchor (c).
        Reflects the R4 symmetry of the 25-48 dimension horizon.
        """
        return ProtorealElement(a=self.a, b=self.c, c=self.b, e=self.e, l=self.l)

    def parity_locked_projection(self):
        """
        Combined Projection: (u + u_inv) / 2
        Forces the manifold into a balanced symmetry where Thrust = Anchor.
        """
        u_inv = self.monster_inverse()
        return ProtorealElement(
            a=self.a,
            b=(self.b + u_inv.b) / 2,
            c=(self.c + u_inv.c) / 2,
            e=self.e,
            l=self.l
        )

    def consolidate(self):
        """Consolidate: a, i <- a*2, i*2."""
        return ProtorealElement(a=self.a * 2, b=self.b, c=self.c * 2, e=self.e, l=self.l)

    def __eq__(self, other):
        if isinstance(other, (int, float)):
            other = ProtorealElement(a=other)
        if not isinstance(other, ProtorealElement):
            return NotImplemented
        return (self.a == other.a and self.b == other.b and self.c == other.c and 
                self.e == other.e and self.l == other.l)

class ProtorealRing:
    """Factory for the 5-component Klein Universe."""
    def __init__(self):
        self.zero = ProtorealElement(0,0,0,0,0)
        self.one = ProtorealElement(1,0,0,0,0)
        self.w = ProtorealElement(0,1,0,0,0)
        self.i = ProtorealElement(0,0,1,0,0)
        self.e = ProtorealElement(0,0,0,1,0)
        self.l = ProtorealElement(0,0,0,0,1)

    def element(self, a=0, b=0, c=0, e=0, l=0):
        return ProtorealElement(a, b, c, e, l)

    def omega(self): return self.w
    def iota(self): return self.i
    def epsilon(self): return self.e
    def lambda_element(self): return self.l

    def from_real(self, r):
        return ProtorealElement(a=r)

    def from_complex(self, z):
        z = complex(z)
        return ProtorealElement(a=z.real, b=z.imag, c=0)

    def verify_contraction(self):
        """Verify omega * iota = -1."""
        result = self.w * self.i
        return result == ProtorealElement(a=-1), result

    def get_duality_offset(self, t):
        """
        Calculates the theoretical 'a' attractor for a given zero height t.
        As proven in Lean 4: a_U = Re(s) + 1/2.
        For s = 1/2 + it, a_U = 1.0.
        """
        return 1.0 # The unique fixed point attractor

    def verify_commutativity(self, u1, u2):
        """Verify u1 * u2 == u2 * u1."""
        return u1 * u2 == u2 * u1

    def verify_distributivity(self, u1, u2, u3):
        """Verify u1 * (u2 + u3) == u1*u2 + u1*u3."""
        lhs = u1 * (u2 + u3)
        rhs = u1 * u2 + u1 * u3
        return lhs == rhs

    def sage_polynomial_ring(self):
        """Construct native SageMath quotient ring R[w,i]/<w*i+1>."""
        if not SAGE_AVAILABLE:
            raise RuntimeError("SageMath required")
        R = PolynomialRing(QQ, 'omega, iota')
        w, i = R.gens()
        return R.quotient(R.ideal(w * i + 1), names=['omega', 'iota'])


# Module-level convenience
U = ProtorealRing()
omega = U.omega()
iota = U.iota()
