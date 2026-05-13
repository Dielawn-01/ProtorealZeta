from goait.dud import DeductiveProtorealDatabase
import goait

def run_zetaspace_demo():
    print("--- ZetaSpace Geometry Engine Demo ---")
    dud = DeductiveProtorealDatabase()

    # Define a triangle in ZetaSpace
    print("Constructing Triangle {A, B, C}...")
    dud.add_point("A", 0, 0)
    dud.add_point("B", 1, 0)
    dud.add_point("C", 0, 1)

    # Add a collinear point D on AB
    print("Adding Point D(0.5, 0) on segment AB...")
    dud.add_point("D", 0.5, 0)

    # Run inference (Symbolic Deduction)
    print("Running DUD Inference Engine...")
    facts = dud.run_inference()
    
    print("\n[Deduced Facts]:")
    for fact in facts:
        print(f" - {fact}")

    # Demonstrate Protoreal Pythagoras
    print("\n[Protoreal Geometric Reasoning]:")
    # Distance AC = 1, AB = 1
    # Standard BC = sqrt(2)
    # Protoreal BC incorporates manifold curvature
    u_ac = goait.ProtorealFull(1, 0, 0)
    u_ab = goait.ProtorealFull(1, 0, 0)
    
    from goait.zetaspace import ProtorealAR
    u_bc_sq = ProtorealAR.protoreal_pythagoras(u_ac, u_ab)
    print(f"Standard BC^2: 2.0")
    print(f"Protoreal BC^2: {u_bc_sq.a} (Curvature adjustment applied)")

    # Moebius Check
    print("\n[Moebius Stability Check]:")
    print(f"Point A Stability: {dud.check_moebius_stability('A')}")

if __name__ == "__main__":
    run_zetaspace_demo()
