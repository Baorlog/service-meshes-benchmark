import os
import subprocess
from datetime import datetime
import time
from extract_granny import extract_all
import sys

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main(iterating_time):
    meshes = ["baseline", "istio", "linkerd", "kuma", "traefik"]

    init_benchmark_times = []

    for i in range(iterating_time): 
        init_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        init_benchmark_times.append(init_time)
        print(f"\n--- Run {i+1}/2 - init_benchmark_time = {init_time} ---\n")

        for mesh in meshes:
            run(f"python3 big_daddy.py {mesh} {init_time}")

        # Optional: short delay between runs to avoid overlapping timestamps
        time.sleep(2)

    extract_all(init_benchmark_times)

if __name__ == "__main__":
    iterating_time = int(sys.argv[1])

    if len(sys.argv) < 1:
        print("Error: Usage: python3 big_grandpa.py <iterating_time>")
        sys.exit(1)

    print(f"Big grandpa is now running {iterating_time} round{'s' if iterating_time > 1 else ''}")

    main(iterating_time)
