import os
import subprocess
import sys
from datetime import datetime
import time

def run(cmd, cwd=None, shell=True):
    print(f"Running: {cmd}")
    subprocess.run(cmd, cwd=cwd, shell=shell, check=True)

def main(mesh_name, init_benchmark_time):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    result_dir = os.path.join(root_dir, "benchmark", "results", init_benchmark_time, mesh_name)
    os.makedirs(result_dir, exist_ok=True)
    print(f"Output folder: {result_dir}")

    print(f"Benchmarking mesh: {mesh_name}")
    start_time = int(time.time())
    print(f"Start time recorded: {start_time}")

    if mesh_name != "baseline":
        print(f"Deploying {mesh_name}...")
        mesh_dir = os.path.join(root_dir, "deployments", "service-meshes", mesh_name)
        run("make run", cwd=mesh_dir)
        print("Waiting for deployments to be ready...")
        run("kubectl rollout status deployment -n default --timeout=180s")

    run_fortio = os.path.join(root_dir, "benchmark", "fortio", "run-fortio.sh")
    run(f"{run_fortio} {mesh_name} {result_dir}")

    run_k6 = os.path.join(root_dir, "benchmark", "k6", "run-tests.sh")
    run(f"{run_k6} {mesh_name} {result_dir}")

    print("Waiting for test results...")
    time.sleep(30)

    end_time = int(time.time())
    extract_script = os.path.join(root_dir, "benchmark", "metrics", "extract-prometheus-metrics.sh")
    run(f"{extract_script} {start_time} {end_time} {mesh_name} {result_dir}")

    if mesh_name != "baseline":
        stop_dir = os.path.join(root_dir, "deployments", "service-meshes", mesh_name)
        run("make stop", cwd=stop_dir)
        print("Waiting for deployments to terminate...")
        run("kubectl rollout status deployment -n default --timeout=180s")

    print(f"Benchmarking complete for {mesh_name}.")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: Usage: python3 big_daddy.py <mesh_name> <init_benchmark_time>")
        sys.exit(1)

    mesh_name = sys.argv[1]
    init_benchmark_time = sys.argv[2]
    main(mesh_name, init_benchmark_time)
