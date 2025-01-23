# **Hệ thống Benchmark Kubernetes với Service Mesh**

## **Các thành phần trong hệ thống**

### **1. Kubernetes Cluster**
- **Mục đích:**
  - Nền tảng triển khai và quản lý các ứng dụng microservices.
  - Cung cấp khả năng tự động hóa việc điều phối tài nguyên, mở rộng, và tự phục hồi.

### **2. Istio**
- **Mục đích:**
  - Cung cấp service mesh để quản lý giao tiếp giữa các microservices.
  - Hỗ trợ load balancing, bảo mật (mTLS), giám sát và phân tích traffic.

### **3. Prometheus**
- **Mục đích:**
  - Hệ thống giám sát để thu thập và lưu trữ số liệu hiệu năng từ hệ thống.
  - Được sử dụng để kiểm tra các chỉ số như CPU, RAM, throughput và độ trễ.

### **4. Grafana**
- **Mục đích:**
  - Công cụ trực quan hóa số liệu thu thập từ Prometheus.
  - Cung cấp dashboard để phân tích hiệu năng và hiển thị kết quả benchmark.

### **5. TeaStore**
- **Mục đích:**
  - Ứng dụng microservices mẫu dùng để thử nghiệm và benchmark hiệu năng.
  - Bao gồm các thành phần: WebUI, Persistence, Recommender, Authentication, Registry.

### **6. k6**
- **Mục đích:**
  - Công cụ tạo tải để kiểm tra hiệu năng của hệ thống.
  - Hỗ trợ các loại kiểm tra: Load test, Stress test, và Spike test.

---

## **TODO List**

1. **Thiết lập môi trường:**
   - Cài đặt Kubernetes cluster.
   - Cấu hình các node Master và Worker.

2. **Triển khai các thành phần:**
   - Cài đặt Istio trên Kubernetes.
   - Triển khai TeaStore làm ứng dụng mẫu.
   - Cài đặt Prometheus và Grafana để giám sát.

3. **Viết kịch bản benchmark:**
   - Xây dựng các script k6 để tạo tải và kiểm tra hiệu năng.

4. **Thực hiện thử nghiệm:**
   - Chạy các kịch bản benchmark với nhiều loại tải khác nhau.
   - Thu thập số liệu và phân tích kết quả.

5. **Tạo báo cáo:**
   - Tổng hợp số liệu từ Prometheus và k6.
   - Sử dụng Grafana để hiển thị trực quan các kết quả thử nghiệm.
