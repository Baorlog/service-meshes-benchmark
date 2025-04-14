.PHONY: istio-run istio-stop

ISTIO_NAMESPACE=istio-system
ISTIO_FILES=istio-onlineboutique-full.yaml prometheus.yaml kiali.yaml

run:
	@echo "Deploying Istio and related resources..."
	istioctl install --set profile=demo -y
	@for file in $(ISTIO_FILES); do \
		kubectl apply -f $$file; \
	done
	kubectl rollout restart deployment -n default
	@echo "Istio and resources have been deployed."

stop:
	@echo "Stopping Istio and removing resources..."
	@for file in $(ISTIO_FILES); do \
		kubectl delete -f $$file; \
	done
	istioctl uninstall --purge -y
	@echo "Waiting for Istio namespace to be deleted..."
	kubectl delete namespace $(ISTIO_NAMESPACE) --wait
	kubectl rollout restart deployment -n default
	@echo "Istio and namespace have been removed."
