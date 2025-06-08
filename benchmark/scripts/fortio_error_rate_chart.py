import os
import json
import sys
import math
import matplotlib.pyplot as plt
from collections import defaultdict

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
CASES = ["c4q100t2m", "c8q100t10m", "c16q200t10m", "c16q400t10m", "c64q400t10m"]
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_error_rates(protocol, timestamps):
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

                    error_rate = 1.0 if total == 0 else round(1 - (success_count / total), 10)
                    mesh_case_data[mesh][case].append(error_rate)

    # Average across runs
    mesh_data = {}
    for mesh, case_map in mesh_case_data.items():
        mesh_data[mesh] = [
            round(sum(case_map[case]) / len(case_map[case]), 10) if case_map[case] else 1.0
            for case in CASES
        ]

    return mesh_data

def plot_error_rate_chart(protocol, timestamps, run_id):
    data = extract_error_rates(protocol, timestamps)

    for mesh, error_list in data.items():
        for i, val in enumerate(error_list):
            if val == 0:
                error_list[i] = 1e-10
            error_list[i] = math.log10(error_list[i])

    marker_styles = ['o', 's', '^', 'D', '*', 'v', 'x', '+']
    line_styles = ['-', '--', '-.', ':']

    plt.figure(figsize=(10, 6))
    for i, (mesh, error_list) in enumerate(data.items()):
        marker = marker_styles[i % len(marker_styles)]
        line_style = line_styles[i % len(line_styles)]
        plt.plot(CASES, error_list, marker=marker, linestyle=line_style, label=mesh)

        # Hiển thị giá trị chính xác tại điểm cuối cùng
        x_val = CASES[-1]
        y_val = error_list[-1]
        display_val = round(10**y_val, 10)  # Lấy lại error rate thực tế
        plt.text(x_val, y_val, f"{display_val:.1e}", fontsize=8, ha='center', va='bottom', color='black')

    plt.title(f"Error Rate (log10) - {protocol.upper()}")
    plt.xlabel("Test Case")
    plt.ylabel("log10(Error Rate)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.join(OUTPUT_DIR, run_id), exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, run_id, f"error_rate_{protocol}_log10.png")
    plt.savefig(out_path)
    print(f"Saved chart to {out_path}")

# === MAIN ===
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Usage: python3 fortio_error_rate_chart.py <run_id> <init_benchmark_time1> [time2 ...]")
        sys.exit(1)

    run_id = sys.argv[1]
    timestamps = sys.argv[2:]

    plot_error_rate_chart("http", timestamps, run_id)
    plot_error_rate_chart("grpc", timestamps, run_id)
