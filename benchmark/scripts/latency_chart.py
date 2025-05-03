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

    plt.figure(figsize=(10, 6))
    for mesh, values in data.items():
        plt.plot(x_labels, values, marker="o", label=mesh)

    plt.title(f"Latency - {str(protocol).upper()} - {case_id}")
    plt.xlabel("Percentile / Metric")
    plt.ylabel("Latency (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_png)
    print(f"Chart saved to {output_png}")

def extract_latency(protocol, case_id, init_benchmark_times):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    INPUT_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
    OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
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

if __name__ == "__main__":
    init_benchmark_times = sys.argv[1:]
    if not init_benchmark_times:
        print("Error: Please pass at least one benchmark timestamp folder")
        sys.exit(1)

    for protocol in ["http", "grpc"]:
        for case_id in ["c4q100t2m", "c8q100t10m", "c16q200t10m", "c16q400t10m", "c32q400t10m"]:
            extract_latency(protocol, case_id, init_benchmark_times)
