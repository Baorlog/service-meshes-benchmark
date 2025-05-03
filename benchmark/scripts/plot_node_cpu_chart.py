import os
import json
import matplotlib.pyplot as plt
import datetime
import sys

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
METRICS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "..", "metrics", "node"))
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_cpu_metrics(mesh):
    file_path = os.path.join(METRICS_DIR, mesh, f"node_cpu_{mesh}.json")
    if not os.path.isfile(file_path):
        print(f"Missing: {file_path}")
        return [], []

    with open(file_path, "r") as f:
        data = json.load(f)

    values = data["data"]["result"][0]["values"]
    times = [datetime.datetime.fromtimestamp(v[0]) for v in values]
    cpu_values = [float(v[1]) for v in values]
    return times, cpu_values


def plot_node_cpu_chart(init_benchmark_time):
    plt.figure(figsize=(12, 6))
    plotted_meshes = []

    for mesh in os.listdir(METRICS_DIR):
        mesh_dir = os.path.join(METRICS_DIR, mesh)
        if not os.path.isdir(mesh_dir):
            continue

        times, cpu_values = load_cpu_metrics(mesh)
        if times and cpu_values:
            # Plot on main comparison chart
            plt.plot(times, cpu_values, label=mesh)
            plotted_meshes.append(mesh)

            # Save individual chart
            plt.figure(figsize=(12, 6))
            plt.plot(times, cpu_values, label=mesh, color="tab:orange")
            plt.title(f"Node CPU Usage - {mesh}")
            plt.xlabel("Time")
            plt.ylabel("CPU Usage (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            out_path = os.path.join(OUTPUT_DIR, init_benchmark_time, f"stress_node_cpu_{mesh}.png")
            plt.savefig(out_path)
            plt.close()
            print(f"Saved individual chart: {out_path}")

    # Save all-mesh comparison chart
    if plotted_meshes:
        plt.title("Node CPU Usage Over Time (All Meshes)")
        plt.xlabel("Time")
        plt.ylabel("CPU Usage (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        out_path = os.path.join(OUTPUT_DIR, init_benchmark_time, "stress_node_cpu_chart.png")
        plt.savefig(out_path)
        print(f"Saved comparison chart: {out_path}")


# === MAIN ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Usage: python3 latency_chart.py <init_benchmark_time>")
        sys.exit(1)

    init_benchmark_time = sys.argv[1]

    plot_node_cpu_chart(init_benchmark_time)
