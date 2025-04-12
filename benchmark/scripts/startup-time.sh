#!/bin/bash

# Usage: ./startup-time.sh <service-mesh-name>
# Example: ./startup-time.sh istio

set -e

MESH_NAME=$1
if [ -z "$MESH_NAME" ]; then
  echo "❌ Error: Service mesh name not provided."
  echo "Usage: ./startup-time.sh <service-mesh-name>"
  exit 1
fi

# Save current directory to return to it later
ORIGINAL_DIR=$(pwd)

MESH_DIR="${ORIGINAL_DIR}/../../deployments/service-meshes/${MESH_NAME}"
OUTPUT_FILE="${MESH_DIR}/startup-time.txt"

if [ ! -f "${MESH_DIR}/Makefile" ]; then
  echo "❌ Error: Makefile not found in $MESH_DIR"
  exit 1
fi

# Clear previous results
echo "📄 Writing startup times to $OUTPUT_FILE"
echo -n > "$OUTPUT_FILE"

# Enter the mesh folder
cd "$MESH_DIR"

for i in {1..5}; do
  echo "🔁 Run #$i for $MESH_NAME"

  START_TIME=$(date +%s)

  # Deploy
  make run

  # Wait for readiness
  echo "⏳ Waiting for deployments to be ready..."
  kubectl rollout status deployment -n default --timeout=180s

  END_TIME=$(date +%s)
  STARTUP_DURATION=$((END_TIME - START_TIME))

  echo "$STARTUP_DURATION" >> startup-time.txt
  echo "✅ Run #$i startup time: ${STARTUP_DURATION}s"

  # Teardown
  make stop

  # Wait for readiness
  echo "⏳ Waiting for deployments to be ready..."
  kubectl rollout status deployment -n default --timeout=180s

  # Optional cooldown between runs
  sleep 5
done

# Return to original directory for next loop
cd "$ORIGINAL_DIR"

echo "📊 All 5 startup times logged in $OUTPUT_FILE"
