CONSUL_NS=consul
HELM_RELEASE=consul
HELM_VALUES=helm-values.yaml
ALLOW_ALL_INTENTIONS=allow-all-intention.yaml
KUSTOMIZE_DIR=.

.PHONY: run stop debug

run:
	@echo "[+] Creating namespace $(CONSUL_NS)"
	kubectl create ns $(CONSUL_NS) --dry-run=client -o yaml | kubectl apply -f -

	@echo "[+] Installing Consul via Helm"
	helm upgrade --install $(HELM_RELEASE) hashicorp/consul \
		--namespace $(CONSUL_NS) \
		-f $(HELM_VALUES)

	@echo "[+] Waiting for connect-injector service to be ready"
	kubectl wait --timeout=30s --for=condition=available deployment/consul-connect-injector -n $(CONSUL_NS)

	@echo "[+] Applying allow-all intentions"
	kubectl apply -f $(ALLOW_ALL_INTENTIONS)

	@echo "[+] Applying kustomize patching"
	kubectl apply -k $(KUSTOMIZE_DIR)

	@echo "[+] Restarting deployments in default namespace"
	kubectl rollout restart deployment -n default

stop:
	@echo "[+] Removing default namespace labels and annotations"
	kubectl label ns default consul.hashicorp.com/connect-inject- || true
	kubectl annotate ns default consul.hashicorp.com/connect-inject- || true

	@echo "[+] Deleting Consul Helm release"
	helm uninstall $(HELM_RELEASE) -n $(CONSUL_NS) || true

	@echo "[+] Deleting namespace $(CONSUL_NS)"
	kubectl delete ns $(CONSUL_NS) --ignore-not-found

	@echo "[+] Restarting deployments in default namespace"
	kubectl rollout restart deployment -n default

debug:
	@echo "Creating hello-grpc server pod..."
	kubectl apply -f hello-grpc.yaml

	@echo "[+] Starting debug pod with Ubuntu and grpcurl setup"
	kubectl run grpcurl-debug \
		--image=ubuntu \
		--restart=Never \
		--namespace=default \
		--command -- bash -c "apt-get update && \
		  apt-get install -y wget tar && \
		  wget https://github.com/fullstorydev/grpcurl/releases/download/v1.9.3/grpcurl_1.9.3_linux_x86_64.tar.gz && \
		  tar -xvf grpcurl_1.9.3_linux_x86_64.tar.gz && \
		  chmod +x grpcurl && \
		  mv grpcurl /usr/local/bin && \
		  bash"

	@echo "[+] To connect: kubectl exec -it grpcurl-debug -- bash"
