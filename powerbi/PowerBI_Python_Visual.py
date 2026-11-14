# =========================================================================
# POWER BI PYTHON VISUAL: FEATURE IMPORTANCE & STUDY CORRELATION
# In Power BI Desktop:
# 1. Add a "Python Visual" from the Visualizations pane.
# 2. Drag into Values: 'study_hours_per_week', 'ml_predicted_gpa', 'ml_predicted_risk', 'attendance_rate'
# 3. Paste the code below into the Python script editor.
# =========================================================================

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# The following code to create a dataframe and remove duplicated rows is always executed in Power BI:
# dataset = pandas.DataFrame(study_hours_per_week, ml_predicted_gpa, ml_predicted_risk, attendance_rate)
# dataset = dataset.drop_duplicates()

plt.figure(figsize=(9, 5), dpi=150)
sns.set_theme(style="whitegrid")

palette = {
    "Low Risk": "#10B981",       # Emerald Green
    "Moderate Risk": "#F59E0B",  # Amber
    "High Risk": "#EF4444"       # Coral Red
}

# Scatter plot with bubble size representing attendance
ax = sns.scatterplot(
    data=dataset,
    x="study_hours_per_week",
    y="ml_predicted_gpa",
    hue="ml_predicted_risk",
    size="attendance_rate",
    sizes=(40, 200),
    palette=palette,
    alpha=0.85,
    edgecolor="none"
)

# Trend line
sns.regplot(
    data=dataset,
    x="study_hours_per_week",
    y="ml_predicted_gpa",
    scatter=False,
    ax=ax,
    color="#1E3A8A",
    line_kws={"linewidth": 2, "linestyle": "--"}
)

plt.title("Study Hours vs. ML Predicted Final GPA (Bubble Size = Attendance %)", fontsize=13, weight="bold", color="#1E293B", pad=12)
plt.xlabel("Weekly Study Hours", fontsize=11, weight="bold", color="#475569")
plt.ylabel("Predicted Final GPA (Scale 1.0 - 4.0)", fontsize=11, weight="bold", color="#475569")
plt.ylim(1.5, 4.1)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.show()
