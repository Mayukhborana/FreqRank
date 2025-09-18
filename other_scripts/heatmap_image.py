import matplotlib.pyplot as plt
import seaborn as sns

# Data sets
data3 = [
    [25, 21, 23, 24, 11, 9, 3, 5, 0, 0],
    [14, 14, 20, 17, 10, 10, 2, 2, 1, 0],
    [19, 22, 20, 8, 11, 13, 2, 6, 0, 0],
    [20, 21, 22, 16, 18, 9, 4, 1, 0, 0],
    [21, 11, 23, 17, 9, 5, 7, 1, 0, 0],
    [25, 10, 15, 6, 8, 3, 2, 1, 0, 0],
    [15, 15, 8, 6, 4, 3, 6, 0, 0, 0],
    [18, 17, 12, 3, 3, 3, 2, 0, 0, 0],
    [3, 6, 0, 3, 0, 0, 3, 0, 0, 0],
]
data2 = [
    [17, 24, 18, 21, 15, 9, 8, 3, 1, 0],
    [22, 19, 20, 13, 15, 9, 4, 0, 0, 0],
    [16, 13, 14, 16, 19, 8, 7, 1, 0, 0],
    [22, 17, 10, 13, 6, 4, 3, 1, 1, 0],
    [11, 27, 10, 12, 2, 7, 1, 3, 3, 0],
    [15, 16, 16, 9, 9, 6, 3, 2, 0, 0],
    [15, 11, 13, 12, 4, 4, 0, 0, 0, 0],
    [8, 4, 6, 9, 9, 3, 6, 0, 3, 0],
    [10, 5, 0, 0, 2, 0, 0, 0, 0, 0],
]
data1 = [
    [15, 15, 20, 18, 15, 19, 25, 13, 1, 0],
    [26, 20, 23, 27, 20, 22, 24, 18, 4, 0],
    [26, 30, 30, 28, 24, 21, 20, 15, 3, 0],
    [26, 27, 24, 28, 24, 24, 10, 12, 7, 0],
    [28, 29, 26, 24, 21, 22, 22, 11, 1, 0],
    [27, 25, 27, 25, 23, 13, 10, 10, 0, 0],
    [28, 30, 28, 26, 23, 10, 6, 3, 0, 0],
    [26, 24, 25, 21, 10, 15, 2, 4, 0, 0],
    [30, 14, 9, 9, 6, 0, 3, 0, 0, 0],
]

# Axis labels
x_labels = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
y_labels = [10, 9, 8, 7, 6, 5, 4, 3, 2]

# Plotting all heatmaps in a single row
fig, axes = plt.subplots(1, 3, figsize=(24, 8), dpi=600)

# Set consistent color range
vmin, vmax = 0, 30

# Titles for each subplot
titles = ["Heatmap - Original", "Heatmap - MTB(FreqRank)", "Heatmap - MTB(###peramaull)"]
data_list = [data1, data2, data3]

# Plot each heatmap
for i in range(3):
    sns.heatmap(
        data_list[i],
        ax=axes[i],
        annot=True,
        fmt="d",
        cmap="coolwarm",
        cbar=(i == 2),  # Only last one has colorbar
        linewidths=0.0,
        xticklabels=x_labels,
        yticklabels=y_labels,
        vmin=vmin,
        vmax=vmax
    )
    axes[i].set_title(titles[i])
    axes[i].set_xlabel("False Positive Percentage")
    axes[i].set_ylabel("Ranking Score")

plt.tight_layout()
output_path = "heatmap_combined_PerammmRanks.png"
plt.savefig(output_path, dpi=600, bbox_inches="tight")
plt.show()

output_path
