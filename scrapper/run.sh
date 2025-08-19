#!/bin/bash
set -euo pipefail

LOGFILE="run_scrapper.log"
exec > >(tee -a "$LOGFILE") 2>&1

echo "=== Starting Scrapper Script ==="
echo "Timestamp: $(date)"
echo "--------------------------------"

# Load conda
CONDA_BASE="$HOME/anaconda3"
if [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
    echo "[INFO] Sourcing conda.sh"
    source "$CONDA_BASE/etc/profile.d/conda.sh"
else
    echo "[ERROR] conda.sh not found at $CONDA_BASE/etc/profile.d/conda.sh" >&2
    exit 1
fi

# Activate conda environment
echo "[INFO] Activating conda environment: scrapper-env"
if conda activate scrapper-env; then
    echo "[OK] Conda environment activated"
else
    echo "[ERROR] Failed to activate conda environment: scrapper-env" >&2
    exit 1
fi

# Start Redis server
echo "[INFO] Starting Redis server on port 6376"
if redis-server --port 6376 --dbfilename dump.rdb --dir redis & then
    REDIS_PID=$!
    echo "[OK] Redis server started with PID $REDIS_PID"
else
    echo "[ERROR] Failed to start Redis server" >&2
    exit 1
fi

# Run Python script
echo "[INFO] Running Python scrapper"
if python -m src.main; then
    echo "[OK] Python scrapper finished successfully"
else
    echo "[ERROR] Python scrapper failed" >&2
    kill $REDIS_PID || true
    exit 1
fi

# Cleanup Redis after script ends
echo "[INFO] Stopping Redis server (PID $REDIS_PID)"
kill $REDIS_PID || true
wait $REDIS_PID 2>/dev/null || true

echo "--------------------------------"
echo "=== Scrapper Script Completed ==="
