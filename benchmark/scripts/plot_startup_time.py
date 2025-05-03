import os
import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT_DIR, "data", "startup_time.csv")
OUTPUT_PATH = os.path.join(ROOT_DIR, "data", "startup_time_chart.png")

# === COLOR MAP ===
COLOR_MAP = {
    "istio": "#ff7f0e",
    "linkerd": "#9467bd",
    "kuma": "#1f77b4",
    "traefik": "#d62728"
}

# === LOAD DATA ===
df = pd.read_csv(DATA_PATH)

# === COMPUTE AVERAGES ===
averages = df.drop(columns=["Time"]).mean()

# === PLOT ===
plt.figure(figsize=(8, 5))
colors = [COLOR_MAP.get(mesh.lower(), "#7f7f7f") for mesh in averages.index]
averages.plot(kind="bar", color=colors)
plt.title("Average Startup Time of Service Meshes")
plt.xlabel("Service Mesh")
plt.ylabel("Startup Time (seconds)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
print(f"Saved chart to {OUTPUT_PATH}")
