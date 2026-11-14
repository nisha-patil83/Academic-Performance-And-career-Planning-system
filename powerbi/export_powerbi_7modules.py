"""
Power BI 7-Module Enterprise Exporter
Generates full star-schema and consolidated CSV datasets for TKIET Warananagar
with verified student rosters.
"""

import os
import pandas as pd
from data_manager import generate_master_records, COMPANIES, COURSES, DEPARTMENTS, COLLEGES

def export_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    datasets_dir = os.path.join(base_dir, "datasets")
    os.makedirs(datasets_dir, exist_ok=True)

    print("Generating comprehensive TKIET Warananagar datasets...")
    data = generate_master_records(seed=42)

    df_master = data["master_unified"]
    df_students = data["students"]
    df_academic = data["academic"]
    df_training = data["training"]
    df_placement = data["placement"]
    df_learning = data["learning"]

    # 1. Master Consolidated Table
    df_master.to_csv(os.path.join(datasets_dir, "PowerBI_Enterprise_Unified.csv"), index=False)

    # 2. Fact Tables
    df_academic.to_csv(os.path.join(datasets_dir, "Fact_Academic_Analytics.csv"), index=False)
    df_training.merge(df_placement, on="student_id").to_csv(os.path.join(datasets_dir, "Fact_Training_Placement.csv"), index=False)
    df_learning.to_csv(os.path.join(datasets_dir, "Fact_AI_Learning_Career.csv"), index=False)

    # 3. Dimension Tables
    df_students.to_csv(os.path.join(datasets_dir, "Dim_Students.csv"), index=False)
    pd.DataFrame(COMPANIES).to_csv(os.path.join(datasets_dir, "Dim_Companies.csv"), index=False)
    pd.DataFrame(COURSES).to_csv(os.path.join(datasets_dir, "Dim_Courses.csv"), index=False)
    pd.DataFrame(DEPARTMENTS).to_csv(os.path.join(datasets_dir, "Dim_Departments.csv"), index=False)
    pd.DataFrame(COLLEGES).to_csv(os.path.join(datasets_dir, "Dim_Colleges.csv"), index=False)

    print("Export complete! All 8 enterprise CSV files saved to powerbi/datasets/")

if __name__ == "__main__":
    export_all()
