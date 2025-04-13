import os
import json
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
METRICS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "..", "metrics", "pod"))
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_pod_cpu_metrics(mesh):
    file_path = os.path.join(METRICS_DIR, mesh, f"pod_cpu_{mesh}.json")
    if not os.path.isfile(file_path):
        print(f"⚠️ Missing: {file_path}")
        return {}

    with open(file_path, "r") as f:
        data = json.load(f)

    pod_data = defaultdict(list)

    for result in data["data"]["result"]:
        pod_name = result["metric"].get("pod", "unknown")
        for value in result["values"]:
            timestamp, usage = value
            pod_data[pod_name].append((datetime.datetime.fromtimestamp(timestamp), float(usage)))

    return pod_data


def plot_pod_cpu_chart():
    total_cpu_by_mesh = {}

    for mesh in os.listdir(METRICS_DIR):
        mesh_dir = os.path.join(METRICS_DIR, mesh)
        if not os.path.isdir(mesh_dir):
            continue

        pod_data = load_pod_cpu_metrics(mesh)
        if not pod_data:
            continue

        # Plot individual pods for this mesh
        fig, ax = plt.subplots(figsize=(14, 6))
        for pod_name, datapoints in pod_data.items():
            times, usages = zip(*datapoints)
            ax.plot(times, usages, label=pod_name)

        ax.set_title(f"Pod CPU Usage - {mesh}")
        ax.set_xlabel("Time")
        ax.set_ylabel("CPU (cores)")
        ax.grid(True)
        ax.legend(
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            borderaxespad=0.0,
            fontsize="small",
            ncol=1
        )

        fig.tight_layout(rect=[0, 0, 0.85, 1])
        out_path = os.path.join(OUTPUT_DIR, f"pod_cpu_{mesh}.png")
        fig.savefig(out_path)
        plt.close(fig)
        print(f"✅ Saved pod-level chart: {out_path}")

        # Aggregate total per timestamp
        combined = defaultdict(float)
        for _, datapoints in pod_data.items():
            for ts, usage in datapoints:
                combined[ts] += usage

        sorted_combined = sorted(combined.items())
        total_cpu_by_mesh[mesh] = sorted_combined

    # Plot combined total CPU per mesh
    if total_cpu_by_mesh:
        plt.figure(figsize=(12, 6))
        for mesh, datapoints in total_cpu_by_mesh.items():
            times, totals = zip(*datapoints)
            plt.plot(times, totals, label=mesh)

        plt.title("Total Pod CPU Usage Per Mesh")
        plt.xlabel("Time")
        plt.ylabel("CPU (cores)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        out_path = os.path.join(OUTPUT_DIR, "pod_cpu_total_chart.png")
        plt.savefig(out_path)
        print(f"✅ Saved total pod CPU comparison chart: {out_path}")


# === MAIN ===
if __name__ == "__main__":
    plot_pod_cpu_chart()
