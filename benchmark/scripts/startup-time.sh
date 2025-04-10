START=$(date +%s)
kubectl apply -f service.yaml
kubectl wait --for=condition=ready pod -l app=xyz
END=$(date +%s)
echo "Startup time: $((END - START)) seconds"
