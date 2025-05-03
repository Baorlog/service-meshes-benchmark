import os
import subprocess
from datetime import datetime

def run(cmd):
    print(f"▶️ {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def main():
    init_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    os.environ["INIT_BENCHMARK_TIME"] = init_time
    print(f"📌 INIT_BENCHMARK_TIME set to {init_time}")

    run("python3 big_daddy.py")
    # run("python3 big_daddy.py istio")
    # run("python3 big_daddy.py linkerd")
    # run("python3 big_daddy.py kuma")
    # run("python3 big_daddy.py traefik")

if __name__ == "__main__":
    main()
