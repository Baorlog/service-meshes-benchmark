SHELL := /bin/bash
NAMESPACE := traefik-mesh
HELM_RELEASE := traefik-mesh
HELM_CHART := traefik/traefik-mesh
SERVICE_FILE := traefik-mesh-proxy-service.yaml

.PHONY: run stop check-traefik wait-for-pods

run: 
	@echo "Installing Traefik Mesh in namespace $(NAMESPACE)..."
	# @helm repo add traefik https://helm.traefik.io/traefik
	# @helm repo update
	@helm install $(HELM_RELEASE) $(HELM_CHART) -n $(NAMESPACE) --create-namespace || { echo "Helm install failed"; exit 1; }
	@$(MAKE) wait-for-pods
	@echo "Traefik Mesh installed successfully!"

	@echo "Applying $(SERVICE_FILE)..."
	@kubectl apply -f $(SERVICE_FILE) -n $(NAMESPACE) || { echo "Failed to apply service file"; exit 1; }
	@echo "$(SERVICE_FILE) applied successfully!"

stop:
	@echo "Uninstalling Traefik Mesh..."
	@helm uninstall $(HELM_RELEASE) -n $(NAMESPACE) || echo "Helm release not found, skipping."
	@kubectl delete namespace $(NAMESPACE) --ignore-not-found
	@echo "Traefik Mesh removed successfully!"

check-traefik:
	@kubectl get pods -n $(NAMESPACE) || echo "No pods found in $(NAMESPACE)."

wait-for-pods:
	@echo "⏳ Waiting for Traefik Mesh pods (`app=maesh`) to be ready..."
	@kubectl wait --for=condition=Ready pod -l app=maesh -n $(NAMESPACE) --timeout=180s || \
	{ echo "Pods failed to become ready"; exit 1; }
	@echo "All Traefik Mesh pods are ready!"
