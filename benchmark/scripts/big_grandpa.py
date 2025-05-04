import os
import subprocess
from datetime import datetime
import time

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    meshes = ["baseline", "istio", "linkerd", "kuma", "traefik"]

    for i in range(2):  # Run 2 rounds
        init_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        print(f"\n--- Run {i+1}/2 - init_benchmark_time = {init_time} ---\n")

        for mesh in meshes:
            run(f"python3 big_daddy.py {mesh} {init_time}")

        # Optional: short delay between runs to avoid overlapping timestamps
        time.sleep(2)

if __name__ == "__main__":
    main()
