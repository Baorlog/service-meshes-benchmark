# Makefile for Fortio Benchmarking

FORTIO_BIN ?= fortio
TARGET_URL ?= http://example.com/api
PAYLOAD_FILE ?= request.json

.PHONY: all low_load high_load payload_load compare_with_mesh server

all: low_load high_load payload_load

# Benchmark với tải thấp
low_load:
	@echo "Running low load benchmark..."
	$(FORTIO_BIN) load -qps 10 -c 1 -t 10s $(TARGET_URL)

# Benchmark với tải cao
high_load:
	@echo "Running high load benchmark..."
	$(FORTIO_BIN) load -qps 200 -c 20 -t 60s $(TARGET_URL)

# Benchmark với payload từ file JSON
payload_load:
	@echo "Running payload load benchmark..."
	$(FORTIO_BIN) load -qps 50 -c 10 -t 20s -payload-file=$(PAYLOAD_FILE) $(TARGET_URL)

# So sánh với/không có service mesh
compare_with_mesh:
	@echo "Running benchmark with service mesh..."
	$(FORTIO_BIN) load -qps 100 -c 10 -t 30s $(TARGET_URL)
	@echo "Running benchmark without service mesh..."
	$(FORTIO_BIN) load -qps 100 -c 10 -t 30s $(TARGET_URL) # Thay URL nếu cần

# Chạy Fortio server để sử dụng WebUI
server:
	@echo "Starting Fortio server..."
	$(FORTIO_BIN) server

clean:
	@echo "Cleaning up temporary files..."
	rm -f *.json *.txt *.log
