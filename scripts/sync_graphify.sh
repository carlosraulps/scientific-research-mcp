#!/bin/bash
# Automatically synchronize the Graphify Knowledge Graph
set -e

REPO_DIR="/home/cr/simulations/scientific-research"
cd "$REPO_DIR"

echo "=== Synchronizing Graphify Knowledge Graph ==="
graphify update .
echo "=== Graphify synchronization complete! ==="
