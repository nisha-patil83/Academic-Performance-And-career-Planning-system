"""
Academic Performance & Career Planning System - Core ML Engine
Provides data generation, predictive modeling, and career recommendation algorithms.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Any

# ---------------------------------------------------------
# 1. Career Taxonomy & Knowledge Base (Configured for All 7 Departments)
# ---------------------------------------------------------
CAREER_DATABASE = [
    {
        "id": "full_stack_dev",
        "title": "Full Stack Software Engineer",
        "domain": "Software Engineering",
        "description": "Builds robust end-to-end web applications covering responsive user interfaces, REST/GraphQL APIs, and relational databases.",
        "core_skills": ["Python", "Java", "SQL", "Git", "React", "Data Structures", "Node.js", "REST APIs"],
        "soft_skills": ["Agile Methodology", "Code Review", "Adaptability"],
        "target_gpa": 3.1,
        "avg_salary": "₹10,50,000 / yr",
        "recommended_courses": ["Data Structures & Algorithms", "Database Management Systems", "Full Stack Web Technologies", "Cloud Computing"],
        "certifications": ["Meta Full-Stack Engineer Certificate", "AWS Certified Developer - Associate", "Oracle Certified Java Associate"],
        "capstone_ideas": ["Collaborative Real-time Whiteboard Platform", "Campus Placement & Hackathon Management Portal"]
    },
    {
        "id": "enterprise_cloud_architect",
        "title": "Enterprise Cloud & Web Architect",
        "domain": "Enterprise Software",
        "description": "Architects scalable enterprise backend systems, Spring Boot microservices, containerized deployments, and resilient cloud architectures.",
        "core_skills": ["Java", "Spring Boot", "React", "SQL", "Docker", "REST APIs", "Microservices", "Kubernetes"],
        "soft_skills": ["Architectural Vision", "Code Review", "Agile Collaboration"],
        "target_gpa": 3.2,
        "avg_salary": "₹12,00,000 / yr",
        "recommended_courses": ["Enterprise Java & Cloud Architecture", "Microservices Design Patterns", "Distributed Systems", "Cloud Infrastructure"],
        "certifications": ["Oracle Certified Professional Java SE", "Spring Professional Certification", "AWS Certified Solutions Architect"],
        "capstone_ideas": ["Enterprise B2B Supply Chain Portal with Kafka Messaging", "Cloud-Native Banking Microservices with Spring Boot & Docker"]
    },
    {
        "id": "robotics_cad_engineer",
        "title": "Robotics & CAD Automation Engineer",
        "domain": "Mechanical & Robotics",
        "description": "Designs precision 3D CAD models, performs finite element simulations, programs industrial automation PLCs, and develops robotic systems.",
        "core_skills": ["SolidWorks", "AutoCAD", "CATIA", "ANSYS / FEA", "Thermodynamics", "PLC/SCADA", "CNC Programming", "Python"],
        "soft_skills": ["Spatial Reasoning", "Safety Standards Compliance", "Analytical Problem Solving"],
        "target_gpa": 3.1,
        "avg_salary": "₹9,50,000 / yr",
        "recommended_courses": ["CAD/CAM & Industrial Automation", "Thermodynamics & Heat Transfer", "Finite Element Analysis", "Robotics & Mechatronics"],
        "certifications": ["Certified SOLIDWORKS Professional (CSWP)", "Autodesk Certified Professional (AutoCAD/Inventor)", "Siemens PLC Automation Certified"],
        "capstone_ideas": ["Autonomous Mobile Robot (AGV) for Warehouse Logistics", "FEA Structural & Thermal Optimization of EV Battery Pack Enclosure"]
    },
    {
        "id": "cyber_defense_analyst",
        "title": "Cyber Defense & SOC Security Analyst",
        "domain": "Cybersecurity",
        "description": "Monitors enterprise networks, conducts vulnerability assessments, investigates threats in SIEMs, and implements zero-trust defense architectures.",
        "core_skills": ["Ethical Hacking", "Networking", "Linux", "SIEM/Wireshark", "Cryptography", "Burp Suite", "Firewalls", "Python"],
        "soft_skills": ["Incident Investigation", "Risk Mitigation", "Attention to Detail"],
        "target_gpa": 3.1,
        "avg_salary": "₹11,00,000 / yr",
        "recommended_courses": ["Ethical Hacking & Penetration Testing", "Applied Cryptography & Network Defense", "Computer Networks", "Digital Forensics"],
        "certifications": ["Certified Ethical Hacker (CEH)", "CompTIA Security+", "Cisco Certified CyberOps Associate"],
        "capstone_ideas": ["AI-Driven Network Intrusion Detection & Real-time SIEM Dashboard", "Zero-Trust Microsegmentation for Campus Network Infrastructure"]
    },
    {
        "id": "embedded_iot_architect",
        "title": "Embedded Systems & IoT Architect",
        "domain": "Embedded & IoT",
        "description": "Develops real-time firmware, microcontrollers (ARM Cortex, ESP32), low-power IoT wireless protocols, and hardware sensor interfaces.",
        "core_skills": ["Embedded C", "Microcontrollers", "RTOS", "IoT Protocols", "Networking", "PCB Design", "Python", "ARM Architecture"],
        "soft_skills": ["Hardware Debugging", "Low-Power Optimization", "Cross-disciplinary Communication"],
        "target_gpa": 3.1,
        "avg_salary": "₹10,50,000 / yr",
        "recommended_courses": ["Embedded Systems & Microcontrollers", "Wireless Communication & IoT Protocols", "Real-Time Operating Systems", "VLSI Design"],
        "certifications": ["ARM Certified Engineer", "Embedded Linux Development (Linux Foundation)", "AWS Certified IoT Specialist"],
        "capstone_ideas": ["Industrial IoT Edge Gateway with FreeRTOS & LoRaWAN", "Smart Agricultural Telemetry Mesh Network with Solar Energy Harvesting"]
    },
    {
        "id": "fintech_enterprise_analyst",
        "title": "FinTech & Enterprise Solutions Analyst",
        "domain": "Business & FinTech",
        "description": "Integrates software engineering, business analytics, ERP architecture (SAP), and financial econometrics for technology-driven enterprises.",
        "core_skills": ["Python", "Business Analytics", "SQL", "ERP Systems", "Data Structures", "Financial Econometrics", "Design Thinking", "Tableau"],
        "soft_skills": ["Strategic Reasoning", "User Journey Mapping", "Financial Acumen"],
        "target_gpa": 3.2,
        "avg_salary": "₹11,50,000 / yr",
        "recommended_courses": ["Business Analytics & Enterprise Systems", "Financial Econometrics & Design Thinking", "Data Mining", "FinTech Innovations"],
        "certifications": ["SAP Certified Application Associate", "Tableau Certified Data Analyst", "CFA Institute Investment Foundations"],
        "capstone_ideas": ["High-Frequency Algorithmic Portfolio Risk Simulator", "ERP-Connected Predictive Supply Chain Demand Engine"]
    },
    {
        "id": "product_business_strategist",
        "title": "Product & Business Strategy Manager",
        "domain": "Management & Strategy",
        "description": "Guides business expansion, market research, financial valuation modeling, agile sprints, and corporate technology roadmap planning.",
        "core_skills": ["Financial Modeling", "Business Strategy", "Market Research", "Agile", "Tableau/Power BI", "Corporate Finance", "Business Analytics", "Excel/PowerPoint"],
        "soft_skills": ["Executive Presentation", "Negotiation", "Cross-Functional Leadership"],
        "target_gpa": 3.2,
        "avg_salary": "₹13,00,000 / yr",
        "recommended_courses": ["Financial Analytics & Portfolio Management", "Strategic Marketing & Consumer Insights", "Corporate Strategy", "Managerial Economics"],
        "certifications": ["Project Management Professional (PMP)", "Certified Scrum Product Owner (CSPO)", "Financial Modeling & Valuation Analyst (FMVA)"],
        "capstone_ideas": ["FinTech Market Entry Strategy & 5-Year DCF Valuation Model", "Omnichannel Consumer Acquisition & Lifetime Value Optimization Campaign"]
    },
    {
        "id": "data_scientist",
        "title": "Data Scientist",
        "domain": "Data & AI",
        "description": "Applies statistical analysis, machine learning, and data visualization to uncover patterns and drive decisions.",
        "core_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization", "Pandas", "Scikit-Learn"],
        "soft_skills": ["Critical Thinking", "Problem Solving", "Business Communication"],
        "target_gpa": 3.3,
        "avg_salary": "₹13,50,000 / yr",
        "recommended_courses": ["Advanced Machine Learning", "Probability & Statistics", "Data Mining", "Big Data Analytics"],
        "certifications": ["TensorFlow Developer Certificate", "AWS Certified Machine Learning", "Google Professional Data Engineer"],
        "capstone_ideas": ["Customer Churn Prediction Engine", "Healthcare Outcome Forecasting with Explainable AI"]
    },
    {
        "id": "ml_engineer",
        "title": "Machine Learning Engineer",
        "domain": "Data & AI",
        "description": "Designs, builds, and deploys production machine learning systems, pipelines, and deep learning models.",
        "core_skills": ["Python", "Machine Learning", "Deep Learning", "Docker", "PyTorch/TensorFlow", "MLOps", "API Development"],
        "soft_skills": ["System Design", "Collaboration", "Debugging"],
        "target_gpa": 3.4,
        "avg_salary": "₹14,00,000 / yr",
        "recommended_courses": ["Deep Learning & Neural Networks", "Distributed Systems", "Cloud Computing", "Computer Vision / NLP"],
        "certifications": ["Databricks Certified ML Professional", "Azure AI Engineer Associate"],
        "capstone_ideas": ["Real-time Recommendation Pipeline with Kafka & FastAPI", "Computer Vision Quality Control System"]
    },
    {
        "id": "cloud_solutions_architect",
        "title": "Cloud Solutions Architect",
        "domain": "Cloud & Infrastructure",
        "description": "Designs scalable, resilient, and secure cloud environments across enterprise workloads.",
        "core_skills": ["AWS", "Cloud Computing", "Docker", "Kubernetes", "Linux", "Networking", "Terraform"],
        "soft_skills": ["Architectural Vision", "Stakeholder Presentation", "Risk Assessment"],
        "target_gpa": 3.0,
        "avg_salary": "₹14,50,000 / yr",
        "recommended_courses": ["Cloud Computing Architecture", "Computer Networks", "Operating Systems", "Information Security"],
        "certifications": ["AWS Certified Solutions Architect", "Google Cloud Professional Architect", "Microsoft Certified: Azure Solutions Architect"],
        "capstone_ideas": ["Multi-tier Cloud Microservices Infrastructure with Auto-scaling", "Disaster Recovery Pipeline using Terraform"]
    },
    {
        "id": "data_engineer",
        "title": "Data Engineer",
        "domain": "Data & AI",
        "description": "Constructs resilient data extraction, transformation, and warehousing pipelines for big data analytics.",
        "core_skills": ["SQL", "Python", "Data Warehousing", "ETL Pipelines", "Docker", "Apache Spark", "Cloud Computing"],
        "soft_skills": ["Data Governance", "Cross-team Collaboration", "Optimization"],
        "target_gpa": 3.2,
        "avg_salary": "₹12,80,000 / yr",
        "recommended_courses": ["Database Systems", "Distributed Data Systems", "Cloud Data Architectures", "Algorithms"],
        "certifications": ["IBM Data Engineering Professional", "AWS Certified Data Analytics"],
        "capstone_ideas": ["Streaming IoT Telemetry Pipeline with Kafka & Snowflake", "Automated ETL Lakehouse with DBT & Airflow"]
    },
    {
        "id": "ui_ux_frontend",
        "title": "UI/UX & Frontend Design Technologist",
        "domain": "Design & Frontend",
        "description": "Crafts accessible, performant, and delightful digital user interfaces and design systems.",
        "core_skills": ["React", "JavaScript/TypeScript", "CSS/Tailwind", "Figma", "User Research", "Prototyping", "Accessibility"],
        "soft_skills": ["Visual Aesthetics", "Empathy", "Storytelling"],
        "target_gpa": 3.0,
        "avg_salary": "₹9,80,000 / yr",
        "recommended_courses": ["Human-Computer Interaction", "Interactive Web Design", "Cognitive Psychology in UX", "Graphic Design"],
        "certifications": ["Google UX Design Professional Certificate", "Nielsen Norman Group UX Master"],
        "capstone_ideas": ["Accessible Learning Management System Design System", "Smart Health Portal Mobile & Web Interface"]
    }
]

ALL_AVAILABLE_SKILLS = sorted(list({skill for c in CAREER_DATABASE for skill in c["core_skills"]}))
ALL_DOMAINS = sorted(list({c["domain"] for c in CAREER_DATABASE}))

# ---------------------------------------------------------
# 2. Synthetic Dataset Generation
# ---------------------------------------------------------
def generate_student_dataset(n_samples: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """
    Generates a realistic student academic dataset with consistent educational correlations.
    """
    np.random.seed(random_state)
    
    student_ids = [f"STU{1000 + i}" for i in range(n_samples)]
    names = [f"Student_{i+1}" for i in range(n_samples)]
    departments = np.random.choice(
        ["Computer Science", "Data Science & AI", "Information Technology", "Electrical Engineering", "Software Engineering"],
        size=n_samples,
        p=[0.35, 0.25, 0.15, 0.15, 0.10]
    )
    
    # Realistic feature distributions
    attendance = np.clip(np.random.normal(loc=78, scale=12, size=n_samples), 40, 100).round(1)
    study_hours = np.clip(np.random.normal(loc=14, scale=6, size=n_samples), 2, 35).round(1)
    prior_gpa = np.clip(np.random.normal(loc=3.1, scale=0.5, size=n_samples), 1.8, 4.0).round(2)
    assignment_rate = np.clip(np.random.normal(loc=82, scale=14, size=n_samples), 35, 100).round(1)
    midterm_score = np.clip(
        (prior_gpa * 18) + (attendance * 0.25) + (study_hours * 0.8) + np.random.normal(0, 6, n_samples),
        30, 100
    ).round(1)
    
    past_failures = np.random.choice([0, 1, 2, 3], size=n_samples, p=[0.75, 0.16, 0.06, 0.03])
    stress_level = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.1, 0.25, 0.35, 0.2, 0.1])
    
    # Ground truth formula for Final GPA with variance
    gpa_raw = (
        0.35 * prior_gpa +
        0.015 * attendance +
        0.025 * study_hours +
        0.015 * assignment_rate +
        0.012 * midterm_score -
        0.25 * past_failures -
        0.04 * stress_level +
        np.random.normal(0, 0.18, n_samples)
    )
    final_gpa = np.clip(gpa_raw, 1.2, 4.0).round(2)
    
    # Risk Level Categorization
    def categorize_risk(gpa, fail, attend):
        if gpa < 2.5 or fail >= 2 or attend < 60:
            return "High Risk"
        elif gpa < 3.0 or fail == 1 or attend < 75:
            return "Moderate Risk"
        else:
            return "Low Risk"
            
    risk_level = [categorize_risk(g, f, a) for g, f, a in zip(final_gpa, past_failures, attendance)]
    
    df = pd.DataFrame({
        "student_id": student_ids,
        "name": names,
        "department": departments,
        "prior_gpa": prior_gpa,
        "attendance_rate": attendance,
        "study_hours_per_week": study_hours,
        "midterm_score": midterm_score,
        "assignment_completion_rate": assignment_rate,
        "past_failures": past_failures,
        "stress_level": stress_level,
        "final_gpa": final_gpa,
        "risk_level": risk_level
    })
    return df

# ---------------------------------------------------------
# 3. Model Training & Prediction Pipeline
# ---------------------------------------------------------
class AcademicModelSuite:
    def __init__(self):
        self.feature_cols = [
            "prior_gpa",
            "attendance_rate",
            "study_hours_per_week",
            "midterm_score",
            "assignment_completion_rate",
            "past_failures",
            "stress_level"
        ]
        self.gpa_regressor = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
        self.risk_classifier = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
        self.is_trained = False
        self.df_cohort = None

    def fit(self, df: pd.DataFrame):
        self.df_cohort = df.copy()
        X = df[self.feature_cols]
        y_gpa = df["final_gpa"]
        y_risk = df["risk_level"]

        self.gpa_regressor.fit(X, y_gpa)
        self.risk_classifier.fit(X, y_risk)
        self.is_trained = True

    def predict_student(self, student_input: Dict[str, float]) -> Dict[str, Any]:
        """
        Takes student indicators and returns predicted GPA, risk tier, and feature impact diagnostics.
        """
        if not self.is_trained:
            raise RuntimeError("Model is not trained. Call fit() first.")

        X_input = pd.DataFrame([student_input])[self.feature_cols]
        predicted_gpa = round(float(self.gpa_regressor.predict(X_input)[0]), 2)
        predicted_gpa = max(1.0, min(4.0, predicted_gpa))

        predicted_risk = self.risk_classifier.predict(X_input)[0]
        risk_probs = self.risk_classifier.predict_proba(X_input)[0]
        class_labels = self.risk_classifier.classes_
        risk_confidence = {label: round(float(prob), 3) for label, prob in zip(class_labels, risk_probs)}

        # Explainability: Feature contribution proxy using deviation from cohort median
        diagnostics = []
        medians = self.df_cohort[self.feature_cols].median()
        
        # Attendance diagnosis
        att_diff = student_input["attendance_rate"] - medians["attendance_rate"]
        if att_diff < -10:
            diagnostics.append(("Attendance", f"Low attendance ({student_input['attendance_rate']}%) is significantly dragging down expected performance.", "negative"))
        elif att_diff > 5:
            diagnostics.append(("Attendance", f"Strong attendance record ({student_input['attendance_rate']}%) actively supports steady GPA.", "positive"))

        # Study hours diagnosis
        hrs_diff = student_input["study_hours_per_week"] - medians["study_hours_per_week"]
        if hrs_diff < -4:
            diagnostics.append(("Study Habits", f"Study hours ({student_input['study_hours_per_week']} hrs/wk) is below cohort average of {medians['study_hours_per_week']} hrs/wk.", "negative"))
        elif hrs_diff > 4:
            diagnostics.append(("Study Habits", f"High study volume ({student_input['study_hours_per_week']} hrs/wk) provides strong buffer for exams.", "positive"))

        # Assignments diagnosis
        asg_diff = student_input["assignment_completion_rate"] - medians["assignment_completion_rate"]
        if asg_diff < -15:
            diagnostics.append(("Assignment Consistency", f"Assignment completion ({student_input['assignment_completion_rate']}%) represents an immediate vulnerability.", "negative"))
        
        # Past failures
        if student_input["past_failures"] > 0:
            diagnostics.append(("Course Backlogs", f"Existing course backlogs ({int(student_input['past_failures'])}) increase academic strain.", "negative"))

        return {
            "predicted_gpa": predicted_gpa,
            "predicted_risk": predicted_risk,
            "risk_probabilities": risk_confidence,
            "diagnostics": diagnostics,
            "feature_importances": dict(zip(self.feature_cols, self.gpa_regressor.feature_importances_.round(4)))
        }

# ---------------------------------------------------------
# 4. Career Recommender & Skill Gap Analysis Engine
# ---------------------------------------------------------
DEPT_DOMAIN_MAP = {
    "Mechanical": ["Mechanical & Robotics", "Design & Frontend"],
    "Cyber Security": ["Cybersecurity", "Cloud & Infrastructure"],
    "E&TC": ["Embedded & IoT", "Cloud & Infrastructure"],
    "CSBS": ["Business & FinTech", "Data & AI", "Management & Strategy"],
    "MBA": ["Management & Strategy", "Business & FinTech", "Product & Management"],
    "MCA": ["Enterprise Software", "Software Engineering", "Cloud & Infrastructure"],
    "CS": ["Software Engineering", "Data & AI", "Cloud & Infrastructure"]
}

def recommend_career_paths(
    student_skills: List[str],
    preferred_domain: str = None,
    current_gpa: float = 3.0,
    department: str = None,
    top_n: int = 5
) -> List[Dict[str, Any]]:
    """
    Ranks careers based on Jaccard/Overlap similarity of skills, department/domain alignment, and GPA qualification.
    Computes exact skill gap for each role.
    """
    student_skills_set = set(student_skills)
    recommendations = []

    dept_domains = DEPT_DOMAIN_MAP.get(department, []) if department else []

    for role in CAREER_DATABASE:
        core_set = set(role["core_skills"])
        common_skills = list(student_skills_set.intersection(core_set))
        missing_skills = list(core_set - student_skills_set)

        # Skill match score (0 - 65%)
        skill_score = (len(common_skills) / len(core_set)) * 65 if core_set else 0

        # Department domain bonus (up to 25 points)
        dept_bonus = 25 if (dept_domains and role["domain"] in dept_domains) else 0

        # User preferred domain bonus (up to 10 points)
        pref_domain_bonus = 10 if (preferred_domain and role["domain"] == preferred_domain) else 0

        # GPA factor (up to 10 points)
        gpa_ratio = min(1.0, current_gpa / role["target_gpa"])
        gpa_score = gpa_ratio * 10

        total_match_score = min(99, round(skill_score + dept_bonus + pref_domain_bonus + gpa_score, 1))

        recommendations.append({
            "id": role["id"],
            "title": role["title"],
            "domain": role["domain"],
            "description": role["description"],
            "match_score": total_match_score,
            "skills_matched": common_skills,
            "skills_missing": missing_skills,
            "all_core_skills": role["core_skills"],
            "soft_skills": role["soft_skills"],
            "avg_salary": role["avg_salary"],
            "recommended_courses": role["recommended_courses"],
            "certifications": role["certifications"],
            "capstone_ideas": role["capstone_ideas"]
        })

    # Sort descending by match score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:top_n]
