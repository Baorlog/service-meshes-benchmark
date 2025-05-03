#!/bin/bash

MESH_NAME="$1"
DIR="$2"
INIT_BENCHMARK_TIME="$3"

cd $DIR

if [ -z "$MESH_NAME" ]; then
  MESH_NAME="baseline"
fi

FRONTEND_ENDPOINT="http://frontend.default.svc.cluster.local:80"
PRODUCT_ENDPOINT="productcatalogservice.default.svc.cluster.local:3550"

echo "Running benchmarking for HTTP"
OUTPUT_DIR="./results/$INIT_BENCHMARK_TIME/$MESH_NAME/http/"
mkdir -p "$OUTPUT_DIR"

# Thread: 4, qps: 100, time: 2m
THREAD=4
QPS=100
TIME=2m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-http-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" "$FRONTEND_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 8, qps: 100, time: 10m
THREAD=8
QPS=100
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-http-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" "$FRONTEND_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 16, qps: 200, time: 10m
THREAD=16
QPS=200
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-http-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" "$FRONTEND_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 16, qps: 4000, time: 10m
THREAD=16
QPS=4000
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-http-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" "$FRONTEND_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 320, qps: 4000, time: 10m
THREAD=320
QPS=4000
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-http-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" "$FRONTEND_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


echo "Running benchmarking for gRPC"
OUTPUT_DIR="./results/$INIT_BENCHMARK_TIME/$MESH_NAME/grpc/"
mkdir -p "$OUTPUT_DIR"

# Thread: 4, qps: 100, time: 2m
THREAD=4
QPS=100
TIME=2m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-grpc-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" --grpc "$PRODUCT_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 8, qps: 100, time: 10m
THREAD=8
QPS=100
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-grpc-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" --grpc "$PRODUCT_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 16, qps: 200, time: 10m
THREAD=16
QPS=200
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-grpc-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" --grpc "$PRODUCT_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 16, qps: 4000, time: 10m
THREAD=16
QPS=4000
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-grpc-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" --grpc "$PRODUCT_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60


# Thread: 320, qps: 4000, time: 10m
THREAD=320
QPS=4000
TIME=10m
echo "Thread: $THREAD, qps: $QPS, time: $TIME"

FILE_NAME="${MESH_NAME}-grpc-c${THREAD}q${QPS}t${TIME}.json"

# Run Fortio inside the cluster
kubectl exec -it fortio-client -- /usr/local/bin/fortio load -c "$THREAD" -qps "$QPS" -t "$TIME" --json "/tmp/$FILE_NAME" --grpc "$PRODUCT_ENDPOINT"

# Copy results from pod to local
kubectl cp "default/fortio-client:/tmp/$FILE_NAME" "$OUTPUT_DIR$FILE_NAME"

echo "Benchmark complete. Output saved to $OUTPUT_DIR$FILE_NAME"
echo "Waiting 1 minute..."
sleep 60
