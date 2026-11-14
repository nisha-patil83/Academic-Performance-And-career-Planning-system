"""
Database & Domain Schema for EduPlan AI
Exclusively Configured for:
Tatyasaheb Kore Institute of Engineering & Technology, Warananagar (TKIET)
(An Autonomous Institute | Approved by AICTE | Affiliated to Shivaji University, Kolhapur)

Features Verified Student Rosters across:
MCA, Mechanical, Cyber Security, E&TC, CS, CSBS, MBA
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any

# ---------------------------------------------------------------------------
# Institutional Profile: TKIET Warananagar
# ---------------------------------------------------------------------------
INSTITUTE_PROFILE = {
    "name": "Tatyasaheb Kore Institute of Engineering & Technology, Warananagar",
    "short_name": "TKIET, Warananagar",
    "code": "TKIET-WARANA (Autonomous)",
    "location": "Warananagar, Tal. Panhala, Dist. Kolhapur, Maharashtra - 416113",
    "affiliation": "Autonomous Institute | Affiliated to Shivaji University, Kolhapur | NAAC 'A' Grade Accredited",
    "principal": "Dr. K. I. Patil",
    "tpo": "Prof. P. J. Patil",
    "website": "www.tkietwarana.ac.in",
    "email": "principal@tkietwarana.ac.in",
    "tpo_email": "tpo@tkietwarana.ac.in",
    "phone": "+91 2328 224012 / 224013"
}

COLLEGES = [
    {
        "id": "TKIET01",
        "name": "Tatyasaheb Kore Institute of Engineering & Technology, Warananagar",
        "code": "TKIET-WARANA",
        "location": "Warananagar, Tal. Panhala, Dist. Kolhapur, Maharashtra - 416113",
        "affiliation": "Autonomous Institute (Affiliated to Shivaji University, Kolhapur)"
    }
]

# ---------------------------------------------------------------------------
# Verified HOD Roster across the 7 Disciplines
# ---------------------------------------------------------------------------
DEPARTMENTS = [
    {"dept_id": "MCA", "dept_name": "Master of Computer Applications", "hod": "Dr. Shivaleela Arlimatti", "degree": "PG"},
    {"dept_id": "MBA", "dept_name": "Master of Business Administration", "hod": "Dr. Snehal Deshmukh", "degree": "PG"},
    {"dept_id": "CS", "dept_name": "Computer Science & Engineering", "hod": "Dr. Patil Ramgouda B.", "degree": "UG"},
    {"dept_id": "Mechanical", "dept_name": "Mechanical Engineering", "hod": "Dr. Mulik P. V.", "degree": "UG"},
    {"dept_id": "E&TC", "dept_name": "Electronics & Telecommunication", "hod": "Dr. S. T. Jadhav", "degree": "UG"},
    {"dept_id": "CSBS", "dept_name": "Computer Science & Business Systems", "hod": "Dr. Arvind Iyer", "degree": "UG"},
    {"dept_id": "Cyber Security", "dept_name": "Cyber Security Engineering", "hod": "Prof. Rajesh Dhananjay Gade", "degree": "UG"}
]

COURSES = [
    # CS
    {"code": "CS301", "name": "Data Structures & Algorithms", "dept": "CS", "credits": 4, "sem": 3},
    {"code": "CS302", "name": "Database Management Systems", "dept": "CS", "credits": 4, "sem": 3},
    # MCA
    {"code": "MCA401", "name": "Enterprise Java & Cloud Architecture", "dept": "MCA", "credits": 4, "sem": 2},
    {"code": "MCA402", "name": "Full Stack Web Technologies", "dept": "MCA", "credits": 4, "sem": 3},
    # MBA
    {"code": "MBA501", "name": "Financial Analytics & Portfolio Management", "dept": "MBA", "credits": 3, "sem": 2},
    {"code": "MBA502", "name": "Strategic Marketing & Consumer Insights", "dept": "MBA", "credits": 3, "sem": 3},
    # Mechanical
    {"code": "ME401", "name": "Thermodynamics & Heat Transfer", "dept": "Mechanical", "credits": 4, "sem": 4},
    {"code": "ME402", "name": "CAD/CAM & Industrial Automation", "dept": "Mechanical", "credits": 4, "sem": 5},
    # E&TC
    {"code": "ETC301", "name": "Embedded Systems & Microcontrollers", "dept": "E&TC", "credits": 4, "sem": 4},
    {"code": "ETC302", "name": "Wireless Communication & IoT Protocols", "dept": "E&TC", "credits": 4, "sem": 5},
    # CSBS
    {"code": "CSB401", "name": "Business Analytics & Enterprise Systems", "dept": "CSBS", "credits": 4, "sem": 4},
    {"code": "CSB402", "name": "Financial Econometrics & Design Thinking", "dept": "CSBS", "credits": 3, "sem": 5},
    # Cyber Security
    {"code": "CYB401", "name": "Ethical Hacking & Penetration Testing", "dept": "Cyber Security", "credits": 4, "sem": 4},
    {"code": "CYB402", "name": "Applied Cryptography & Network Defense", "dept": "Cyber Security", "credits": 4, "sem": 5}
]

SUBJECT_TOPIC_MAP = {
    # CS
    "Data Structures & Algorithms": ["Dynamic Programming", "Graph Traversal (BFS/DFS)", "Binary Search Trees", "Recursion", "Sorting & Heaps"],
    "Database Management Systems": ["SQL Joins & Subqueries", "Normalization & Normal Forms", "Indexing & B-Trees", "ACID Transactions", "NoSQL Concepts"],
    # MCA
    "Enterprise Java & Cloud Architecture": ["Spring Boot Microservices", "RESTful API Security", "Docker Containerization", "Hibernate ORM", "Kafka Messaging"],
    "Full Stack Web Technologies": ["React Component Lifecycle", "Node.js & Express", "State Management (Redux)", "MongoDB Aggregation", "GraphQL"],
    # MBA
    "Financial Analytics & Portfolio Management": ["DCF Financial Modeling", "Capital Asset Pricing Model", "Financial Ratio Analysis", "Risk & VaR Calculation", "Mergers & Acquisitions"],
    "Strategic Marketing & Consumer Insights": ["Customer Lifetime Value (CLV)", "Brand Positioning", "Digital Funnel Optimization", "Market Segmentation", "Pricing Strategies"],
    # Mechanical
    "Thermodynamics & Heat Transfer": ["Carnot Cycle & Entropy", "Heat Conduction & Convection", "Rankine Power Cycles", "Refrigeration Systems", "Fluid Dynamics Analysis"],
    "CAD/CAM & Industrial Automation": ["SolidWorks 3D Modeling", "Finite Element Analysis (FEA)", "CNC G-Code Programming", "PLC & SCADA Basics", "Additive Manufacturing"],
    # E&TC
    "Embedded Systems & Microcontrollers": ["ARM Cortex Architecture", "UART/SPI/I2C Protocols", "Real-Time OS (RTOS)", "Sensor Interfacing", "Interrupt Handling"],
    "Wireless Communication & IoT Protocols": ["5G Cellular Architecture", "MQTT & CoAP Protocols", "RF Modulation Techniques", "Zigbee & LoRaWAN", "Antenna Signal Processing"],
    # CSBS
    "Business Analytics & Enterprise Systems": ["Predictive Sales Forecasting", "ERP SAP Architecture", "Customer Churn Modeling", "Agile Product Management", "Tableau/Power BI Dashboards"],
    "Financial Econometrics & Design Thinking": ["Time Series Econometrics", "User Journey Mapping", "Design Sprint Prototyping", "Regression Discontinuity", "Behavioral Economics"],
    # Cyber Security
    "Ethical Hacking & Penetration Testing": ["OWASP Top 10 Exploitation", "Network Vulnerability Scanning", "Burp Suite & Metasploit", "Social Engineering Tactics", "Web App Privilege Escalation"],
    "Applied Cryptography & Network Defense": ["RSA & Elliptic Curve Math", "Zero-Trust Firewalls", "SIEM Log Threat Hunting", "TLS/SSL Handshake Protocol", "Malware Reverse Engineering"]
}

# ---------------------------------------------------------------------------
# Corporate Campus Placement Partners at TKIET
# ---------------------------------------------------------------------------
COMPANIES = [
    {
        "company_id": "COMP01",
        "name": "Google",
        "industry": "Big Tech / Cloud",
        "ctc": "28 LPA",
        "min_cgpa": 8.5,
        "max_backlogs": 0,
        "allowed_depts": ["CS", "CSBS", "Cyber Security", "MCA"],
        "role": "Software Development Engineer (SDE-1)",
        "skills_required": ["Data Structures", "Algorithms", "System Design", "Python", "C++"]
    },
    {
        "company_id": "COMP02",
        "name": "Microsoft",
        "industry": "Cloud & AI",
        "ctc": "24 LPA",
        "min_cgpa": 8.0,
        "max_backlogs": 0,
        "allowed_depts": ["CS", "CSBS", "Cyber Security", "MCA", "E&TC"],
        "role": "Azure Cloud / Security Engineer",
        "skills_required": ["Algorithms", "Cloud Computing", "Python", "SQL", "Git"]
    },
    {
        "company_id": "COMP03",
        "name": "Tata Consultancy Services (TCS Digital)",
        "industry": "IT & Business Solutions",
        "ctc": "7.5 LPA",
        "min_cgpa": 7.0,
        "max_backlogs": 1,
        "allowed_depts": ["MCA", "MBA", "CS", "Mechanical", "E&TC", "CSBS", "Cyber Security"],
        "role": "Digital Technology Associate",
        "skills_required": ["Aptitude", "Java", "Python", "SQL", "Analytics"]
    },
    {
        "company_id": "COMP04",
        "name": "Deloitte Consulting",
        "industry": "Strategy, Analytics & Audit",
        "ctc": "12.5 LPA",
        "min_cgpa": 7.5,
        "max_backlogs": 0,
        "allowed_depts": ["MBA", "CSBS", "MCA", "CS"],
        "role": "Technology & Business Consultant",
        "skills_required": ["Business Analytics", "SQL", "Tableau/Power BI", "Communication", "Financial Modeling"]
    },
    {
        "company_id": "COMP05",
        "name": "Tata Motors / L&T Tech",
        "industry": "Automotive, Robotics & Hardware",
        "ctc": "9.5 LPA",
        "min_cgpa": 7.0,
        "max_backlogs": 0,
        "allowed_depts": ["Mechanical", "E&TC"],
        "role": "Mechatronics & Automation Specialist",
        "skills_required": ["SolidWorks/CAD", "Embedded Systems", "Thermodynamics", "PLC/SCADA", "Python"]
    },
    {
        "company_id": "COMP06",
        "name": "Palo Alto Networks",
        "industry": "Cybersecurity & Defense",
        "ctc": "18 LPA",
        "min_cgpa": 7.8,
        "max_backlogs": 0,
        "allowed_depts": ["Cyber Security", "CS", "E&TC"],
        "role": "Security Operations & SOC Analyst",
        "skills_required": ["Ethical Hacking", "Networking", "SIEM/Wireshark", "Cryptography", "Linux"]
    },
    {
        "company_id": "COMP07",
        "name": "Accenture Strategy",
        "industry": "Global Operations & Technology",
        "ctc": "8.5 LPA",
        "min_cgpa": 6.8,
        "max_backlogs": 1,
        "allowed_depts": ["MCA", "MBA", "CS", "Mechanical", "E&TC", "CSBS", "Cyber Security"],
        "role": "Associate Strategy Consultant",
        "skills_required": ["Verbal Ability", "Analytical Reasoning", "Problem Solving", "Excel/PowerPoint"]
    }
]

# ---------------------------------------------------------------------------
# Specific Student Rosters for TKIET Warananagar
# ---------------------------------------------------------------------------
STUDENT_ROSTER_CONFIG = {
    "MCA": [
        "Nisha Patil", "Sanika Jadhav", "Rutuja Mohite", "Omkar Mali", "Arman Mulla",
        "Aadarsha Dongale", "Abhijit Sonavane", "Akshada Patil", "Darshana Patil",
        "Vaishnavi Nikam", "Paras Adake", "Saniya Ambekari", "Abhijit Jounjal",
        "Prathamesh Joshi", "Sneha Kulkarni", "Rohit Chougule"
    ],
    "Mechanical": [
        "Varun Divate", "Sandesh Mane", "Harshvardhan Gaikwad", "Rohita Patil",
        "Saurabh Patil", "Pratik Deshmukh", "Vinayak Kamble", "Digvijay Powar",
        "Aditya Mohite", "Sanket Shinde", "Abhishek Yadav", "Omkar Chavan"
    ],
    "Cyber Security": [
        "Sushama Patil", "Shreya Shinde", "Arjun Patil", "Tejaswini Yadav",
        "Omkar Ghatage", "Sayali Salunkhe", "Aniket Kadam", "Snehal Chougule",
        "Akash Mane", "Pooja Pawar", "Ketan Patil", "Rohit Jadhav"
    ],
    "E&TC": [
        "Shreyash Rokade", "Shrinath Patil", "Sanika Patil", "Sakshi Patil",
        "Rohan Ghorpade", "Ruturaj Bhosale", "Shraddha Mane", "Digvijay Patil",
        "Priyanka Salokhe", "Ketan Powar", "Vaibhav Jadhav", "Sneha Shinde"
    ],
    "CS": [
        "Sayali Patil", "Ashwini Munde", "Ashwini Patil", "Prathamesh Patil",
        "Aarav Sharma", "Tanvi More", "Suraj Bhosale", "Radhika Kulkarni",
        "Shreyas Kamble", "Neha Kadam", "Aditya Jadhav", "Pooja Patil"
    ],
    "CSBS": [
        "Priya Chavan", "Siddharth Chopra", "Tanmay Patil", "Shruti Kadam",
        "Harshwardhan Deshmukh", "Ananya Kulkarni", "Karan Shinde", "Aditi Mane"
    ],
    "MBA": [
        "Rohan Bhosale", "Ishita Ghorpade", "Sourabh Salunkhe", "Pranita Patil",
        "Sanket Powar", "Meera Kadam", "Omkar Deshmukh", "Tejas Patil"
    ]
}

# ---------------------------------------------------------------------------
# Master Dataset Generation with Specific Named Students
# ---------------------------------------------------------------------------
def generate_master_records(n_students: int = 175, seed: int = 42) -> Dict[str, pd.DataFrame]:
    np.random.seed(seed)
    
    student_records = []
    academic_records = []
    learning_records = []
    training_records = []
    placement_records = []

    branch_career_map = {
        "CS": ("Full Stack Software Engineer", ["Python", "Java", "SQL", "Git", "React", "Data Structures", "Algorithms", "Operating Systems"]),
        "MCA": ("Enterprise Cloud & Web Architect", ["Java", "Spring Boot", "React", "SQL", "Docker", "REST APIs", "Microservices", "Kubernetes"]),
        "MBA": ("Product & Business Strategy Manager", ["Business Strategy", "Financial Modeling", "Market Research", "Agile", "Tableau/Power BI", "Corporate Finance", "Business Analytics"]),
        "Mechanical": ("Robotics & CAD Automation Engineer", ["SolidWorks", "AutoCAD", "CATIA", "ANSYS / FEA", "Thermodynamics", "PLC/SCADA", "CNC Programming", "Python"]),
        "E&TC": ("Embedded Systems & IoT Architect", ["Embedded C", "Microcontrollers", "RTOS", "IoT Protocols", "Networking", "PCB Design", "ARM Architecture", "Python"]),
        "CSBS": ("FinTech & Enterprise Solutions Analyst", ["Python", "Business Analytics", "SQL", "ERP Systems", "Data Structures", "Financial Econometrics", "Design Thinking", "Tableau"]),
        "Cyber Security": ("Cyber Defense & SOC Security Analyst", ["Ethical Hacking", "Networking", "Linux", "SIEM/Wireshark", "Cryptography", "Burp Suite", "Firewalls", "Python"])
    }

    branch_subject_map = {
        "CS": ("Data Structures & Algorithms", "Database Management Systems"),
        "MCA": ("Enterprise Java & Cloud Architecture", "Full Stack Web Technologies"),
        "MBA": ("Financial Analytics & Portfolio Management", "Strategic Marketing & Consumer Insights"),
        "Mechanical": ("Thermodynamics & Heat Transfer", "CAD/CAM & Industrial Automation"),
        "E&TC": ("Embedded Systems & Microcontrollers", "Wireless Communication & IoT Protocols"),
        "CSBS": ("Business Analytics & Enterprise Systems", "Financial Econometrics & Design Thinking"),
        "Cyber Security": ("Ethical Hacking & Penetration Testing", "Applied Cryptography & Network Defense")
    }

    student_counter = 1001

    for branch, names in STUDENT_ROSTER_CONFIG.items():
        sem_choice = 3 if branch in ["MCA", "MBA"] else 7
        target_career, default_skills = branch_career_map[branch]
        sub_pair = branch_subject_map[branch]
        weak_sub, strong_sub = sub_pair

        for name in names:
            s_id = f"TKIET{student_counter}"
            student_counter += 1

            clean_name = name.lower().replace(" ", ".")
            email = f"{clean_name}@{branch.lower().replace(' ', '')}.tkietwarana.ac.in"
            college = "Tatyasaheb Kore Institute of Engineering & Technology, Warananagar"

            # Top performance tuning for key students like Nisha Patil
            is_top_student = ("nisha" in clean_name or "aadarsha" in clean_name or "sayali" in clean_name or "varun" in clean_name or "sushama" in clean_name or "shreyash" in clean_name)
            
            if is_top_student:
                prior_cgpa = float(np.clip(np.random.normal(loc=9.1, scale=0.3), 8.8, 9.85).round(2))
                attendance = float(np.clip(np.random.normal(loc=94, scale=2.5), 90, 99).round(1))
                study_hours = float(np.clip(np.random.normal(loc=22, scale=3.0), 18, 32).round(1))
                backlogs = 0
            else:
                prior_cgpa = float(np.clip(np.random.normal(loc=7.8, scale=0.9), 5.2, 9.5).round(2))
                attendance = float(np.clip(np.random.normal(loc=81, scale=9.5), 48, 98).round(1))
                study_hours = float(np.clip(np.random.normal(loc=15, scale=4.5), 4, 30).round(1))
                backlogs = int(np.random.choice([0, 1, 2], p=[0.80, 0.15, 0.05]))

            midterm_pct = float(np.clip((prior_cgpa * 9.5) + (attendance * 0.12) + np.random.normal(0, 3.5), 42, 99).round(1))
            online_test_avg = float(np.clip((midterm_pct * 0.88) + np.random.normal(3, 3.0), 38, 98).round(1))

            predicted_sgpa = float(np.clip((prior_cgpa * 0.6) + (attendance * 0.02) + (midterm_pct * 0.025) - (backlogs * 0.35) + np.random.normal(0, 0.15), 4.0, 9.9).round(2))

            if predicted_sgpa < 6.0 or backlogs >= 2 or attendance < 65:
                risk_tier = "High Risk"
            elif predicted_sgpa < 7.2 or backlogs == 1 or attendance < 75:
                risk_tier = "Moderate Risk"
            else:
                risk_tier = "Low Risk"

            weak_topics = list(np.random.choice(SUBJECT_TOPIC_MAP[weak_sub], size=min(2, len(SUBJECT_TOPIC_MAP[weak_sub])), replace=False))
            strong_topics = list(np.random.choice(SUBJECT_TOPIC_MAP[strong_sub], size=min(2, len(SUBJECT_TOPIC_MAP[strong_sub])), replace=False))

            n_skills = int(np.clip(prior_cgpa * 0.7 + (study_hours * 0.12), 3, len(default_skills)))
            student_skills = list(np.random.choice(default_skills, size=n_skills, replace=False))
            career_match_score = float(np.clip((len(student_skills) / len(default_skills)) * 82 + (prior_cgpa * 1.8), 48, 98).round(1))

            aptitude_score = float(np.clip(np.random.normal(loc=74, scale=11) + (prior_cgpa * 2), 40, 99).round(1))
            coding_score = float(np.clip(np.random.normal(loc=72, scale=13) + (len(student_skills) * 3), 30, 100).round(1))
            tech_mcq = float(np.clip((aptitude_score * 0.4 + coding_score * 0.6) + np.random.normal(0, 3.5), 35, 98).round(1))
            verbal_ability = float(np.clip(np.random.normal(loc=77, scale=10), 50, 98).round(1))
            mock_interview_score = float(np.clip((coding_score * 0.4 + verbal_ability * 0.3 + prior_cgpa * 3), 45, 99).round(1))
            t_attendance = float(np.clip(attendance * 0.96 + np.random.normal(2, 2.5), 55, 100).round(1))

            placement_readiness = (coding_score * 0.35) + (aptitude_score * 0.25) + (prior_cgpa * 4.0) + (mock_interview_score * 0.15)
            
            eligible_comps = [c for c in COMPANIES if branch in c["allowed_depts"]]
            chosen_comp = np.random.choice(eligible_comps)

            if placement_readiness >= 75 and backlogs == 0 and prior_cgpa >= 7.6:
                placed_status = "Placed - Tier 1 (Dream)"
                applied_company = chosen_comp["name"]
                package = chosen_comp["ctc"]
                interview_stage = "Selected / Offer Rolled Out"
            elif placement_readiness >= 63 and backlogs <= 1 and prior_cgpa >= 6.8:
                placed_status = "Placed - Tier 2 (Core)"
                applied_company = chosen_comp["name"]
                package = "7.5 to 9.5 LPA"
                interview_stage = "Selected / Offer Rolled Out"
            elif placement_readiness >= 52:
                placed_status = "In Progress / Active Drives"
                applied_company = chosen_comp["name"]
                package = "Pending"
                interview_stage = np.random.choice(["Technical Round 2", "HR Round", "Aptitude Cleared"])
            else:
                placed_status = "Needs Upskilling"
                applied_company = "Not Eligible Yet"
                package = "N/A"
                interview_stage = "Training Required"

            resume_score = int(np.clip((len(student_skills) * 11) + (prior_cgpa * 3.2) + np.random.normal(0, 3), 54, 98))

            student_records.append({
                "student_id": s_id,
                "name": name,
                "email": email,
                "college": college,
                "department": branch,
                "current_sem": sem_choice,
                "prior_cgpa": prior_cgpa,
                "backlogs": backlogs
            })

            academic_records.append({
                "student_id": s_id,
                "attendance_rate": attendance,
                "study_hours_per_week": study_hours,
                "midterm_pct": midterm_pct,
                "online_test_avg": online_test_avg,
                "predicted_sgpa": predicted_sgpa,
                "risk_tier": risk_tier,
                "weak_subject": weak_sub,
                "weak_topics": ", ".join(weak_topics),
                "strong_subject": strong_sub,
                "strong_topics": ", ".join(strong_topics)
            })

            learning_records.append({
                "student_id": s_id,
                "target_career": target_career,
                "career_match_score": career_match_score,
                "skills": ", ".join(student_skills),
                "weak_topics_to_remedy": ", ".join(weak_topics),
                "study_hours_allocated": study_hours + 4.0,
                "suggested_resource": f"Masterclass & Interactive Labs on {weak_topics[0]}",
                "practice_questions_due": len(weak_topics) * 15
            })

            training_records.append({
                "student_id": s_id,
                "training_attendance": t_attendance,
                "aptitude_score": aptitude_score,
                "coding_score": coding_score,
                "tech_mcq_score": tech_mcq,
                "verbal_score": verbal_ability,
                "mock_interview_score": mock_interview_score,
                "training_rank": 0
            })

            placement_records.append({
                "student_id": s_id,
                "placement_status": placed_status,
                "target_company": applied_company,
                "interview_round": interview_stage,
                "offered_package": package,
                "resume_ats_score": resume_score,
                "placement_readiness_pct": round(placement_readiness, 1)
            })

    df_students = pd.DataFrame(student_records)
    df_academic = pd.DataFrame(academic_records)
    df_learning = pd.DataFrame(learning_records)
    df_training = pd.DataFrame(training_records)
    df_placement = pd.DataFrame(placement_records)

    df_training["training_rank"] = (df_training["coding_score"] * 0.4 + df_training["aptitude_score"] * 0.3 + df_training["mock_interview_score"] * 0.3).rank(ascending=False).astype(int)

    df_master = df_students.merge(df_academic, on="student_id") \
                           .merge(df_learning, on="student_id") \
                           .merge(df_training, on="student_id") \
                           .merge(df_placement, on="student_id")

    return {
        "students": df_students,
        "academic": df_academic,
        "learning": df_learning,
        "training": df_training,
        "placement": df_placement,
        "master_unified": df_master
    }
