import os
import json
import matplotlib.pyplot as plt
import datetime

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
METRICS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "..", "metrics", "node"))
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_memory_metrics(mesh):
    file_path = os.path.join(METRICS_DIR, mesh, f"node_memory_{mesh}.json")
    if not os.path.isfile(file_path):
        print(f"Missing: {file_path}")
        return [], []

    with open(file_path, "r") as f:
        data = json.load(f)

    values = data["data"]["result"][0]["values"]
    times = [datetime.datetime.fromtimestamp(v[0]) for v in values]
    mem_values = [float(v[1]) for v in values]
    return times, mem_values


def plot_node_memory_chart():
    plt.figure(figsize=(12, 6))
    plotted_meshes = []

    for mesh in os.listdir(METRICS_DIR):
        mesh_dir = os.path.join(METRICS_DIR, mesh)
        if not os.path.isdir(mesh_dir):
            continue

        times, mem_values = load_memory_metrics(mesh)
        if times and mem_values:
            # Plot on main comparison chart
            plt.plot(times, mem_values, label=mesh)
            plotted_meshes.append(mesh)

            # Save individual chart
            plt.figure(figsize=(12, 6))
            plt.plot(times, mem_values, label=mesh, color="tab:blue")
            plt.title(f"Node Memory Usage - {mesh}")
            plt.xlabel("Time")
            plt.ylabel("Active Memory Usage (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            out_path = os.path.join(OUTPUT_DIR, f"stress_node_memory_{mesh}.png")
            plt.savefig(out_path)
            plt.close()
            print(f"Saved individual chart: {out_path}")

    # Save all-mesh comparison chart
    if plotted_meshes:
        plt.title("Node Memory Usage Over Time (All Meshes)")
        plt.xlabel("Time")
        plt.ylabel("Active Memory Usage (%)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        out_path = os.path.join(OUTPUT_DIR, "stress_node_memory_chart.png")
        plt.savefig(out_path)
        print(f"Saved comparison chart: {out_path}")


# === MAIN ===
if __name__ == "__main__":
    plot_node_memory_chart()
