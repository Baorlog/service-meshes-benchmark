import pandas as pd
import matplotlib.pyplot as plt
import os

# === CONFIGURATION ===
DATA_PATH = "usage_qualitative_scores.csv"  # CSV file chứa dữ liệu
OUTPUT_PATH = "usage_qualitative_scores.png"

# === COLOR MAP ===
COLOR_MAP = {
    "istio": "#1f77b4",
    "linkerd": "#ff7f0e",
    "kuma": "#2ca02c",
    "traefik": "#d62728",
    "consul": "#9467bd",
    "aws app mesh": "#8c564b"
}

# === HATCH PATTERN MAP ===
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
    for bar in bars:
        bar.set_facecolor(color)
        bar.set_hatch(hatch)

ax.set_ylabel("Score")
ax.set_xlabel("Mức đáp ứng")
ax.set_title("Qualitative Evaluation of Service Meshes (Usage)")

# Đặt label trục x như yêu cầu: "Vượt tiêu chí", "Đạt tiêu chí", "Không đạt", "Tổng điểm"
ax.set_xticks([p + (len(df.columns) / 2 - 0.5) * bar_width for p in x])
ax.set_xticklabels(["Vượt tiêu chí", "Đạt tiêu chí", "Không đạt", "Tổng điểm"], rotation=0)

ax.legend()
ax.grid(axis="y", linestyle="--", linewidth=0.5)
plt.tight_layout()
plt.savefig(OUTPUT_PATH)
print(f"Saved chart to {OUTPUT_PATH}")
