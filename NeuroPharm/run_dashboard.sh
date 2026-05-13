#!/bin/bash

# GOAIT Research Dashboard Launcher
echo "📊 Launching GOAIT Research Dashboard..."

# Path to the bittensor-env python (which has streamlit installed in typical research environments)
# If not, use the system python
PYTHON_BIN="/home/phrxmaz/bittensor-env/bin/python3"
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run streamlit
$PYTHON_BIN -m streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
