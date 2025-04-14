import os
import pandas as pd
import matplotlib.pyplot as plt

# === CONFIGURATION ===
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(ROOT_DIR, "data", "startup_time.csv")
OUTPUT_PATH = os.path.join(ROOT_DIR, "data", "startup_time_chart.png")

# === LOAD DATA ===
df = pd.read_csv(DATA_PATH)

# === COMPUTE AVERAGES ===
averages = df.drop(columns=["Time"]).mean()

# === PLOT ===
plt.figure(figsize=(8, 5))
averages.plot(kind="bar", color="skyblue")
plt.title("Average Startup Time of Service Meshes")
plt.xlabel("Service Mesh")
plt.ylabel("Startup Time (seconds)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
print(f"Saved chart to {OUTPUT_PATH}")
