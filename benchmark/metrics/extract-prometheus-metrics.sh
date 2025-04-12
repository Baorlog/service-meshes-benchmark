#!/bin/bash

START="$1"
END="$2"
MESH_NAME="$3"

PROM_IP=$(minikube ip)
PROM_PORT=$(kubectl get svc prometheus -n monitoring -o=jsonpath='{.spec.ports[0].nodePort}')
PROM_URL="http://${PROM_IP}:${PROM_PORT}"

STEP="15s"

mkdir -p node pod

query_and_save() {
  local query="$1"
  local type="$2"   # node or pod
  local name="$3"   # e.g., node_cpu
  local out_dir="./$type"
  local outfile="${out_dir}/${name}_${MESH_NAME}.json"

  echo "📥 Fetching $type metric: $name"
  curl -sG "${PROM_URL}/api/v1/query_range" \
    --data-urlencode "query=$query" \
    --data-urlencode "start=${START}" \
    --data-urlencode "end=${END}" \
    --data-urlencode "step=${STEP}" \
    -o "$outfile"
}

# Node metrics
query_and_save "100 - (avg by (instance) (irate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)" node node_cpu
query_and_save "node_memory_Active_bytes / node_memory_MemTotal_bytes * 100" node node_memory

# Pod metrics (CPU in cores, memory in bytes)
query_and_save "sum(rate(container_cpu_usage_seconds_total{namespace=\"default\"}[1m])) by (pod)" pod pod_cpu
query_and_save "sum(container_memory_usage_bytes{namespace=\"default\"}) by (pod)" pod pod_memory

echo "✅ All metrics saved to ./node/ and ./pod/"
