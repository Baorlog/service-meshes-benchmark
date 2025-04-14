#!/bin/bash

# big-daddy.sh - Automate benchmarking for a service mesh

set -e

# Input mesh name: istio, linkerd, kuma, traefik (optional)
MESH_NAME=$1

cd ../..

if [ -n "$MESH_NAME" ]; then
  echo "Benchmarking mesh: $MESH_NAME"

  # === 1. Record start time for Prometheus metrics ===
  START_TIME=$(date +%s)
  echo "Start time recorded: $START_TIME"

  # === 2. Deploy service mesh ===
  echo "Deploying $MESH_NAME..."
  cd deployments/service-meshes/$MESH_NAME
  make run

  # Wait for readiness
  echo "Waiting for deployments to be ready..."
  kubectl rollout status deployment -n default --timeout=180s

  cd ../../../
else
  MESH_NAME="baseline"
  echo "No mesh selected, skipping mesh deployment. Benchmarking $MESH_NAME case"
  START_TIME=$(date +%s)
  echo "Start time recorded: $START_TIME"
fi

# === 3. Run Fortio and K6 benchmarks ===
echo "Running Fortio HTTP + gRPC tests..."
# You will define these scripts later, so we assume their names for now
cd ./benchmark/fortio
./run-fortio.sh "$MESH_NAME" "$PWD"

# echo "Running K6 user flow tests..."
# cd ../k6
# ./run-tests.sh "$MESH_NAME" "$PWD"

# === 4. Wait until results are complete (placeholder logic) ===
# Optional: check if result files exist
echo "Waiting for all test results to finish..."
sleep 30  # TODO: Replace with actual result-waiting logic if needed

# === 5. Extract Prometheus metrics ===
echo "Extracting Prometheus metrics..."
END_TIME=$(date +%s)
cd ../metrics
./extract-prometheus-metrics.sh "$START_TIME" "$END_TIME" "$MESH_NAME" "$PWD"

if [ -n "$MESH_NAME" ]; then
  # === 6. Reset everything
  cd ../../deployments/service-meshes/$MESH_NAME
  make stop

  # Wait for readiness
  echo "Waiting for deployments to be ready..."
  kubectl rollout status deployment -n default --timeout=180s

  cd ../../../benchmark/scripts
else
  cd ../scripts
fi

echo "Benchmarking complete for $MESH_NAME."
