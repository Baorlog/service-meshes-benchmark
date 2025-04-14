import os
import json
import csv
import matplotlib.pyplot as plt


def plot_latency_chart(protocol, case_id):

    # === CONFIGURATION ===
    csv_filename = f"data_latency_{protocol}_{case_id}.csv"
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    INPUT_CSV = os.path.join(DATA_DIR, csv_filename)
    OUTPUT_PNG = os.path.join(DATA_DIR, csv_filename.replace(".csv", ".png"))

    # === LOAD CSV ===
    data = {}
    x_labels = []

    with open(INPUT_CSV, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        x_labels = headers[1:]  # avg, p50, ...
        for row in reader:
            mesh = row[0]
            values = list(map(float, row[1:]))
            data[mesh] = values

    # === PLOT ===
    plt.figure(figsize=(10, 6))
    for mesh, values in data.items():
        plt.plot(x_labels, values, marker="o", label=mesh)

    plt.title(f"Latency - {str(protocol).upper()} - {case_id}")
    plt.xlabel("Percentile / Metric")
    plt.ylabel("Latency (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG)
    print(f"Chart saved to {OUTPUT_PNG}")


def extract_latency(protocol, case_id):
    # === CONFIGURATION ===
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    INPUT_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
    OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    OUTPUT_CSV = os.path.join(OUTPUT_DIR, f"data_latency_{protocol}_{case_id}.csv")

    # === INITIALIZE ===
    metrics = ["avg", "p50", "p75", "p90", "p99", "p99.9", "max"]
    rows = []

    # === SCAN MESH FOLDERS ===
    for mesh in os.listdir(INPUT_ROOT):
        mesh_dir = os.path.join(INPUT_ROOT, mesh, protocol)
        if not os.path.isdir(mesh_dir):
            continue

        file_name = f"{mesh}-{protocol}-{case_id}.json"
        file_path = os.path.join(mesh_dir, file_name)
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

            row_values = [mesh_data[m] for m in metrics]
            rows.append([mesh] + row_values)

    # === WRITE CSV ===
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["mesh"] + metrics)
        writer.writerows(rows)

    print(f"CSV saved to {OUTPUT_CSV}")

    plot_latency_chart(protocol=protocol, case_id=case_id)


if __name__ == "__main__":
    for protocol in ["http", "grpc"]:
        for case_id in ["c4q100t2m", "c8q100t10m", "c16q200t10m", "c16q400t10m", "c32q400t10m"]:
            extract_latency(protocol=protocol, case_id=case_id)
