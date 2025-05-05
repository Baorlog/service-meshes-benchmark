#!/bin/bash

# === INPUT PARAMETERS ===
MESH_NAME="$1"
DIR="$2"
INIT_BENCHMARK_TIME="$3"

cd $DIR

if [ -z "$MESH_NAME" ]; then
  MESH_NAME="baseline"
fi

FRONTEND_ENDPOINT="http://frontend.default.svc.cluster.local:80"
PRODUCT_ENDPOINT="productcatalogservice.default.svc.cluster.local:3550"

# === FUNCTION: Run a single Fortio test ===
run_fortio() {
  local protocol=$1
  local connections=$2
  local qps=$3
  local duration=$4
  local output_dir=$5

  local case_label="c${connections}q${qps}t${duration}"
  local file_name="${MESH_NAME}-${protocol}-${case_label}.json"

  local endpoint="$FRONTEND_ENDPOINT"

  if [ "$protocol" = "grpc" ]; then
    endpoint="$PRODUCT_ENDPOINT"
  fi

  echo "Running Fortio $protocol test - Case $case_label"
  echo "Thread: $connections, qps: $qps, time: $duration"

  # Run Fortio inside the cluster
  kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$connections" -qps "$qps" -t "$duration" --json "/tmp/$file_name" "$endpoint"

  # Copy results from pod to local directory
  kubectl cp "default/fortio-client:/tmp/$file_name" "$output_dir$file_name"


  echo "Benchmark complete. Output saved to $output_dir$file_name"
  echo "Waiting 1 minute..."
  sleep 60
  echo ""
}

# === HTTP TEST CASES ===
echo "Running benchmarking for HTTP"
OUTPUT_DIR="./results/$INIT_BENCHMARK_TIME/$MESH_NAME/http/"
mkdir -p "$OUTPUT_DIR"

run_fortio "http" 4 100 "2m" "$OUTPUT_DIR"
# run_fortio "http" 8 100 "10m" "$OUTPUT_DIR"
# run_fortio "http" 16 200 "10m" "$OUTPUT_DIR"
# run_fortio "http" 16 400 "10m" "$OUTPUT_DIR"
# run_fortio "http" 32 400 "10m" "$OUTPUT_DIR"

# === gRPC TEST CASES ===
# echo "Running benchmarking for gRPC"
# OUTPUT_DIR="./results/$INIT_BENCHMARK_TIME/$MESH_NAME/grpc/"
# mkdir -p "$OUTPUT_DIR"

# run_fortio "grpc" 4 100 "2m" "$OUTPUT_DIR"
# run_fortio "grpc" 8 100 "10m" "$OUTPUT_DIR"
# run_fortio "grpc" 16 200 "10m" "$OUTPUT_DIR"
# run_fortio "grpc" 16 400 "10m" "$OUTPUT_DIR"
# run_fortio "grpc" 32 400 "10m" "$OUTPUT_DIR"
