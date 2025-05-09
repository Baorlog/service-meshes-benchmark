import os
import json
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
K6_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "k6", "results"))
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
K6_CASES = ["summary_case1.json", "summary_case2.json", "summary_case3.json"]

COLOR_MAP = {
    "kuma": "#1f77b4",
    "istio": "#ff7f0e",
    "baseline": "#2ca02c",
    "traefik": "#d62728",
    "linkerd": "#9467bd"
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_k6_latency(init_benchmark_times):
    mesh_case_data = defaultdict(lambda: defaultdict(list))

    for timestamp in init_benchmark_times:
        timestamp_dir = os.path.join(K6_ROOT, timestamp)
        if not os.path.isdir(timestamp_dir):
            continue

        for mesh in os.listdir(timestamp_dir):
            mesh_dir = os.path.join(timestamp_dir, mesh)
            if not os.path.isdir(mesh_dir):
                continue

            for idx, case_file in enumerate(K6_CASES):
                file_path = os.path.join(mesh_dir, case_file)
                if not os.path.isfile(file_path):
                    continue

                with open(file_path, "r") as f:
                    data = json.load(f)
                    duration = data.get("metrics", {}).get("http_req_duration", {})
                    avg = duration.get("avg", 0)
                    mesh_case_data[f"case{idx+1}"][mesh].append(round(avg, 2))

    averaged = defaultdict(dict)
    for case, mesh_data in mesh_case_data.items():
        for mesh, values in mesh_data.items():
            averaged[case][mesh] = round(sum(values) / len(values), 2) if values else 0

    return averaged

def plot_line_chart(case_data, run_id):
    plt.figure(figsize=(10, 6))
    mesh_names = set()
    for case in case_data:
        mesh_names.update(case_data[case].keys())

    mesh_names = sorted(mesh_names)
    for mesh in mesh_names:
        values = [case_data[case].get(mesh, 0) for case in sorted(case_data)]
        plt.plot(sorted(case_data), values, marker="o", label=mesh, color=COLOR_MAP.get(mesh, None))

    plt.title("Latency - HTTP (K6)")
    plt.xlabel("Test Case")
    plt.ylabel("Avg Latency (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    os.makedirs(os.path.join(OUTPUT_DIR, run_id), exist_ok=True)
    line_chart_path = os.path.join(OUTPUT_DIR, run_id, "k6_latency.png")
    plt.savefig(line_chart_path)
    print(f"Saved chart to {line_chart_path}")

def plot_bar_charts(case_data, run_id):
    for case, mesh_rates in case_data.items():
        meshes = list(mesh_rates.keys())
        values = list(mesh_rates.values())
        colors = [COLOR_MAP.get(mesh, "#7f7f7f") for mesh in meshes]

        plt.figure(figsize=(8, 6))
        bars = plt.bar(meshes, values, color=colors)
        plt.title(f"Latency - K6 - {case}")
        plt.xlabel("Service Mesh")
        plt.ylabel("Avg Latency (ms)")

        y_min = min(values)
        y_max = max(values)
        padding = (y_max - y_min) * 0.15 if y_max != y_min else 5
        plt.ylim(y_min - padding, y_max + padding)

        plt.tight_layout()
        out_file = os.path.join(OUTPUT_DIR, run_id, f"k6_latency_{case}.png")
        plt.savefig(out_file)
        print(f"Saved chart to {out_file}")

if __name__ == "__main__":
    run_id = sys.argv[1]
    if len(sys.argv) < 2:
        print("Usage: python3 k6_latency_chart.py <run_id> <timestamp1> [timestamp2...]")
        sys.exit(1)

    timestamps = sys.argv[2:]
    case_data = extract_k6_latency(timestamps)
    plot_line_chart(case_data, run_id)
    plot_bar_charts(case_data, run_id)
