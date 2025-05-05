import subprocess
from datetime import datetime
import os
import sys
from random_name import generate_random_name

DEFAULT_INIT_BENCHMARK_TIMES = ["2025-05-04-04-16-30", "2025-05-04-14-18-14"]

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)


if __name__ == "__main__":
    init_benchmark_times = sys.argv[1:]
    if not init_benchmark_times:
        print("No benchmark times defined, use in-code instead")
        init_benchmark_times = DEFAULT_INIT_BENCHMARK_TIMES

    init_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    run_id = f"{generate_random_name()}_{init_time}"

    run(f"python3 latency_chart.py {run_id} {' '.join(init_benchmark_times)}")
    run(f"python3 fortio_throughput_chart.py {run_id} {' '.join(init_benchmark_times)}")
    run(f"python3 k6_throughput_chart.py {run_id} {' '.join(init_benchmark_times)}")
    run(f"python3 error_rate_chart.py {run_id} {' '.join(init_benchmark_times)}")

    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    OUTPUT_DIR = os.path.join(ROOT_DIR, "data", run_id)
    with open(os.path.join(OUTPUT_DIR, "time_keep.txt"), "a") as file:
        for time in init_benchmark_times:
            file.write(f"{time}\n")
