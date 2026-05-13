import bittensor as bt
import torch
import time
import os
import sys
from goait.protoreal_gan import setup_protoreal_gan
import numpy as np

# Add parent dir to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GoaitTrainer:
    """
    GOAIT (Generative Observatory for Adelic Topology) Trainer.
    A Bittensor-ready neuron that trains the ProtorealGAN.
    """
    def __init__(self, netuid=1, wallet_name="default", hotkey_name="default"):
        self.netuid = netuid
        
        # 1. Setup Bittensor connections
        print("🔗 Connecting to Subtensor...")
        self.subtensor = bt.subtensor()
        self.wallet = bt.wallet(name=wallet_name, hotkey=hotkey_name)
        self.metagraph = self.subtensor.metagraph(self.netuid)
        
        # 2. Setup ProtorealGAN (Goait)
        print("👹 Initializing ProtorealGAN (Goait)...")
        self.gan = setup_protoreal_gan("gpt2-topological-compass")
        
        # 3. Training Stats
        self.step = 0
        self.best_bearing = 0.0

    def sync(self):
        """Sync with the Bittensor metagraph."""
        print("🔄 Syncing metagraph...")
        self.metagraph.sync(subtensor=self.subtensor)

    def run_epoch(self, primes):
        """Run a single training epoch."""
        self.step += 1
        print(f"\n--- GOAIT Training Step {self.step} ---")
        
        # Execute GAN step
        results = self.gan.training_step(primes)
        
        bearing = results['bearing']
        reward = results['reward']
        facts = results['facts_discovered']
        
        print(f"🧭 Topological Bearing: {bearing:.4f}")
        print(f"💎 Adversarial Reward: {reward:.4f}")
        print(f"📜 Geometric Facts: {facts}")
        
        # Save checkpoint if resonance improves
        if bearing < self.best_bearing:
            self.best_bearing = bearing
            print("🌟 New Resonance Peak Detected! Saving Checkpoint...")
            # self.save_checkpoint()
            
        return results

    def start_background_loop(self, interval=60):
        """
        Main loop to run while the user sleeps.
        Continually refines the manifold stability.
        """
        print(f"🚀 Starting GOAIT Background Training (Interval: {interval}s)...")
        # Dummy prime set for the loop
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        
        try:
            while True:
                self.run_epoch(primes)
                # In a real subnet, we would also set weights or send extrinsic here
                # self.subtensor.set_weights(...)
                
                time.sleep(interval)
                if self.step % 10 == 0:
                    self.sync()
                    
        except KeyboardInterrupt:
            print("🛑 Training stopped by user.")

def run_trainer():
    # Use environment variables or defaults
    netuid = int(os.getenv("GOAIT_NETUID", 1))
    trainer = GoaitTrainer(netuid=netuid)
    
    # Run the loop
    trainer.start_background_loop()

if __name__ == "__main__":
    run_trainer()
