#!/bin/bash

# GOAIT (Generative Observatory for Adelic Topology) Launcher
# Use this script to start background training on the Bittensor CLI

echo "🚀 Launching GOAIT Training Session..."
echo "Environment: bittensor-env"
echo "Project: ProtorealGAN (Goait)"

# Path to the high-performance venv python
PYTHON_BIN="/home/phrxmaz/Documents/Prime Search/venv/bin/python3"

# Set PYTHONPATH to include the current directory
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Optional: Set Bittensor Network UID (default to 1 for local/test)
export GOAIT_NETUID=1

# Run the trainer in the background (using nohup to survive shell exit)
nohup $PYTHON_BIN goait/goait_trainer.py > goait_training.log 2>&1 &

echo "✅ GOAIT is now training in the background."
echo "📝 Logs are being written to: goait_training.log"
echo "💤 Sleep well. The manifold is being stabilized."
