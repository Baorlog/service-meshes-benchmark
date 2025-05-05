import os
import json
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
CASES = ["c4q100t2m", "c8q100t10m", "c16q200t10m", "c16q400t10m", "c32q400t10m"]
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_error_rates(protocol, timestamps):
    """
    Returns a dict:
    {
        'istio': [avg_rate_case1, avg_rate_case2, ...],
        ...
    }
    """
    mesh_case_data = defaultdict(lambda: defaultdict(list))

    for timestamp in timestamps:
        timestamp_dir = os.path.join(RESULTS_ROOT, timestamp)
        if not os.path.isdir(timestamp_dir):
            print(f"Skipping missing timestamp: {timestamp}")
            continue

        for mesh in os.listdir(timestamp_dir):
            mesh_dir = os.path.join(timestamp_dir, mesh, protocol)
            if not os.path.isdir(mesh_dir):
                continue

            for case in CASES:
                file_path = os.path.join(mesh_dir, f"{mesh}-{protocol}-{case}.json")
                if not os.path.isfile(file_path):
                    print(f"Missing file: {file_path}")
                    continue

                with open(file_path, "r") as f:
                    data = json.load(f)
                    total = data.get("DurationHistogram", {}).get("Count", 0)
                    ret_codes = data.get("RetCodes", {})

                    success_count = 0
                    for code, count in ret_codes.items():
                        if code.startswith("2") or code.upper() in ["0", "OK", "SERVING"]:
                            success_count += count

                    error_rate = 1.0 if total == 0 else round(1 - (success_count / total), 4)
                    mesh_case_data[mesh][case].append(error_rate)

    # Average across runs
    mesh_data = {}
    for mesh, case_map in mesh_case_data.items():
        mesh_data[mesh] = [
            round(sum(case_map[case]) / len(case_map[case]), 4) if case_map[case] else 1.0
            for case in CASES
        ]

    return mesh_data

def plot_error_rate_chart(protocol, timestamps, run_id):
    data = extract_error_rates(protocol, timestamps)

    plt.figure(figsize=(10, 6))
    for mesh, error_list in data.items():
        plt.plot(CASES, error_list, marker="o", label=mesh)

    plt.title(f"Error Rate - {protocol.upper()}")
    plt.xlabel("Test Case")
    plt.ylabel("Error Rate")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, run_id, f"error_rate_{protocol}.png")
    plt.savefig(out_path)
    print(f"Saved chart to {out_path}")

# === MAIN ===
if __name__ == "__main__":
    run_id = sys.argv[1]
    if len(sys.argv) < 2:
        print("Error: Usage: python3 error_rate_chart.py <init_benchmark_time1> [time2 ...]")
        sys.exit(1)

    timestamps = sys.argv[2:]

    plot_error_rate_chart("http", timestamps, run_id)
    plot_error_rate_chart("grpc", timestamps, run_id)
