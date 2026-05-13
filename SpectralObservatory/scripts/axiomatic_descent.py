import sys
import os
import numpy as np

# Ensure the local core is discoverable
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import core.ProtorealEngine as ue
import ZetaEngine as ze

def axiomatic_descent(target_t, initial_a=0.0, iterations=10):
    """
    Evolves the Protoreal state to discover the equilibrium 'a' value.
    The goal is to reach Standard Resonance (SR) = 0.
    """
    print(f"🕵️ Starting Axiomatic Descent for Zero at t={target_t}")
    print(f"   Initial a: {initial_a}")
    
    # Initialize state
    u = ue.zeta_project(target_t, a=initial_a)
    
    for i in range(iterations):
        sr = ue.calculate_standard_resonance(u)
        
        # HYPERBOLIC OPTIMIZATION:
        # Instead of a linear step, we use the Protoreal Tanh of the resonance.
        # This squashes the error and stabilizes the manifold evolution.
        step_potential = ue.protoreal_tanh(-sr)
        u.e = step_potential
        
        print(f"   [Step {i+1}] SR={sr:.6f} | Hyperbolic Step={u.e:.6f}")
        
        # Sow the potential into Reality (a)
        u = u.funct()
        
    print(f"   Final State: {u}")
    print(f"   Discovered 'a' Connection: {u.a}")
    return u.a

if __name__ == "__main__":
    # Test on the first Zeta zero
    t1 = 14.134725
    a_found = axiomatic_descent(t1, initial_a=0.0)
    
    if abs(a_found - 1.0) < 0.001:
        print("\n🏁 Equilibrium reached at a = 1.0 (The Protoreal Attractor).")
    elif abs(a_found - 0.5) < 0.001:
        print("\n🏁 Equilibrium reached at a = 0.5 (The Critical Line).")
    else:
        print(f"\n🏁 Equilibrium reached at a = {a_found}")
