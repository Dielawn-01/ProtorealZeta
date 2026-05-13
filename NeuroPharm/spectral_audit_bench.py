import goait
import numpy as np
import time

def spectral_audit_performance():
    print("--- Goait Spectral Audit Performance Check ---")
    
    # 2 Million Zeros simulation (summarized)
    # We'll run a batch of 10,000 to measure throughput
    batch_size = 10000
    primes = np.random.uniform(2, 10000, batch_size)
    indices = np.arange(batch_size)
    
    start_time = time.time()
    
    for i in range(batch_size):
        # High-performance Protoreal mapping in Rust
        u = goait.resonance_antenna([i], [primes[i]])
        # Calculate curvature (associator check)
        # In a real audit, we'd compare this to the Riemann zeros
        _ = goait.get_jitter(u, u, u) 
        
    end_time = time.time()
    
    duration = end_time - start_time
    throughput = batch_size / duration
    
    print(f"Batch Size: {batch_size}")
    print(f"Duration: {duration:.4f}s")
    print(f"Throughput: {throughput:.2f} Protoreal ops/sec")
    print(f"Estimated time for 2M zeros: {(2000000 / throughput) / 60:.2f} minutes")

if __name__ == "__main__":
    try:
        spectral_audit_performance()
    except Exception as e:
        print(f"Audit could not be run: {e}")
