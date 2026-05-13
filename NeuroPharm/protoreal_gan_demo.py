from goait.protoreal_gan import setup_protoreal_gan
import numpy as np

def run_gan_demo():
    print("--- ProtorealGAN: Topological Compass Demo ---")
    
    # Initialize the GAN
    gan = setup_protoreal_gan("gpt2-topological-compass")
    
    # Simulate a spectral sequence (Primes 2 to 71)
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
    
    print(f"Feeding Prime Sequence (N={len(primes)}) into GAN...")
    
    # Run a few training steps
    for step in range(3):
        results = gan.training_step(primes)
        print(f"\nStep {step + 1}:")
        print(f" - Topological Bearing: {results['bearing']:.4f}")
        print(f" - Geometric Facts Found: {results['facts_discovered']}")
        print(f" - Adversarial Reward: {results['reward']:.4f}")
        
        if results['bearing'] < -0.8:
            print("🧭 Compass indicates STRONG RESONANCE. Manifold is stable.")
        elif results['bearing'] > 0.0:
            print("🧭 Compass indicates MODULAR JITTER. Approaching Repulsion Wall.")

if __name__ == "__main__":
    run_gan_demo()
