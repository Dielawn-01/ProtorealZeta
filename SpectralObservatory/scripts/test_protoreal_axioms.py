import sys
import os
import unittest

# Ensure the local core is discoverable
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core'))
import ProtorealEngine as ue
from protoreal.ring import ProtorealElement, omega, iota, U

class TestProtorealKleinAxioms(unittest.TestCase):
    """
    Test Suite for the 5-Component Non-Commutative Protoreal-Klein Algebra.
    Based on formal proofs in LaRue_Protoreal_Algebra.
    """

    def test_klein_multiplication_bridge(self):
        """
        Verify the Anti-Commutative Bridge Identity:
        omega * iota = -1
        iota * omega = 1
        [omega, iota] = -2
        """
        w = ue.omega
        i = ue.iota
        
        wi = w * i
        iw = i * w
        commutator = wi - iw
        
        print(f"\n[Multiplication Test]")
        print(f"  omega * iota = {wi}")
        print(f"  iota * omega = {iw}")
        print(f"  [omega, iota] = {commutator}")
        
        self.assertEqual(wi.a, -1, "omega * iota should be -1")
        self.assertEqual(iw.a, 1, "iota * omega should be 1")
        self.assertEqual(commutator.a, -2, "Commutator [omega, iota] should be -2")

    def test_noise_consolidation_bridge(self):
        """
        Verify the Noise-Consolidation Identity:
        lam * eps = 1
        eps * lam = -1
        [eps, lam] = 2
        """
        e = ue.epsilon
        l = ue.lambda_element # 'lambda' is reserved in Python
        
        le = l * e
        el = e * l
        commutator = el - le
        
        print(f"\n[Consolidation Test]")
        print(f"  lambda * epsilon = {le}")
        print(f"  epsilon * lambda = {el}")
        print(f"  [epsilon, lambda] = {commutator}")
        
        self.assertEqual(le.a, 1, "lambda * epsilon should be 1")
        self.assertEqual(el.a, -1, "epsilon * lambda should be -1")

    def test_manifestation_operator(self):
        """
        Verify that Manifestation transfers Noise (e) to Reality (a).
        """
        u = ProtorealElement(a=10, e=5.5)
        print(f"\n[Manifestation Test]")
        print(f"  Pre-Manifest: {u}")
        
        u_new = u.manifest()
        print(f"  Post-Manifest: {u_new}")
        
        self.assertEqual(u_new.a, 15.5)
        self.assertEqual(u_new.e, 0)
        self.assertEqual(u_new.l, 1, "Consolidation level should increase")

    def test_zeta_projection_stability(self):
        """
        Verify that Consolidate sharpens the anchor of a Zeta projection.
        """
        t = 14.134725 # First Zeta zero
        u = ue.zeta_project(t)
        print(f"\n[Zeta Stability Test]")
        print(f"  Original Anchor: {u.c}")
        
        u_stable = u.consolidate()
        print(f"  Consolidated Anchor: {u_stable.c}")
        
        self.assertTrue(u_stable.c > u.c, "Consolidation should increase anchor weight")

if __name__ == "__main__":
    unittest.main()
