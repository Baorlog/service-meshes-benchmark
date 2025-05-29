import pandas as pd
import matplotlib.pyplot as plt
import os

# === CONFIGURATION ===
DATA_PATH = "characteristic_qualitative_scores.csv"
OUTPUT_PATH = "characteristic_qualitative_scores.png"

# === COLOR MAP ===
COLOR_MAP = {
    "istio": "#1f77b4",
    "linkerd": "#ff7f0e",
    "kuma": "#2ca02c",
    "traefik": "#d62728",
    "consul": "#9467bd",
    "aws app mesh": "#8c564b"
}

# === HATCH MAP ===
HATCH_MAP = {
    "istio": "//",
    "linkerd": "\\\\",
    "kuma": "xx",
    "traefik": "--",
    "consul": "..",
    "aws app mesh": "||"
}

# === LOAD DATA ===
df = pd.read_csv(DATA_PATH, index_col=0)

# === PLOT ===
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.12
x = range(len(df.index))

for i, mesh in enumerate(df.columns):
    mesh_key = mesh.lower().strip()
    color = COLOR_MAP.get(mesh_key, "#7f7f7f")
    hatch = HATCH_MAP.get(mesh_key, "")

    bars = ax.bar(
        [p + i * bar_width for p in x],
        df[mesh],
        width=bar_width,
        color=color,
        edgecolor='black',  # Viền đen
        label=mesh
    )
    # Thêm hatch đúng cách
    for bar in bars:
        bar.set_facecolor(color)  # Đảm bảo màu vẫn hiển thị
        bar.set_hatch(hatch)

ax.set_xlabel("Metric")
ax.set_ylabel("Score")
ax.set_title("Qualitative Evaluation of Service Meshes")
ax.set_xticks([p + (len(df.columns) / 2 - 0.5) * bar_width for p in x])
ax.set_xticklabels(df.index, rotation=0)
ax.legend()
ax.grid(axis="y", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
print(f"Saved chart to {OUTPUT_PATH}")
