import sys
import os
import math

# Add workspace paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../core")

from core.ProtorealEngine import ProtorealState, omega, iota, U
import ZetaEngine as ze

def protoreal_exp(u):
    """
    Formal Taylor expansion of e^u in the Protoreal Ring.
    e^(a + bw + ci) = e^a * (1 - c(e^b - 1) + (e^b - 1)w + ci)
    (Derived using w^2 = w, i^2 = 0, wi = -1)
    """
    a, b, c = float(u.a), float(u.b), float(u.c)
    exp_a = math.exp(a)
    exp_b = math.exp(b)
    
    a_prime = exp_a * (1 - c * (exp_b - 1))
    b_prime = exp_a * (exp_b - 1)
    c_prime = exp_a * c
    
    return ProtorealState(a=a_prime, b=b_prime, c=c_prime)

def formal_sinh(u):
    """sinh(u) = (exp(u) - exp(-u)) / 2 using formal Protoreal exp."""
    return (protoreal_exp(u) - protoreal_exp(-u)) * 0.5

def custom_sinh(u):
    """The 'Resonance Pulse' identity: sinh(u) = (b*w + c*i) * 2*pi*a"""
    a, b, c = float(u.a), float(u.b), float(u.c)
    factor = 2 * math.pi * a
    return ProtorealState(a=0, b=b * factor, c=c * factor)

def main():
    print("𝕌 REVERSE ENGINEERING RESONANCE PULSE")
    print("-" * 40)
    
    # Analyze zeros from the dataset
    zeros = ze.KNOWN_ZEROS
    if not zeros:
        print("Error: No zeros loaded.")
        return
        
    print(f"Loaded {len(zeros)} zeros.")
    
    for p_idx in [1, 2, 3, 5, 8, 13, 21]: # Fibonacci sequence of prime indices
        # We need a prime pair or T3 to get an ProtorealState
        # Let's use D_m_n for (p_idx, p_idx)
        val, eps, norm, rank = ze.D_m_n(p_idx, p_idx)
        val_f = float(val)
        u_state = ProtorealState(a=val_f, b=float(eps), c=-float(norm))
        
        f_sinh = formal_sinh(u_state)
        c_sinh = custom_sinh(u_state)
        
        print(f"\n[Rank {rank}] Zero at T={val_f:.4f}")
        print(f"  Protoreal State: {u_state}")
        
        # Linearized hypothesis: e^iu approx e^ia * (1 + i(bw + ci))
        # This implies sinh(u) approx i * sin(u/i)
        # For small b, c: sinh(a + bw + ci) approx sinh(a) + cosh(a)(bw + ci)
        
        lin_sinh = ProtorealState(a=math.sinh(val_f), b=math.cosh(val_f)*float(eps), c=-math.cosh(val_f)*float(norm))
        
        print(f"  Formal Sinh: {f_sinh}")
        print(f"  Linearized Sinh: {lin_sinh}")
        print(f"  Custom Resonance Pulse: {c_sinh}")
        
        # Calculate ratio/scaling
        if abs(c_sinh.b) > 0:
            ratio_b = f_sinh.b / c_sinh.b
            print(f"  Thrust Ratio (Formal/Custom): {ratio_b:.2e}")
            
    print("\n--- HYPOTHESIS: PHASE LOCK ---")
    print("The custom sinh definition is a 'Linearization' of the formal sinh")
    print("at the transfinite scale. We are looking for the 'Uncomplex Bridge'")
    print("that connects them.")

if __name__ == "__main__":
    main()
