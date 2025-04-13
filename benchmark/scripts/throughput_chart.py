import os
import json
import matplotlib.pyplot as plt

# === CONSTANTS ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
CASES = ["c4q100t2m", "c8q100t10m", "c16q200t10m"]
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_throughput(protocol):
    """
    Returns a dict:
    {
      'istio': [63.6, 97.2, 186.5],
      'linkerd': [...],
      ...
    }
    """
    mesh_data = {}

    for mesh in os.listdir(RESULTS_ROOT):
        print(mesh)
        mesh_case_dir = os.path.join(RESULTS_ROOT, mesh, protocol)
        if not os.path.isdir(mesh_case_dir):
            continue

        qps_values = []
        for case in CASES:
            json_path = os.path.join(mesh_case_dir, f"{mesh}-{protocol}-{case}.json")
            if not os.path.isfile(json_path):
                print(f"⚠️ Missing file: {json_path}")
                qps_values.append(0)
                continue

            with open(json_path, "r") as f:
                data = json.load(f)
                actual_qps = round(data.get("ActualQPS", 0), 2)
                qps_values.append(actual_qps)

        mesh_data[mesh] = qps_values

    return mesh_data


def plot_throughput_chart(protocol):
    data = extract_throughput(protocol)
    print(data)

    plt.figure(figsize=(10, 6))
    for mesh, qps_list in data.items():
        plt.plot(CASES, qps_list, marker="o", label=mesh)

    plt.title(f"Throughput - {protocol.upper()}")
    plt.xlabel("Test Case")
    plt.ylabel("Actual QPS")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, f"throughput_{protocol}.png")
    plt.savefig(output_path)
    print(f"✅ Saved chart to {output_path}")


# === RUN ===
if __name__ == "__main__":
    plot_throughput_chart("http")
    plot_throughput_chart("grpc")
