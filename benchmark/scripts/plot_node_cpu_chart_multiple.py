
import os
import json
import matplotlib.pyplot as plt
import datetime
import sys
from collections import defaultdict

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
METRICS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "..", "metrics", "node"))
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")

def load_cpu_metrics(mesh, timestamp):
    file_path = os.path.join(METRICS_DIR, timestamp, mesh, f"node_cpu_{mesh}.json")
    if not os.path.isfile(file_path):
        print(f"Missing: {file_path}")
        return [], []

    with open(file_path, "r") as f:
        data = json.load(f)

    values = data["data"]["result"][0]["values"]
    times = [datetime.datetime.fromtimestamp(v[0]) for v in values]
    cpu_values = [float(v[1]) for v in values]
    return times, cpu_values

def plot_average_node_cpu_chart(run_id, timestamps):
    os.makedirs(os.path.join(OUTPUT_DIR, run_id), exist_ok=True)
    mesh_values_accumulator = defaultdict(list)

    for mesh in os.listdir(os.path.join(METRICS_DIR, timestamps[0])):
        all_times = None
        merged_values = []

        for timestamp in timestamps:
            times, values = load_cpu_metrics(mesh, timestamp)
            if not times or not values:
                continue
            if all_times is None:
                all_times = times
                merged_values = [[v] for v in values]
            else:
                for i in range(min(len(merged_values), len(values))):
                    merged_values[i].append(values[i])

        if merged_values:
            avg_values = [sum(v_list)/len(v_list) for v_list in merged_values]
            mesh_values_accumulator[mesh] = (all_times[:len(avg_values)], avg_values)

            # Individual chart
            plt.figure(figsize=(12, 6))
            plt.plot(all_times[:len(avg_values)], avg_values, label=mesh, color="tab:orange")
            plt.title(f"Node CPU Usage - {mesh}")
            plt.xlabel("Time")
            plt.ylabel("CPU Usage (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            out_path = os.path.join(OUTPUT_DIR, run_id, f"avg_node_cpu_{mesh}.png")
            plt.savefig(out_path)
            plt.close()
            print(f"Saved individual chart: {out_path}")

    # Combined chart
    plt.figure(figsize=(16, 8))
    for mesh, (times, avg_values) in mesh_values_accumulator.items():
        plt.plot(times, avg_values, label=mesh)
    if mesh_values_accumulator:
        plt.title("Node CPU Usage Over Time (All Meshes)")
        plt.xlabel("Time")
        plt.ylabel("CPU Usage (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        out_path = os.path.join(OUTPUT_DIR, run_id, "avg_node_cpu_chart.png")
        plt.savefig(out_path)
        print(f"Saved comparison chart: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 plot_node_cpu_chart.py <run_id> <timestamp1> [timestamp2 ...]")
        sys.exit(1)

    run_id = sys.argv[1]
    timestamps = sys.argv[2:]
    plot_average_node_cpu_chart(run_id, timestamps)
