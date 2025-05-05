import os
import json
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

# === CONSTANTS ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
CASES = ["c4q100t2m", "c8q100t10m", "c16q200t10m", "c16q400t10m", "c32q400t10m"]
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_throughput(protocol, init_benchmark_times):
    """
    Returns a dict:
    {
      'istio': [avg_c1, avg_c2, avg_c3, avg_c4, avg_c5],
      ...
    }
    """
    mesh_case_data = defaultdict(lambda: defaultdict(list))

    for timestamp in init_benchmark_times:
        timestamp_dir = os.path.join(RESULTS_ROOT, timestamp)
        if not os.path.isdir(timestamp_dir):
            print(f"Skipping missing folder: {timestamp_dir}")
            continue

        for mesh in os.listdir(timestamp_dir):
            protocol_dir = os.path.join(timestamp_dir, mesh, protocol)
            if not os.path.isdir(protocol_dir):
                continue

            for case in CASES:
                file_path = os.path.join(protocol_dir, f"{mesh}-{protocol}-{case}.json")
                if not os.path.isfile(file_path):
                    print(f"Missing: {file_path}")
                    continue

                with open(file_path, "r") as f:
                    data = json.load(f)
                    actual_qps = round(data.get("ActualQPS", 0), 2)
                    mesh_case_data[mesh][case].append(actual_qps)

    # Aggregate by averaging per mesh/case
    mesh_data = {}
    for mesh, case_map in mesh_case_data.items():
        mesh_data[mesh] = [
            round(sum(case_map[case]) / len(case_map[case]), 2) if case_map[case] else 0
            for case in CASES
        ]

    return mesh_data


def plot_throughput_chart(protocol, init_benchmark_times, run_id):
    data = extract_throughput(protocol, init_benchmark_times)
    print(f"Aggregated throughput data ({protocol}): {data}")

    plt.figure(figsize=(10, 6))
    for mesh, qps_list in data.items():
        plt.plot(CASES, qps_list, marker="o", label=mesh)

    plt.title(f"Throughput - {protocol.upper()}")
    plt.xlabel("Test Case")
    plt.ylabel("Actual QPS")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    out_file = os.path.join(OUTPUT_DIR, run_id, f"throughput_{protocol}.png")
    plt.savefig(out_file)
    print(f"Saved chart to {out_file}")


# === RUN ===
if __name__ == "__main__":
    run_id = sys.argv[1]
    if len(sys.argv) < 2:
        print("Error: Usage: python3 throughput_chart.py <init_benchmark_time> [more_times...]")
        sys.exit(1)

    init_benchmark_times = sys.argv[2:]

    plot_throughput_chart("http", init_benchmark_times, run_id)
    plot_throughput_chart("grpc", init_benchmark_times, run_id)
