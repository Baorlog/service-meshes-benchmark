KUMA_NAMESPACE = kuma-system
APP_NAMESPACE = default
HELM_RELEASE = kuma

.PHONY: run stop

run:
	@echo "Adding Kuma Helm repo..."
	# helm repo add kuma https://kumahq.github.io/charts || true
	# helm repo update

	@echo "Installing Kuma with Helm..."
	helm install --create-namespace --namespace $(KUMA_NAMESPACE) $(HELM_RELEASE) kuma/kuma

	@echo "Enabling sidecar injection on namespace $(APP_NAMESPACE)..."
	kubectl label namespace $(APP_NAMESPACE) kuma.io/sidecar-injection=enabled --overwrite

	@echo "Rolling out all deployments in $(APP_NAMESPACE)..."
	kubectl rollout restart deployment -n $(APP_NAMESPACE)

	@echo "Kuma is installed and injection applied. Check pods with:"
	@echo "   kubectl get pods -n $(APP_NAMESPACE)"

stop:
	@echo "Uninstalling Kuma..."
	helm uninstall $(HELM_RELEASE) -n $(KUMA_NAMESPACE) || true
	kubectl delete namespace $(KUMA_NAMESPACE) --ignore-not-found

	@echo "Removing injection label from namespace $(APP_NAMESPACE)..."
	kubectl label namespace $(APP_NAMESPACE) kuma.io/sidecar-injection-

	@echo "Rolling out all deployments in $(APP_NAMESPACE)..."
	kubectl rollout restart deployment -n $(APP_NAMESPACE)

	@echo "Cleanup complete."
