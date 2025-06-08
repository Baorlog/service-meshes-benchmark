import os
import json
import csv
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_latency_chart(protocol, case_id, output_csv, output_png):
    data = {}
    x_labels = []

    with open(output_csv, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        x_labels = headers[1:]
        for row in reader:
            mesh = row[0]
            values = list(map(float, row[1:]))
            data[mesh] = values

    # Thêm marker style và line style để phân biệt đen trắng
    marker_styles = ['o', 's', '^', 'D', '*', 'v', 'x', '+']
    line_styles = ['-', '--', '-.', ':']

    plt.figure(figsize=(10, 6))
    for i, (mesh, values) in enumerate(data.items()):
        marker = marker_styles[i % len(marker_styles)]
        line_style = line_styles[i % len(line_styles)]
        plt.plot(x_labels, values, marker=marker, linestyle=line_style, label=mesh)

    plt.title(f"Latency - {str(protocol).upper()} - {case_id}")
    plt.xlabel("Percentile / Metric")
    plt.ylabel("Latency (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_png)
    print(f"Chart saved to {output_png}")

def extract_latency(protocol, case_id, init_benchmark_times, run_id):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    INPUT_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
    OUTPUT_DIR = os.path.join(ROOT_DIR, "data", run_id)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    OUTPUT_CSV = os.path.join(OUTPUT_DIR, f"data_latency_{protocol}_{case_id}.csv")
    OUTPUT_PNG = os.path.join(OUTPUT_DIR, f"data_latency_{protocol}_{case_id}.png")

    metrics = ["avg", "p50", "p75", "p90", "p99", "p99.9", "max"]
    mesh_metric_data = defaultdict(lambda: defaultdict(list))

    for timestamp in init_benchmark_times:
        timestamp_dir = os.path.join(INPUT_ROOT, timestamp)
        if not os.path.isdir(timestamp_dir):
            print(f"Skipping invalid timestamp folder: {timestamp_dir}")
            continue

        for mesh in os.listdir(timestamp_dir):
            protocol_dir = os.path.join(timestamp_dir, mesh, protocol)
            if not os.path.isdir(protocol_dir):
                continue

            filename = f"{mesh}-{protocol}-{case_id}.json"
            file_path = os.path.join(protocol_dir, filename)
            if not os.path.isfile(file_path):
                print(f"Missing: {file_path}")
                continue

            with open(file_path, "r") as f:
                j = json.load(f)
                hist = j["DurationHistogram"]

                mesh_data = {
                    "avg": round(hist["Avg"] * 1000, 2),
                    "max": round(hist["Max"] * 1000, 2),
                    "p50": 0,
                    "p75": 0,
                    "p90": 0,
                    "p99": 0,
                    "p99.9": 0
                }

                for p in hist["Percentiles"]:
                    key = f"p{p['Percentile']}"
                    if key in mesh_data:
                        mesh_data[key] = round(p["Value"] * 1000, 2)

                for m in metrics:
                    mesh_metric_data[mesh][m].append(mesh_data[m])

    rows = []
    for mesh, metric_map in mesh_metric_data.items():
        averaged = [round(sum(metric_map[m]) / len(metric_map[m]), 2) if metric_map[m] else 0 for m in metrics]
        rows.append([mesh] + averaged)

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mesh"] + metrics)
        writer.writerows(rows)

    print(f"CSV saved to {OUTPUT_CSV}")
    plot_latency_chart(protocol, case_id, OUTPUT_CSV, OUTPUT_PNG)

def generate_two_mesh_comparison_chart(protocol, case_id, run_id):
    import matplotlib.pyplot as plt
    import os

    csv_path = os.path.join("data", run_id, f"data_latency_{protocol}_{case_id}.csv")
    output_path = os.path.join("data", run_id, f"comparison_latency_{protocol}_{case_id}.png")

    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        return

    data = {}
    metrics = []

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        metrics = headers[1:]

        for row in reader:
            mesh = row[0].strip().lower()
            if mesh in ["baseline", "istio"]:
                data[mesh] = list(map(float, row[1:]))

    if "baseline" not in data or "istio" not in data:
        print(f"Not enough data in {csv_path}")
        return

    # Style giống biểu đồ gốc
    style_map = {
        "baseline": {"label": "Baseline", "color": "#2ca02c", "linestyle": "-.", "marker": "^"},
        "istio": {"label": "Istio", "color": "#ff7f0e", "linestyle": "--", "marker": "s"},
    }

    plt.figure(figsize=(10, 6))
    for mesh in ["baseline", "istio"]:
        style = style_map[mesh]
        plt.plot(
            metrics,
            data[mesh],
            label=style["label"],
            color=style["color"],
            linestyle=style["linestyle"],
            marker=style["marker"],
        )

    plt.title(f"{protocol.upper()} Latency: Baseline vs Istio - {case_id}")
    plt.xlabel("Metric")
    plt.ylabel("Latency (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    print(f"Chart saved: {output_path}")

    def percentage_diff(a, b):
        return round((b - a) / a * 100, 2) if a else float("inf")

    baseline_avg, baseline_max = data["baseline"][0], data["baseline"][-1]
    istio_avg, istio_max = data["istio"][0], data["istio"][-1]

    print(f"Case {case_id} ({protocol.upper()}):")
    print(f"  Avg Latency Diff: {percentage_diff(baseline_avg, istio_avg)}%")
    print(f"  Max Latency Diff: {percentage_diff(baseline_max, istio_max)}%")

if __name__ == "__main__":
    run_id = sys.argv[1]
    init_benchmark_times = sys.argv[2:]
    if not init_benchmark_times:
        print("Error: Please pass at least one benchmark timestamp folder")
        sys.exit(1)

    for protocol in ["http", "grpc"]:
        for case_id in ["c4q100t2m", "c8q100t10m", "c16q200t10m", "c16q400t10m", "c64q400t10m"]:
            extract_latency(protocol, case_id, init_benchmark_times, run_id)

    for protocol in ["http", "grpc"]:
        for case_id in ["c4q100t2m", "c64q400t10m"]:
            generate_two_mesh_comparison_chart(protocol, case_id, run_id)
