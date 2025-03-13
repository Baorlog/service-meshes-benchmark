# Makefile for Automating Linkerd Setup and Teardown

# Namespace
NAMESPACE=default

# Run Linkerd Installation, Injection, and Dashboard Setup
.PHONY: run
run:
	@echo "🔄 Installing Linkerd CRDs..."
	linkerd install --crds | kubectl apply -f -

	@echo "🔄 Installing Linkerd Control Plane..."
	linkerd install | kubectl apply -f -

	@echo "✅ Checking Linkerd Health..."
	linkerd check

	@echo "🚀 Enabling Linkerd Proxy Injection..."
	kubectl annotate namespace $(NAMESPACE) linkerd.io/inject=enabled --overwrite

	@echo "🔄 Restarting Deployments for Proxy Injection..."
	kubectl rollout restart deployment -n $(NAMESPACE)

	@echo "🚀 Installing Linkerd Viz Dashboard..."
	linkerd viz install | kubectl apply -f -

	@echo "✅ Linkerd Viz is ready. Run 'linkerd viz dashboard' to access."

# Teardown Linkerd from Cluster Completely
.PHONY: stop
stop:
	@echo "🛑 Uninstalling Linkerd Viz Dashboard..."
	linkerd viz uninstall | kubectl delete -f - || true

	@echo "🛑 Uninstalling Linkerd Control Plane..."
	linkerd uninstall | kubectl delete -f - || true

	@echo "🛑 Removing Linkerd CRDs..."
	linkerd install --crds | kubectl delete -f - || true

	@echo "🔄 Removing Linkerd Namespace if Exists..."
	kubectl delete namespace linkerd --ignore-not-found
	kubectl delete namespace linkerd-viz --ignore-not-found

	@echo "🔄 Restarting Deployments to Remove Sidecars..."
	kubectl rollout restart deployment -n $(NAMESPACE)

	@echo "✅ Linkerd and its components have been removed from the cluster."
