import os
import subprocess
from datetime import datetime

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    init_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    run(f"python3 big_daddy.py baseline {init_time}")
    run(f"python3 big_daddy.py istio {init_time}")
    run(f"python3 big_daddy.py linkerd {init_time}")
    run(f"python3 big_daddy.py kuma {init_time}")
    run(f"python3 big_daddy.py traefik {init_time}")

if __name__ == "__main__":
    main()
