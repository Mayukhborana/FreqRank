# Re-importing necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns

# Data for the heatmap
data = [
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
# Axis labels
x_labels = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
y_labels = [10, 9, 8, 7, 6, 5, 4, 3, 2]

# Set font scale for better readability
sns.set(font_scale=1.2)

# Create the heatmap with fixed color scale from 0 to 30
plt.figure(figsize=(16, 10), dpi=600)
sns.heatmap(
    data,
    annot=True,
    fmt="d",
    cmap="coolwarm",
    cbar=True,
    linewidths=0.0,
    xticklabels=x_labels,
    yticklabels=y_labels,
    vmin=0,      # Force minimum color scale
    vmax=30      # Force maximum color scale
    
)

# Add axis labels and title
plt.xlabel("False Positive Percentage")
plt.ylabel("Ranking Score")
plt.title("Heatmap Representation")

# Adjust layout and save
plt.tight_layout()
file_path = "/Users/mayukhborana/Work_AI_backdoor/freqrank_and_para/localization/heatmap_PerammmRanks.png"
plt.savefig(file_path, dpi=600, bbox_inches="tight")
plt.show()

file_path
