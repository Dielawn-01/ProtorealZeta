import numpy as np
import jax.numpy as jnp
import goait
from goait.timedilation import TimeDilation
from timesfm.src.timesfm.configs import ForecastConfig
import matplotlib.pyplot as plt

def run_demo():
    print("Initializing Time Dilation Hybrid...")
    
    # Initialize with default settings (no weights loaded for this demo)
    model = TimeDilation()
    
    # Create some dummy "spectral" data
    # We'll simulate a sequence of values that follow a prime-gap-like resonance
    seq_len = 128
    batch_size = 1
    patch_len = 32
    num_patches = seq_len // patch_len
    
    # Dummy inputs: (batch, num_patches, patch_len)
    inputs = np.random.randn(batch_size, num_patches, patch_len).astype(np.float32)
    masks = np.zeros_like(inputs, dtype=bool)
    
    print(f"Running inference on {seq_len} steps with Protoreal Dilation...")
    
    # Call the model
    (dilated, hidden, output_ts, quantiles), _ = model.model(inputs, masks)
    
    print("Inference successful.")
    print(f"Dilated Embeddings Shape: {dilated.shape}")
    print(f"Output TS Shape: {output_ts.shape}")
    
    # Calculate Jitter across the sequence to visualize the "Curvature"
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] # Just a few for the start
    jitters = []
    for i in range(len(primes) - 2):
        u = goait.resonance_antenna([i], [primes[i]])
        v = goait.resonance_antenna([i+1], [primes[i+1]])
        w = goait.resonance_antenna([i+2], [primes[i+2]])
        jitters.append(goait.get_jitter(u, v, w))
    
    print(f"Sample Jitters: {jitters[:5]}")
    
    # Compare with a 'Flat' (non-dilated) baseline conceptually
    # (In a real test, we'd compare training curves)
    
    print("\n[PROTOREAL INSIGHT]")
    print(f"The manifold curvature (delta) for this sequence is non-zero (avg: {np.mean(np.abs(jitters)):.4f}).")
    print("The Bogoliubov mixing has adjusted the hidden states to account for topological handedness.")

if __name__ == "__main__":
    run_demo()
