
import os
import json
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
METRICS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "..", "metrics", "pod"))
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_pod_cpu_metrics(mesh, timestamp):
    file_path = os.path.join(METRICS_DIR, timestamp, mesh, f"pod_cpu_{mesh}.json")
    if not os.path.isfile(file_path):
        print(f"Missing: {file_path}")
        return {}

    with open(file_path, "r") as f:
        data = json.load(f)

    pod_data = defaultdict(list)
    for result in data["data"]["result"]:
        pod_name = result["metric"].get("pod", "unknown")
        values = result["values"]
        if not values:
            continue
        t0 = values[0][0]
        for v in values:
            rel_time = v[0] - t0
            pod_data[pod_name].append((rel_time, float(v[1])))

    return pod_data

def plot_pod_cpu_chart_multiple(run_id, timestamps):
    os.makedirs(os.path.join(OUTPUT_DIR, run_id), exist_ok=True)
    mesh_total_avg = {}

    mesh_list = sorted(os.listdir(os.path.join(METRICS_DIR, timestamps[0])))
    mesh_offsets = {mesh: idx * 8000 for idx, mesh in enumerate(mesh_list)}

    for mesh in mesh_list:
        per_pod_merged = defaultdict(lambda: defaultdict(list))
        total_cpu_by_time = defaultdict(list)

        for ts in timestamps:
            pod_data = load_pod_cpu_metrics(mesh, ts)
            if not pod_data:
                continue

            run_total = defaultdict(float)
            for pod, datapoints in pod_data.items():
                for rel_t, v in datapoints:
                    per_pod_merged[pod][rel_t].append(v)
                    run_total[rel_t] += v
            for rel_t, total in run_total.items():
                total_cpu_by_time[rel_t].append(total)

        offset = mesh_offsets[mesh]
        avg_total = {t + offset: sum(vals)/len(vals) for t, vals in total_cpu_by_time.items()}
        sorted_total = sorted(avg_total.items())
        mesh_total_avg[mesh] = sorted_total

        # Average per pod
        fig, ax = plt.subplots(figsize=(18, 8))  # larger width for legend clarity
        for pod, rel_t_dict in per_pod_merged.items():
            avg_series = sorted((t + offset, sum(vals)/len(vals)) for t, vals in rel_t_dict.items())
            times, values = zip(*avg_series)
            ax.plot(times, values, label=pod)

        ax.set_title(f"Pod CPU Usage - {mesh}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("CPU (cores)")
        ax.grid(True)
        ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8, ncol=2)
        fig.tight_layout(rect=[0, 0, 0.8, 1])
        out_path = os.path.join(OUTPUT_DIR, run_id, f"avg_pod_cpu_{mesh}.png")
        fig.savefig(out_path)
        plt.close(fig)
        print(f"Saved pod-level chart: {out_path}")

    # Combined chart
    if mesh_total_avg:
        plt.figure(figsize=(14, 6))
        for mesh, datapoints in mesh_total_avg.items():
            times, values = zip(*datapoints)
            plt.plot(times, values, label=mesh)

        plt.title("Total Pod CPU Usage Per Mesh (Average of Runs, Shifted)")
        plt.xlabel("Time (s)")
        plt.ylabel("CPU (cores)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        out_path = os.path.join(OUTPUT_DIR, run_id, "avg_pod_cpu_total_chart_shifted.png")
        plt.savefig(out_path)
        print(f"Saved total pod CPU comparison chart: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 plot_pod_cpu_chart_multiple_normalized_shifted.py <run_id> <timestamp1> [timestamp2 ...]")
        sys.exit(1)

    run_id = sys.argv[1]
    timestamps = sys.argv[2:]
    plot_pod_cpu_chart_multiple(run_id, timestamps)
