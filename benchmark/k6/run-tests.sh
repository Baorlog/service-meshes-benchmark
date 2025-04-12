#!/bin/bash

FRONTEND_IP=$(minikube ip)
FRONTEND_PORT=$(kubectl get svc frontend-external -o=jsonpath='{.spec.ports[0].nodePort}')
FRONTEND_URL="http://${FRONTEND_IP}:${FRONTEND_PORT}"

echo "🌐 Using frontend URL: $FRONTEND_URL"

echo "🚀 Running Case 1: Constant 25 VUs for 10 min"
k6 run \
  --tag test_case=case-1 \
  --duration 10m \
  --vus 25 \
  --summary-export=results/summary_case1.json \
  --env FRONTEND_URL=$FRONTEND_URL \
  test-script.js

echo "⏸️ Waiting 1 minute..."
sleep 60

echo "🚀 Running Case 2: Constant 50 VUs for 10 min"
k6 run \
  --tag test_case=case-2 \
  --duration 10m \
  --vus 50 \
  --summary-export=results/summary_case2.json \
  --env FRONTEND_URL=$FRONTEND_URL \
  test-script.js

echo "⏸️ Waiting 1 minute..."
sleep 60

echo "🚀 Running Case 3: Ramp up to 200 users and down"
k6 run \
  -u 0 \
  -s 10m:200 \
  -s 2m:0 \
  --tag test_case=case-3 \
  --summary-export=results/summary_case3.json \
  --env FRONTEND_URL=$FRONTEND_URL \
  test-script.js
