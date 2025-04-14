import os
import json
import matplotlib.pyplot as plt

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
RESULTS_ROOT = os.path.abspath(os.path.join(ROOT_DIR, "..", "fortio", "results"))
CASES = ["c4q100t2m", "c8q100t10m", "c16q200t10m", "c16q400t10m", "c32q400t10m"]
OUTPUT_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_error_rates(protocol):
    """
    Returns a dict:
    {
        'istio': [0.0, 0.01, 0.12],
        ...
    }
    """
    mesh_data = {}

    for mesh in os.listdir(RESULTS_ROOT):
        mesh_case_dir = os.path.join(RESULTS_ROOT, mesh, protocol)
        if not os.path.isdir(mesh_case_dir):
            continue

        error_rates = []
        for case in CASES:
            json_path = os.path.join(mesh_case_dir, f"{mesh}-{protocol}-{case}.json")
            if not os.path.isfile(json_path):
                print(f"⚠️ Missing file: {json_path}")
                error_rates.append(None)
                continue

            with open(json_path, "r") as f:
                data = json.load(f)
                total = data.get("DurationHistogram", {}).get("Count", 0)
                ret_codes = data.get("RetCodes", {})

                success_count = 0
                for code, count in ret_codes.items():
                    if code.startswith("2") or code.upper() in ["0", "OK", "SERVING"]:
                        success_count += count

                if total == 0:
                    error_rate = 1.0
                else:
                    error_rate = round(1 - (success_count / total), 4)

                error_rates.append(error_rate)

        mesh_data[mesh] = error_rates

    return mesh_data


def plot_error_rate_chart(protocol):
    data = extract_error_rates(protocol)

    plt.figure(figsize=(10, 6))
    for mesh, error_list in data.items():
        plt.plot(CASES, error_list, marker="o", label=mesh)

    plt.title(f"Error Rate - {protocol.upper()}")
    plt.xlabel("Test Case")
    plt.ylabel("Error Rate")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_DIR, f"error_rate_{protocol}.png")
    plt.savefig(output_path)
    print(f"✅ Saved chart to {output_path}")


# === MAIN ===
if __name__ == "__main__":
    plot_error_rate_chart("http")
    plot_error_rate_chart("grpc")
