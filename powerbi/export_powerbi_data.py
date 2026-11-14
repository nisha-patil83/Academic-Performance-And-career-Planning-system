"""
Power BI Data Exporter & Model Pipeline
Generates clean, structured CSV files optimized for Power BI Desktop data modeling,
including Star Schema tables and a unified flat reporting dataset.
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure parent directory is in path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import generate_student_dataset, AcademicModelSuite, recommend_career_paths, CAREER_DATABASE

def export_powerbi_datasets():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(output_dir, "datasets")
    os.makedirs(data_dir, exist_ok=True)

    print("1. Generating Cohort & Running ML Inference...")
    df_cohort = generate_student_dataset(n_samples=1200, random_state=42)
    
    suite = AcademicModelSuite()
    suite.fit(df_cohort)

    # Compute ML predictions and career recommendations for each student
    predicted_gpas = []
    predicted_risks = []
    risk_low_probs = []
    risk_mod_probs = []
    risk_high_probs = []
    top_careers = []
    top_career_matches = []
    top_missing_skills = []

    # Map department to typical baseline skill profiles
    dept_skill_map = {
        "Data Science & AI": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
        "Computer Science": ["Python", "JavaScript/TypeScript", "Git", "SQL", "Algorithms"],
        "Software Engineering": ["React", "JavaScript/TypeScript", "Node.js", "Git", "SQL"],
        "Information Technology": ["Linux", "Networking", "SQL", "Cloud Computing", "Docker"],
        "Electrical Engineering": ["Python", "Linux", "Networking", "Problem Solving", "C++"]
    }

    for idx, row in df_cohort.iterrows():
        student_input = {
            "prior_gpa": row["prior_gpa"],
            "attendance_rate": row["attendance_rate"],
            "study_hours_per_week": row["study_hours_per_week"],
            "midterm_score": row["midterm_score"],
            "assignment_completion_rate": row["assignment_completion_rate"],
            "past_failures": row["past_failures"],
            "stress_level": row["stress_level"]
        }
        pred = suite.predict_student(student_input)
        predicted_gpas.append(pred["predicted_gpa"])
        predicted_risks.append(pred["predicted_risk"])
        probs = pred["risk_probabilities"]
        risk_low_probs.append(probs.get("Low Risk", 0.0))
        risk_mod_probs.append(probs.get("Moderate Risk", 0.0))
        risk_high_probs.append(probs.get("High Risk", 0.0))

        # Career recommendation
        base_skills = dept_skill_map.get(row["department"], ["Python", "SQL"])
        # Some student skill variation
        if row["study_hours_per_week"] > 16:
            base_skills = base_skills + ["Docker", "AWS"]
        
        recs = recommend_career_paths(student_skills=base_skills, current_gpa=pred["predicted_gpa"], top_n=1)
        if recs:
            top_rec = recs[0]
            top_careers.append(top_rec["title"])
            top_career_matches.append(top_rec["match_score"])
            top_missing_skills.append(", ".join(top_rec["skills_missing"][:3]))
        else:
            top_careers.append("General Software Engineer")
            top_career_matches.append(50.0)
            top_missing_skills.append("None")

    df_cohort["ml_predicted_gpa"] = predicted_gpas
    df_cohort["ml_predicted_risk"] = predicted_risks
    df_cohort["gpa_variance"] = (df_cohort["ml_predicted_gpa"] - df_cohort["prior_gpa"]).round(2)
    df_cohort["risk_prob_low"] = risk_low_probs
    df_cohort["risk_prob_moderate"] = risk_mod_probs
    df_cohort["risk_prob_high"] = risk_high_probs
    df_cohort["recommended_career"] = top_careers
    df_cohort["career_match_score"] = top_career_matches
    df_cohort["key_missing_skills"] = top_missing_skills

    # 1. Export Unified Flat Reporting Table (Easiest for quick drag-and-drop in Power BI)
    unified_csv_path = os.path.join(data_dir, "PowerBI_Academic_Career_Unified.csv")
    df_cohort.to_csv(unified_csv_path, index=False)
    print(f"-> Exported Unified Table: {unified_csv_path}")

    # 2. Export Star Schema Tables (Best Practice for Enterprise Power BI Data Modeling)
    # Dim_Student
    dim_student = df_cohort[["student_id", "name", "department"]].drop_duplicates()
    dim_student_path = os.path.join(data_dir, "Dim_Student.csv")
    dim_student.to_csv(dim_student_path, index=False)

    # Dim_Career
    careers_data = []
    for c in CAREER_DATABASE:
        careers_data.append({
            "career_id": c["id"],
            "career_title": c["title"],
            "domain": c["domain"],
            "avg_salary": c["avg_salary"],
            "target_gpa": c["target_gpa"],
            "core_skills": ", ".join(c["core_skills"])
        })
    dim_career = pd.DataFrame(careers_data)
    dim_career_path = os.path.join(data_dir, "Dim_Career.csv")
    dim_career.to_csv(dim_career_path, index=False)

    # Fact_Academic_Performance
    fact_academic = df_cohort[[
        "student_id", "prior_gpa", "attendance_rate", "study_hours_per_week",
        "midterm_score", "assignment_completion_rate", "past_failures",
        "stress_level", "final_gpa", "ml_predicted_gpa", "ml_predicted_risk",
        "gpa_variance", "risk_prob_high", "recommended_career", "career_match_score"
    ]]
    fact_academic_path = os.path.join(data_dir, "Fact_Academic_Performance.csv")
    fact_academic.to_csv(fact_academic_path, index=False)

    print("Data export complete! Files are ready for Power BI Desktop.")

if __name__ == "__main__":
    export_powerbi_datasets()
