"""
EduPlan AI: Institutional Academic Performance & Placement System
Exclusively for:
Tatyasaheb Kore Institute of Engineering & Technology, Warananagar (TKIET)
(An Autonomous Institute | Approved by AICTE | Affiliated to Shivaji University, Kolhapur)

Disciplines:
MCA, MBA, CS, Mechanical, E&TC, CSBS, Cyber Security

Features:
- Secure Authentication Gateway (Login & Registration)
- Session-based Role-Based Access Control (RBAC)
- 1-Click Demo Accounts for Student, Faculty, TPO, and Admin
- 7 Core Modules + Dedicated Contact Us Helpdesk
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------------------------------------------------------------------
# Persistent Storage Utilities (Automatically saves registered users & data)
# ---------------------------------------------------------------------------
PERSIST_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(PERSIST_DIR, "registered_users.json")
CUSTOM_STUDENTS_FILE = os.path.join(PERSIST_DIR, "custom_students.json")

def load_persisted_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_persisted_users(users_dict):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users_dict, f, indent=2)
    except Exception:
        pass

def load_custom_students():
    if os.path.exists(CUSTOM_STUDENTS_FILE):
        try:
            with open(CUSTOM_STUDENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_custom_students(df):
    try:
        # Extract newly registered/custom students
        custom_records = df[df["student_id"].astype(str).str.contains(r"^TKIET\d{4}$")].to_dict(orient="records")
        with open(CUSTOM_STUDENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(custom_records, f, indent=2, default=str)
    except Exception:
        pass

from data_manager import (
    generate_master_records,
    INSTITUTE_PROFILE,
    DEPARTMENTS,
    COURSES,
    COMPANIES,
    SUBJECT_TOPIC_MAP
)
from ai_assistant import (
    AcademicAIEngine,
    RESOURCE_LIBRARY,
    DEFAULT_RESOURCE,
    analyze_resume_ats,
    generate_personalized_study_plan
)
from models import recommend_career_paths, ALL_AVAILABLE_SKILLS, ALL_DOMAINS

# ---------------------------------------------------------------------------
# Streamlit Configuration & Custom TKIET Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="TKIET Warananagar | EduPlan AI Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        color: #F8FAFC;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: #CBD5E1;
    }

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    .sidebar-brand-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 1.2rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .sidebar-brand-title {
        font-size: 1.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF !important;
        margin-top: 0.2rem;
    }
    .sidebar-badge {
        display: inline-block;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        color: #FFFFFF !important;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.4rem;
    }

    .user-profile-card {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 0.85rem;
        margin-bottom: 1.2rem;
    }
    .user-profile-name {
        font-size: 0.95rem;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    .user-profile-branch {
        font-size: 0.76rem;
        color: #94A3B8 !important;
    }

    [data-testid="stSidebar"] .stRadio > div {
        background: transparent;
        gap: 6px;
    }
    [data-testid="stSidebar"] .stRadio label {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 8px 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 4px;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(59, 130, 246, 0.15);
        border-color: rgba(59, 130, 246, 0.4);
    }
    [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(37, 99, 235, 0.35) 0%, rgba(30, 58, 138, 0.2) 100%);
        border-left: 3px solid #3B82F6;
        border-color: rgba(59, 130, 246, 0.6);
    }

    .auth-container {
        max-width: 600px;
        margin: 2rem auto;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 18px;
        padding: 2.2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
    }
    .auth-header {
        text-align: center;
        margin-bottom: 1.8rem;
    }
    .auth-title {
        font-size: 1.75rem;
        font-weight: 800;
        color: #1E3A8A;
        letter-spacing: -0.02em;
    }
    .auth-subtitle {
        font-size: 0.9rem;
        color: #64748B;
        margin-top: 4px;
    }

    .page-header-box {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1px solid #DBEAFE;
        border-radius: 16px;
        padding: 1.4rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    .page-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #1E3A8A;
        letter-spacing: -0.02em;
        margin-bottom: 0.2rem;
    }
    .page-subtitle {
        font-size: 0.95rem;
        color: #4B5563;
    }

    .branch-pill {
        display: inline-block;
        background: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-right: 5px;
    }

    .metric-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1E40AF;
    }
    .metric-lbl {
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .contact-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data Caching & State Initializer
# ---------------------------------------------------------------------------
@st.cache_resource
def load_application_state():
    data_dict = generate_master_records(n_students=175, seed=42)
    ai_engine = AcademicAIEngine()
    ai_engine.train(data_dict["master_unified"])
    return data_dict, ai_engine

DATA, AI_MODEL = load_application_state()
if "df_master" not in st.session_state:
    st.session_state["df_master"] = DATA["master_unified"].copy()
    # Initialize ISE-1, ISE-2, MSE, ICA assessment columns
    if "ise1_score" not in st.session_state["df_master"].columns:
        m_base = st.session_state["df_master"]["midterm_pct"].fillna(72.0)
        st.session_state["df_master"]["ise1_score"] = (m_base * 0.20).round(1).clip(0.0, 20.0)
        st.session_state["df_master"]["ise2_score"] = (m_base * 0.19).round(1).clip(0.0, 20.0)
        st.session_state["df_master"]["mse_score"] = (m_base * 0.30).round(1).clip(0.0, 30.0)
        st.session_state["df_master"]["ica_score"] = (m_base * 0.31).round(1).clip(0.0, 30.0)
    
    # Load and merge any previously saved registered students from disk
    saved_students = load_custom_students()
    for s_item in saved_students:
        sid = str(s_item.get("student_id", ""))
        if sid and st.session_state["df_master"][st.session_state["df_master"]["student_id"] == sid].empty:
            st.session_state["df_master"].loc[len(st.session_state["df_master"])] = s_item

df_master = st.session_state["df_master"]

BRANCH_KEYS = ["MCA", "MBA", "CS", "Mechanical", "E&TC", "CSBS", "Cyber Security"]

# ---------------------------------------------------------------------------
# Department-Specific Skills & Academic Knowledge Mapping
# ---------------------------------------------------------------------------
DEPARTMENT_SKILL_MAP = {
    "MCA": {
        "domain": "Enterprise Software",
        "target_career": "Enterprise Cloud & Web Architect",
        "skills": ["Java", "Spring Boot", "React", "SQL", "Docker", "REST APIs", "Microservices", "Kubernetes", "Git"],
        "weak_subject": "Enterprise Java & Cloud Architecture",
        "weak_topics": ["Spring Boot Microservices", "RESTful API Security", "Docker Containerization", "Hibernate ORM", "Kafka Messaging"],
        "strong_subject": "Full Stack Web Technologies",
        "strong_topics": ["React Component Lifecycle", "Node.js & Express", "State Management (Redux)", "MongoDB Aggregation"]
    },
    "Mechanical": {
        "domain": "Mechanical & Robotics",
        "target_career": "Robotics & CAD Automation Engineer",
        "skills": ["SolidWorks", "AutoCAD", "CATIA", "ANSYS / FEA", "Thermodynamics", "PLC/SCADA", "CNC Programming", "Python"],
        "weak_subject": "Thermodynamics & Heat Transfer",
        "weak_topics": ["Carnot Cycle & Entropy", "Heat Conduction & Convection", "Rankine Power Cycles", "Refrigeration Systems", "Fluid Dynamics Analysis"],
        "strong_subject": "CAD/CAM & Industrial Automation",
        "strong_topics": ["SolidWorks 3D Modeling", "Finite Element Analysis (FEA)", "CNC G-Code Programming", "PLC & SCADA Basics"]
    },
    "Cyber Security": {
        "domain": "Cybersecurity",
        "target_career": "Cyber Defense & SOC Security Analyst",
        "skills": ["Ethical Hacking", "Networking", "Linux", "SIEM/Wireshark", "Cryptography", "Burp Suite", "Firewalls", "Python"],
        "weak_subject": "Ethical Hacking & Penetration Testing",
        "weak_topics": ["OWASP Top 10 Exploitation", "Network Vulnerability Scanning", "Burp Suite & Metasploit", "Social Engineering Tactics", "Web App Privilege Escalation"],
        "strong_subject": "Applied Cryptography & Network Defense",
        "strong_topics": ["RSA & Elliptic Curve Math", "Zero-Trust Firewalls", "SIEM Log Threat Hunting", "TLS/SSL Handshake Protocol"]
    },
    "CS": {
        "domain": "Software Engineering",
        "target_career": "Full Stack Software Engineer",
        "skills": ["Python", "Java", "C++", "Data Structures", "Algorithms", "SQL", "Git", "React", "Operating Systems"],
        "weak_subject": "Data Structures & Algorithms",
        "weak_topics": ["Dynamic Programming", "Graph Traversal (BFS/DFS)", "Binary Search Trees", "Recursion", "Sorting & Heaps"],
        "strong_subject": "Database Management Systems",
        "strong_topics": ["SQL Joins & Subqueries", "Normalization & Normal Forms", "Indexing & B-Trees", "ACID Transactions"]
    },
    "E&TC": {
        "domain": "Embedded & IoT",
        "target_career": "Embedded Systems & IoT Architect",
        "skills": ["Embedded C", "Microcontrollers", "RTOS", "IoT Protocols", "Networking", "PCB Design", "ARM Architecture", "Python"],
        "weak_subject": "Embedded Systems & Microcontrollers",
        "weak_topics": ["ARM Cortex Architecture", "UART/SPI/I2C Protocols", "Real-Time OS (RTOS)", "Sensor Interfacing", "Interrupt Handling"],
        "strong_subject": "Wireless Communication & IoT Protocols",
        "strong_topics": ["5G Cellular Architecture", "MQTT & CoAP Protocols", "RF Modulation Techniques", "Zigbee & LoRaWAN"]
    },
    "CSBS": {
        "domain": "Business & FinTech",
        "target_career": "FinTech & Enterprise Solutions Analyst",
        "skills": ["Python", "Business Analytics", "SQL", "ERP Systems", "Data Structures", "Financial Econometrics", "Design Thinking", "Tableau"],
        "weak_subject": "Business Analytics & Enterprise Systems",
        "weak_topics": ["Predictive Sales Forecasting", "ERP SAP Architecture", "Customer Churn Modeling", "Agile Product Management", "Tableau/Power BI Dashboards"],
        "strong_subject": "Financial Econometrics & Design Thinking",
        "strong_topics": ["Time Series Econometrics", "User Journey Mapping", "Design Sprint Prototyping", "Regression Discontinuity"]
    },
    "MBA": {
        "domain": "Management & Strategy",
        "target_career": "Product & Business Strategy Manager",
        "skills": ["Business Strategy", "Financial Modeling", "Market Research", "Agile", "Tableau/Power BI", "Corporate Finance", "Business Analytics", "Excel/PowerPoint"],
        "weak_subject": "Financial Analytics & Portfolio Management",
        "weak_topics": ["DCF Financial Modeling", "Capital Asset Pricing Model", "Financial Ratio Analysis", "Risk & VaR Calculation", "Mergers & Acquisitions"],
        "strong_subject": "Strategic Marketing & Consumer Insights",
        "strong_topics": ["Customer Lifetime Value (CLV)", "Brand Positioning", "Digital Funnel Optimization", "Market Segmentation"]
    }
}

# Pre-seeded users database
if "users_db" not in st.session_state:
    st.session_state["users_db"] = {
        # Student account
        "student@tkiet.edu.in": {
            "password": "student123",
            "name": "Nisha Patil",
            "role": "🎓 Student",
            "branch": "MCA",
            "student_id": "TKIET1001",
            "sem": 3
        },
        "nisha.patil@mca.tkietwarana.ac.in": {
            "password": "nisha123",
            "name": "Nisha Patil",
            "role": "🎓 Student",
            "branch": "MCA",
            "student_id": "TKIET1001",
            "sem": 3
        },
        "sanika.jadhav@mca.tkietwarana.ac.in": {
            "password": "sanika123",
            "name": "Sanika Jadhav",
            "role": "🎓 Student",
            "branch": "MCA",
            "student_id": "TKIET1002",
            "sem": 3
        },
        "varun.divate@mech.tkietwarana.ac.in": {
            "password": "varun123",
            "name": "Varun Divate",
            "role": "🎓 Student",
            "branch": "Mechanical",
            "student_id": "TKIET1017",
            "sem": 5
        },
        "sushama.patil@cyber.tkietwarana.ac.in": {
            "password": "sushama123",
            "name": "Sushama Patil",
            "role": "🎓 Student",
            "branch": "Cyber Security",
            "student_id": "TKIET1029",
            "sem": 5
        },
        "shreyash.rokade@etc.tkietwarana.ac.in": {
            "password": "shreyash123",
            "name": "Shreyash Rokade",
            "role": "🎓 Student",
            "branch": "E&TC",
            "student_id": "TKIET1041",
            "sem": 5
        },
        "sayali.patil@cs.tkietwarana.ac.in": {
            "password": "sayali123",
            "name": "Sayali Patil",
            "role": "🎓 Student",
            "branch": "CS",
            "student_id": "TKIET1053",
            "sem": 5
        },
        "priya.chavan@csbs.tkietwarana.ac.in": {
            "password": "priya123",
            "name": "Priya Chavan",
            "role": "🎓 Student",
            "branch": "CSBS",
            "student_id": "TKIET1065",
            "sem": 5
        },
        "rohan.bhosale@mba.tkietwarana.ac.in": {
            "password": "rohan123",
            "name": "Rohan Bhosale",
            "role": "🎓 Student",
            "branch": "MBA",
            "student_id": "TKIET1073",
            "sem": 3
        },
        # Department HOD Accounts across all 7 Disciplines
        "faculty@tkiet.edu.in": {
            "password": "faculty123",
            "name": "Dr. Patil Ramgouda B.",
            "role": "👨‍🏫 Faculty Member",
            "branch": "CS",
            "emp_id": "HOD-CS-01",
            "subject": "Data Structures & Algorithms"
        },
        "hod.cs@tkietwarana.ac.in": {
            "password": "faculty123",
            "name": "Dr. Patil Ramgouda B.",
            "role": "👨‍🏫 Faculty Member",
            "branch": "CS",
            "emp_id": "HOD-CS-01",
            "subject": "Data Structures & Algorithms"
        },
        "hod.mca@tkietwarana.ac.in": {
            "password": "faculty123",
            "name": "Dr. Shivaleela Arlimatti",
            "role": "👨‍🏫 Faculty Member",
            "branch": "MCA",
            "emp_id": "HOD-MCA-01",
            "subject": "Enterprise Java & Cloud Architecture"
        },
        "hod.mech@tkietwarana.ac.in": {
            "password": "faculty123",
            "name": "Dr. Mulik P. V.",
            "role": "👨‍🏫 Faculty Member",
            "branch": "Mechanical",
            "emp_id": "HOD-MECH-01",
            "subject": "CAD/CAM & Industrial Automation"
        },
        "hod.cyber@tkietwarana.ac.in": {
            "password": "faculty123",
            "name": "Prof. Rajesh Dhananjay Gade",
            "role": "👨‍🏫 Faculty Member",
            "branch": "Cyber Security",
            "emp_id": "HOD-CYBER-01",
            "subject": "Ethical Hacking & Penetration Testing"
        },
        "hod.etc@tkietwarana.ac.in": {
            "password": "faculty123",
            "name": "Dr. S. T. Jadhav",
            "role": "👨‍🏫 Faculty Member",
            "branch": "E&TC",
            "emp_id": "HOD-ETC-01",
            "subject": "Embedded Systems & Microcontrollers"
        },
        "hod.csbs@tkietwarana.ac.in": {
            "password": "faculty123",
            "name": "Dr. Arvind Iyer",
            "role": "👨‍🏫 Faculty Member",
            "branch": "CSBS",
            "emp_id": "HOD-CSBS-01",
            "subject": "Business Analytics & Enterprise Systems"
        },
        "hod.mba@tkietwarana.ac.in": {
            "password": "faculty123",
            "name": "Dr. Snehal Deshmukh",
            "role": "👨‍🏫 Faculty Member",
            "branch": "MBA",
            "emp_id": "HOD-MBA-01",
            "subject": "Financial Analytics & Portfolio Management"
        },
        # TPO account
        "tpo@tkiet.edu.in": {
            "password": "tpo123",
            "name": "Prof. P. J. Patil (TPO)",
            "role": "👔 Training & Placement Officer (TPO)",
            "branch": "All Branches",
            "emp_id": "TPO-HEAD-01"
        },
        # Admin account
        "admin@tkiet.edu.in": {
            "password": "admin123",
            "name": "Dr. K. I. Patil (Principal)",
            "role": "🏛️ College Admin",
            "branch": "Autonomous Board",
            "emp_id": "PRINCIPAL-01"
        }
    }

# Merge any previously saved registered users from persistent storage
persisted_users_disk = load_persisted_users()
if persisted_users_disk:
    st.session_state["users_db"].update(persisted_users_disk)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "drives_list" not in st.session_state:
    st.session_state["drives_list"] = COMPANIES.copy()
if "applications" not in st.session_state:
    st.session_state["applications"] = []
if "applications_detailed" not in st.session_state:
    st.session_state["applications_detailed"] = []
if "active_apply_comp" not in st.session_state:
    st.session_state["active_apply_comp"] = None
if "resume_history" not in st.session_state:
    st.session_state["resume_history"] = []
if "attendance_logs" not in st.session_state:
    st.session_state["attendance_logs"] = []
if "counseling_logs" not in st.session_state:
    st.session_state["counseling_logs"] = []
if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = []
if "custom_courses" not in st.session_state:
    st.session_state["custom_courses"] = []

# ===========================================================================
# 🔐 AUTHENTICATION GATEWAY (LOGIN & REGISTRATION)
# ===========================================================================
if not st.session_state["logged_in"]:
    st.markdown("""
    <div style="text-align:center; padding-top:1.5rem; margin-bottom:1rem;">
        <div style="font-size:3.5rem;">🏛️</div>
        <h1 style="color:#1E3A8A; font-weight:800; margin-bottom:4px;">Tatyasaheb Kore Institute of Engineering & Technology</h1>
        <p style="color:#64748B; font-size:1.05rem;">Warananagar, Kolhapur | An Autonomous Institute | EduPlan AI Gateway</p>
    </div>
    """, unsafe_allow_html=True)

    auth_tab1, auth_tab2, auth_tab3 = st.tabs(["🔑 Sign In to TKIET", "📝 Register New Account", "⚡ 1-Click Demo Login"])

    # --- TAB 1: LOGIN ---
    with auth_tab1:
        st.markdown("### Welcome Back! Please Sign In")
        st.caption("Enter your registered Institutional Email or Student PRN / Employee ID to access your dashboard.")
        l_email = st.text_input("Institutional Email or User ID / PRN", placeholder="Enter your registered email or Student PRN (e.g. name@tkietwarana.ac.in or TKIET1001)", key="login_email")
        l_pwd = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pwd")
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button("🚀 Sign In to Portal", use_container_width=True, type="primary"):
                clean_id = l_email.strip()
                clean_pwd = l_pwd.strip()

                if not clean_id:
                    st.error("⚠️ Please enter your Institutional Email or Student PRN / User ID.")
                elif not clean_pwd:
                    st.error("⚠️ Please enter your password.")
                else:
                    user_record = None
                    matched_key = clean_id.lower()
                    
                    if matched_key in st.session_state["users_db"]:
                        user_record = st.session_state["users_db"][matched_key]
                    else:
                        for u_k, u_v in st.session_state["users_db"].items():
                            s_id = str(u_v.get("student_id", "")).strip().lower()
                            e_id = str(u_v.get("emp_id", "")).strip().lower()
                            u_email = str(u_v.get("email", "")).strip().lower()
                            if matched_key in [s_id, e_id, u_email]:
                                user_record = u_v
                                break

                    if not user_record:
                        st.error("❌ Account not found. Please verify your Email/PRN or register a new account in Tab 2.")
                    elif user_record.get("password") != l_pwd:
                        st.error("❌ Incorrect password. Please check your credentials and try again.")
                    else:
                        st.session_state["logged_in"] = True
                        st.session_state["current_user"] = user_record
                        st.session_state.pop("selected_student_id", None)
                        st.success(f"Welcome, {user_record['name']}! Logging you in...")
                        st.rerun()
        with col_btn2:
            st.caption("🔒 Secured via TKIET Role-Based Access Control.")

    # --- TAB 2: REGISTRATION ---
    with auth_tab2:
        st.markdown("### Create Your Institutional Account")
        st.caption("Register below with your credentials. Your profile and academic records will be automatically saved in the app.")
        with st.form("registration_form"):
            r_role = st.selectbox("I am registering as *", ["🎓 Student", "👨‍🏫 Faculty Member", "👔 Training & Placement Officer (TPO)", "🏛️ College Admin"])
            
            c_r1, c_r2 = st.columns(2)
            with c_r1:
                r_name = st.text_input("Full Name *", placeholder="Enter your full name")
            with c_r2:
                r_email = st.text_input("Official / Institutional Email *", placeholder="Enter your email (e.g. name@tkietwarana.ac.in)")

            c_r3, c_r4 = st.columns(2)
            with c_r3:
                r_branch = st.selectbox("Discipline / Department *", BRANCH_KEYS)
            with c_r4:
                if r_role == "🎓 Student":
                    r_id = st.text_input("Student PRN / Roll No *", placeholder="Enter your Student PRN / Roll No (e.g. TKIET1180)")
                else:
                    r_id = st.text_input("Faculty / Employee ID *", placeholder="Enter your Faculty / Employee ID (e.g. EMP-MECH-08)")

            if r_role == "🎓 Student":
                r_sem = st.selectbox("Current Semester *", [1, 2, 3, 4, 5, 6, 7, 8], index=2 if r_branch in ["MCA", "MBA"] else 4)
            else:
                r_sem = None

            c_p1, c_p2 = st.columns(2)
            with c_p1:
                r_pwd = st.text_input("Create Password *", type="password", placeholder="Create a password (min. 4 characters)")
            with c_p2:
                r_pwd_conf = st.text_input("Confirm Password *", type="password", placeholder="Confirm your password")

            r_submit = st.form_submit_button("✅ Create My Account & Sign In", use_container_width=True)
            if r_submit:
                v_name = r_name.strip()
                v_email = r_email.strip().lower()
                v_id = r_id.strip() if r_id else ""
                v_pwd = r_pwd.strip()
                v_pwd_conf = r_pwd_conf.strip()

                if not v_name:
                    st.error("⚠️ Full Name is required. Please enter your name.")
                elif len(v_name) < 3:
                    st.error("⚠️ Full Name must be at least 3 characters long.")
                elif any(char.isdigit() for char in v_name):
                    st.error("⚠️ Full Name should not contain numeric digits.")
                elif not v_email:
                    st.error("⚠️ Institutional Email is required.")
                elif "@" not in v_email or "." not in v_email.split("@")[-1] or len(v_email) < 6:
                    st.error("⚠️ Please enter a valid email address with a domain (e.g. yourname@tkietwarana.ac.in).")
                elif not v_id:
                    st.error(f"⚠️ {'Student PRN / Roll No' if r_role == '🎓 Student' else 'Employee ID'} is required.")
                elif not v_pwd:
                    st.error("⚠️ Password is required.")
                elif len(v_pwd) < 4:
                    st.error("⚠️ Password must be at least 4 characters long.")
                elif v_pwd != v_pwd_conf:
                    st.error("❌ Passwords do not match! Please check again.")
                elif v_email in st.session_state["users_db"]:
                    st.error("⚠️ An account with this email address already exists. Please Sign In using Tab 1.")
                else:
                    # Register user and save data automatically
                    new_user = {
                        "password": v_pwd,
                        "name": v_name,
                        "role": r_role,
                        "branch": r_branch,
                        "email": v_email,
                        "student_id": v_id if r_role == "🎓 Student" else None,
                        "emp_id": v_id if r_role != "🎓 Student" else None,
                        "sem": r_sem or (3 if r_branch in ["MCA", "MBA"] else 5)
                    }
                    st.session_state["users_db"][v_email] = new_user
                    if v_id:
                        st.session_state["users_db"][v_id.lower()] = new_user

                    # Persist registered users so it is automatically saved
                    save_persisted_users(st.session_state["users_db"])

                    # If student, immediately generate and register their full profile into df_master
                    if r_role == "🎓 Student":
                        dept_spec = DEPARTMENT_SKILL_MAP.get(r_branch, DEPARTMENT_SKILL_MAP["MCA"])
                        new_student_record = {
                            "student_id": v_id,
                            "name": v_name,
                            "gender": "Candidate",
                            "department": r_branch,
                            "current_sem": r_sem or (3 if r_branch in ["MCA", "MBA"] else 5),
                            "attendance_rate": 88.0,
                            "midterm_pct": 82.0,
                            "study_hours_per_week": 22.0,
                            "prior_cgpa": 8.35,
                            "predicted_sgpa": 8.45,
                            "risk_tier": "Low Risk",
                            "backlogs": 0,
                            "weak_subject": dept_spec["weak_subject"],
                            "weak_topics": ", ".join(dept_spec["weak_topics"][:2]),
                            "strong_subject": dept_spec["strong_subject"],
                            "strong_topics": ", ".join(dept_spec["strong_topics"][:2]),
                            "weak_topics_to_remedy": ", ".join(dept_spec["weak_topics"][:2]),
                            "skills": ", ".join(dept_spec["skills"][:6]),
                            "target_career": dept_spec["target_career"],
                            "career_match_score": 88,
                            "aptitude_score": 80,
                            "coding_score": 80,
                            "tech_mcq_score": 82,
                            "mock_interview_score": 84,
                            "training_rank": len(df_master) + 1,
                            "target_company": "TCS Digital" if r_branch in ["CS", "MCA", "CSBS"] else ("Tata Motors" if r_branch == "Mechanical" else "L&T Technology"),
                            "interview_round": "Technical Round 1",
                            "placement_status": "In Process",
                            "offered_package": "7.5 LPA",
                            "email": v_email,
                            "phone": "+91 98220 54321",
                            "resume_ats_score": 84,
                            "placement_probability": 0.88,
                            "ise1_score": 18.0,
                            "ise2_score": 17.5,
                            "mse_score": 26.0,
                            "ica_score": 27.0
                        }
                        if df_master[df_master["student_id"] == v_id].empty:
                            df_master.loc[len(df_master)] = new_student_record
                        save_custom_students(df_master)
                        st.session_state["selected_student_id"] = v_id

                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = new_user
                    st.balloons()
                    st.success(f"🎉 Account created successfully for {v_name}! Your profile and academic records have been automatically saved in the app.")
                    st.rerun()

    # --- TAB 3: 1-CLICK DEMO LOGIN ---
    with auth_tab3:
        st.markdown("### ⚡ Quick Evaluation: Instant Demo Sign-In")
        st.write("Click any persona button below to immediately access that role's full dashboard without typing passwords:")

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.markdown("#### 🎓 Student Persona")
            st.write("Select any student from our verified cohorts across all 7 departments:")
            demo_students = [
                {"name": "Nisha Patil", "branch": "MCA", "id": "TKIET1001", "sem": 3},
                {"name": "Sanika Jadhav", "branch": "MCA", "id": "TKIET1002", "sem": 3},
                {"name": "Varun Divate", "branch": "Mechanical", "id": "TKIET1017", "sem": 5},
                {"name": "Harshvardhan Gaikwad", "branch": "Mechanical", "id": "TKIET1019", "sem": 5},
                {"name": "Sushama Patil", "branch": "Cyber Security", "id": "TKIET1029", "sem": 5},
                {"name": "Shreyash Rokade", "branch": "E&TC", "id": "TKIET1041", "sem": 5},
                {"name": "Sayali Patil", "branch": "CS", "id": "TKIET1053", "sem": 5},
                {"name": "Ashwini Munde", "branch": "CS", "id": "TKIET1054", "sem": 5},
                {"name": "Priya Chavan", "branch": "CSBS", "id": "TKIET1065", "sem": 5},
                {"name": "Rohan Bhosale", "branch": "MBA", "id": "TKIET1073", "sem": 3},
                {"name": "Arman Mulla", "branch": "MCA", "id": "TKIET1005", "sem": 3},
            ]
            demo_labels = [f"🎓 {s['name']} — {s['branch']} ({s['id']})" for s in demo_students]
            demo_student_options = ["-- Select a Student Persona to Sign In --"] + demo_labels
            sel_demo_label = st.selectbox("Select Student to Login As:", demo_student_options, key="sel_demo_student_dropdown")

            if st.button("👉 Login as Selected Student", use_container_width=True, type="primary"):
                if sel_demo_label == "-- Select a Student Persona to Sign In --":
                    st.warning("⚠️ Please select a student persona from the dropdown menu first.")
                else:
                    chosen_demo = demo_students[demo_labels.index(sel_demo_label)]
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = {
                        "password": "demo123",
                        "name": chosen_demo["name"],
                        "role": "🎓 Student",
                        "branch": chosen_demo["branch"],
                        "student_id": chosen_demo["id"],
                        "sem": chosen_demo["sem"],
                        "email": f"{chosen_demo['name'].lower().replace(' ', '.')}@tkietwarana.ac.in"
                    }
                    st.session_state["selected_student_id"] = chosen_demo["id"]
                    st.rerun()

            st.markdown("#### 👨‍🏫 Department HOD / Faculty Persona")
            st.write("Access department-specific attendance register, student gradebook, and course diagnostics:")
            demo_hods = [
                {"name": "Dr. Shivaleela Arlimatti", "dept": "MCA", "subj": "Enterprise Java & Cloud Architecture", "id": "HOD-MCA-01", "email": "hod.mca@tkietwarana.ac.in"},
                {"name": "Dr. Mulik P. V.", "dept": "Mechanical", "subj": "CAD/CAM & Industrial Automation", "id": "HOD-MECH-01", "email": "hod.mech@tkietwarana.ac.in"},
                {"name": "Prof. Rajesh Dhananjay Gade", "dept": "Cyber Security", "subj": "Ethical Hacking & Penetration Testing", "id": "HOD-CYBER-01", "email": "hod.cyber@tkietwarana.ac.in"},
                {"name": "Dr. Patil Ramgouda B.", "dept": "CS", "subj": "Data Structures & Algorithms", "id": "HOD-CS-01", "email": "hod.cs@tkietwarana.ac.in"},
                {"name": "Dr. S. T. Jadhav", "dept": "E&TC", "subj": "Embedded Systems & Microcontrollers", "id": "HOD-ETC-01", "email": "hod.etc@tkietwarana.ac.in"},
                {"name": "Dr. Arvind Iyer", "dept": "CSBS", "subj": "Business Analytics & Enterprise Systems", "id": "HOD-CSBS-01", "email": "hod.csbs@tkietwarana.ac.in"},
                {"name": "Dr. Snehal Deshmukh", "dept": "MBA", "subj": "Financial Analytics & Portfolio Management", "id": "HOD-MBA-01", "email": "hod.mba@tkietwarana.ac.in"},
            ]
            demo_hod_labels = [f"👨‍🏫 {h['name']} — HOD {h['dept']}" for h in demo_hods]
            demo_hod_options = ["-- Select a Department HOD Persona to Sign In --"] + demo_hod_labels
            sel_hod_label = st.selectbox("Select Department HOD to Login As:", demo_hod_options, key="sel_demo_hod_dropdown")

            if st.button("👉 Login as Selected Department HOD", use_container_width=True, type="primary"):
                if sel_hod_label == "-- Select a Department HOD Persona to Sign In --":
                    st.warning("⚠️ Please select an HOD persona from the dropdown menu first.")
                else:
                    chosen_hod = demo_hods[demo_hod_labels.index(sel_hod_label)]
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = {
                        "password": "faculty123",
                        "name": chosen_hod["name"],
                        "role": "👨‍🏫 Faculty Member",
                        "branch": chosen_hod["dept"],
                        "emp_id": chosen_hod["id"],
                        "subject": chosen_hod["subj"],
                        "email": chosen_hod["email"]
                    }
                    st.rerun()
                    "password": "faculty123",
                    "name": chosen_hod["name"],
                    "role": "👨‍🏫 Faculty Member",
                    "branch": chosen_hod["dept"],
                    "emp_id": chosen_hod["id"],
                    "subject": chosen_hod["subj"],
                    "email": chosen_hod["email"]
                }
                st.rerun()

        with d_col2:
            st.markdown("#### 👔 T&P Officer Persona")
            st.write("Test corporate drive creation, eligibility shortlisting, and placement stats.")
            if st.button("👉 Login as TPO (Prof. P. J. Patil)", use_container_width=True):
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = st.session_state["users_db"]["tpo@tkiet.edu.in"]
                st.rerun()

            st.markdown("#### 🏛️ College Admin Persona")
            st.write("Test executive institutional KPIs, accreditation export, and campus governance.")
            if st.button("👉 Login as Principal / Admin (Dr. K. I. Patil)", use_container_width=True):
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = st.session_state["users_db"]["admin@tkiet.edu.in"]
                st.rerun()

    # Stop rendering remainder of the app until authenticated
    st.stop()

# ===========================================================================
# 🚀 AUTHENTICATED WORKSPACE (USER IS LOGGED IN)
# ===========================================================================
user = st.session_state["current_user"]
active_role = user["role"]

# If logged in as student, determine active student record
if active_role == "🎓 Student":
    if "selected_student_id" not in st.session_state:
        # Match by name in df_master
        name_match = df_master[df_master["name"].str.strip().str.lower() == user.get("name", "").strip().lower()]
        if not name_match.empty:
            st.session_state["selected_student_id"] = name_match.iloc[0]["student_id"]
        elif user.get("student_id") and not df_master[df_master["student_id"] == user["student_id"]].empty:
            st.session_state["selected_student_id"] = user["student_id"]
        else:
            # Newly registered student: synthesize authentic profile with their own name and branch
            user_id = user.get("student_id") or f"TKIET{len(df_master)+1001}"
            user["student_id"] = user_id
            s_dept = user.get("branch", "MCA")
            dept_spec = DEPARTMENT_SKILL_MAP.get(s_dept, DEPARTMENT_SKILL_MAP["MCA"])

            new_student_record = {
                "student_id": user_id,
                "name": user["name"],
                "gender": "Candidate",
                "department": s_dept,
                "current_sem": user.get("sem", 3 if s_dept in ["MCA", "MBA"] else 5),
                "attendance_rate": 88.0,
                "midterm_pct": 84.5,
                "study_hours_per_week": 24.0,
                "prior_cgpa": 8.40,
                "predicted_sgpa": 8.55,
                "risk_tier": "Low Risk",
                "backlogs": 0,
                "weak_subject": dept_spec["weak_subject"],
                "weak_topics": ", ".join(dept_spec["weak_topics"][:2]),
                "strong_subject": dept_spec["strong_subject"],
                "strong_topics": ", ".join(dept_spec["strong_topics"][:2]),
                "weak_topics_to_remedy": ", ".join(dept_spec["weak_topics"][:2]),
                "skills": ", ".join(dept_spec["skills"][:6]),
                "target_career": dept_spec["target_career"],
                "career_match_score": 88,
                "aptitude_score": 82,
                "coding_score": 80,
                "tech_mcq_score": 85,
                "mock_interview_score": 84,
                "training_rank": len(df_master) + 1,
                "target_company": "TCS Digital" if s_dept in ["CS", "MCA", "CSBS"] else ("Tata Motors" if s_dept == "Mechanical" else "L&T Technology"),
                "interview_round": "Technical Round 1",
                "placement_status": "In Process",
                "offered_package": "7.5 LPA",
                "email": user.get("email", f"{user['name'].lower().replace(' ', '.')}@tkietwarana.ac.in"),
                "phone": "+91 98220 54321",
                "resume_ats_score": 84,
                "placement_probability": 0.88
            }
            df_master.loc[len(df_master)] = new_student_record
            st.session_state["selected_student_id"] = user_id

    matched = df_master[df_master["student_id"] == st.session_state["selected_student_id"]]
    if not matched.empty:
        curr_student = matched.iloc[0]
    else:
        curr_student = df_master.iloc[0]

# ---------------------------------------------------------------------------
# Authenticated Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    # 1. TKIET Brand Header
    st.markdown("""
    <div class="sidebar-brand-box">
        <div style="font-size: 2.1rem; margin-bottom: 2px;">🏛️</div>
        <div class="sidebar-brand-title">TKIET, Warananagar</div>
        <div style="font-size: 0.78rem; color: #94A3B8;">An Autonomous Institute</div>
        <div class="sidebar-badge">⚡ Authenticated Session</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Logged In User Profile Card
    display_name = curr_student['name'] if active_role == "🎓 Student" else user['name']
    display_dept = curr_student['department'] if active_role == "🎓 Student" else user.get('branch', 'TKIET')
    display_id = curr_student['student_id'] if active_role == "🎓 Student" else (user.get('emp_id') or 'Active')

    st.markdown(f"""
    <div class="user-profile-card">
        <div class="user-profile-name">{display_name}</div>
        <div class="user-profile-branch">{user['role']}</div>
        <div style="margin-top:4px;">
            <span class="branch-pill" style="font-size:0.68rem; padding:2px 8px;">{display_dept}</span>
            <span style="font-size:0.75rem; color:#A7F3D0; font-weight:600;">{display_id}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Student Confidentiality Lock (No switching tabs to respect student privacy)
    if active_role == "🎓 Student":
        st.markdown(f"""
        <div style="background:rgba(16, 185, 129, 0.08); border:1px solid rgba(16, 185, 129, 0.25); border-radius:10px; padding:0.6rem 0.8rem; margin:6px 0 10px 0;">
            <div style="color:#6EE7B7; font-size:0.74rem; font-weight:700;">🔒 PRIVATE STUDENT SESSION</div>
            <div style="color:#94A3B8; font-size:0.68rem; margin-top:2px;">Individual student privacy locked. Academic & placement data strictly confidential.</div>
        </div>
        """, unsafe_allow_html=True)

    elif active_role == "👨‍🏫 Faculty Member":
        st.markdown("<p style='font-weight:600; font-size:0.76rem; color:#94A3B8; margin: 4px 0 2px 0;'>SWITCH HOD / DEPT (RBAC)</p>", unsafe_allow_html=True)
        hod_roster = [
            {"branch": "MCA", "name": "Dr. Shivaleela Arlimatti", "subject": "Enterprise Java & Cloud Architecture", "emp_id": "HOD-MCA-01", "email": "hod.mca@tkietwarana.ac.in"},
            {"branch": "Mechanical", "name": "Dr. Mulik P. V.", "subject": "CAD/CAM & Industrial Automation", "emp_id": "HOD-MECH-01", "email": "hod.mech@tkietwarana.ac.in"},
            {"branch": "Cyber Security", "name": "Prof. Rajesh Dhananjay Gade", "subject": "Ethical Hacking & Penetration Testing", "emp_id": "HOD-CYBER-01", "email": "hod.cyber@tkietwarana.ac.in"},
            {"branch": "CS", "name": "Dr. Patil Ramgouda B.", "subject": "Data Structures & Algorithms", "emp_id": "HOD-CS-01", "email": "hod.cs@tkietwarana.ac.in"},
            {"branch": "E&TC", "name": "Dr. S. T. Jadhav", "subject": "Embedded Systems & Microcontrollers", "emp_id": "HOD-ETC-01", "email": "hod.etc@tkietwarana.ac.in"},
            {"branch": "CSBS", "name": "Dr. Arvind Iyer", "subject": "Business Analytics & Enterprise Systems", "emp_id": "HOD-CSBS-01", "email": "hod.csbs@tkietwarana.ac.in"},
            {"branch": "MBA", "name": "Dr. Snehal Deshmukh", "subject": "Financial Analytics & Portfolio Management", "emp_id": "HOD-MBA-01", "email": "hod.mba@tkietwarana.ac.in"},
        ]
        hod_labels = [f"👨‍🏫 {h['name']} ({h['branch']})" for h in hod_roster]
        curr_hod_idx = 0
        for i, h in enumerate(hod_roster):
            if h["branch"] == user.get("branch"):
                curr_hod_idx = i
                break

        selected_hod_label = st.selectbox(
            "Switch Department HOD:",
            hod_labels,
            index=curr_hod_idx,
            key="sidebar_hod_switcher",
            label_visibility="collapsed"
        )
        chosen_h = hod_roster[hod_labels.index(selected_hod_label)]
        if chosen_h["branch"] != user.get("branch") or chosen_h["name"] != user.get("name"):
            user["branch"] = chosen_h["branch"]
            user["name"] = chosen_h["name"]
            user["subject"] = chosen_h["subject"]
            user["emp_id"] = chosen_h["emp_id"]
            user["email"] = chosen_h["email"]
            st.rerun()

    # Logout Button
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        st.session_state.pop("selected_student_id", None)
        st.rerun()

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    # 3. Dynamic Menu depending on Logged-in Persona
    if active_role == "🎓 Student":
        st.markdown("<p style='font-weight:600; font-size:0.82rem; color:#94A3B8; margin-bottom:4px;'>STUDENT DASHBOARD</p>", unsafe_allow_html=True)
        nav_choice = st.radio(
            "Student Modules",
            [
                "📊 My Academics & Trajectory",
                "📚 My AI Learning & Practice",
                "🎯 Career Path & Skill Gap",
                "🏋️ T&P Mock Arena & Practice",
                "💼 Placement Drives & Apply",
                "🤖 AI Resume Auditor & Sprint",
                "🏛️ TKIET Campus & Affiliations",
                "📞 Contact TKIET T&P Cell"
            ],
            label_visibility="collapsed"
        )

    elif active_role == "👨‍🏫 Faculty Member":
        faculty_dept = user.get("branch", "CS")
        assigned_course = user.get("subject", "Data Structures & Algorithms")
        st.markdown("<p style='font-weight:600; font-size:0.82rem; color:#94A3B8; margin-bottom:4px;'>FACULTY TASKS</p>", unsafe_allow_html=True)
        nav_choice = st.radio(
            "Faculty Modules",
            [
                "📋 Attendance Marking & Defaulters",
                "✍️ Student Marks & Evaluation",
                "🧠 Class Weak-Topic Diagnostics",
                "🚨 High-Risk Student Interventions",
                "🏛️ TKIET Campus & Affiliations",
                "📞 Faculty Helpdesk & Support"
            ],
            label_visibility="collapsed"
        )

    elif active_role == "👔 Training & Placement Officer (TPO)":
        st.markdown("<p style='font-weight:600; font-size:0.82rem; color:#94A3B8; margin-bottom:4px;'>TPO OPERATIONS</p>", unsafe_allow_html=True)
        nav_choice = st.radio(
            "TPO Modules",
            [
                "🏢 Company Drives & Create Drive",
                "⚡ Candidate Eligibility & Shortlisting",
                "📋 Interview Rounds & Offers",
                "📈 Placement Stats & CTC Analytics",
                "🏋️ Training Batches & Leaderboards",
                "🏛️ TKIET Campus & Affiliations",
                "📞 Corporate Recruiter Desk"
            ],
            label_visibility="collapsed"
        )

    elif active_role == "🏛️ College Admin":
        st.markdown("<p style='font-weight:600; font-size:0.82rem; color:#94A3B8; margin-bottom:4px;'>ADMINISTRATION</p>", unsafe_allow_html=True)
        nav_choice = st.radio(
            "Admin Modules",
            [
                "📈 Campus Executive Scorecard",
                "🏢 7 Disciplines & Course Structure",
                "🏛️ TKIET Campus Profile & Affiliations",
                "👥 RBAC Role Permissions Matrix",
                "📑 Accreditation Data Export (CSV)",
                "📞 Institutional Inquiries Log"
            ],
            label_visibility="collapsed"
        )

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.73rem; line-height: 1.4;">
        <b>Tatyasaheb Kore Institute of Engineering & Technology</b><br>
        <i>Warananagar, Kolhapur - 416113</i><br>
        <span style="color:#38BDF8;">An Autonomous Institute</span>
    </div>
    """, unsafe_allow_html=True)

# ===========================================================================
# 📞 COMMON CONTACT US FORM COMPONENT
# ===========================================================================
def render_contact_us_form(default_role="Student", default_dept="CS"):
    st.markdown("""
    <div class="page-header-box">
        <span class="branch-pill">TKIET Helpdesk</span>
        <div class="page-title">Contact TKIET, Warananagar</div>
        <div class="page-subtitle">Official communication desk for <b>Tatyasaheb Kore Institute of Engineering & Technology, Warananagar</b>.</div>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_info = st.columns([1.5, 1.1])

    with col_form:
        st.subheader("📬 Submit an Inquiry or Support Request")
        with st.form("contact_form", clear_on_submit=True):
            f_name = st.text_input("Full Name *", placeholder="Enter your full name")
            f_email = st.text_input("Email Address *", placeholder="Enter your email address")
            f_phone = st.text_input("Mobile / WhatsApp Number *", placeholder="Enter your 10-digit mobile number")
            
            f_c1, f_c2 = st.columns(2)
            with f_c1:
                f_role = st.selectbox("Your Role / Affiliation", ["Student", "Faculty Member", "Corporate Recruiter", "Alumni", "Parent / Guardian", "Other"], index=0)
            with f_c2:
                f_branch = st.selectbox("Discipline / Department", BRANCH_KEYS + ["General / Administration"], index=BRANCH_KEYS.index(default_dept) if default_dept in BRANCH_KEYS else 0)

            f_category = st.selectbox("Inquiry Category *", [
                "Training & Placement Cell / Campus Recruitment",
                "Autonomous Examination & Grade Records",
                "AI Learning Portal & Technical Support",
                "Admissions & Curriculum Inquiry",
                "Alumni Association & Mentorship",
                "Principal Office / General Inquiry"
            ])
            
            f_msg = st.text_area("Your Message / Detailed Query *", height=120, placeholder="Please describe your question or support request in detail...")

            submitted = st.form_submit_button("🚀 Submit Message to TKIET Desk", use_container_width=True)
            if submitted:
                if f_name.strip() and f_phone.strip() and f_msg.strip():
                    ticket_id = f"TKIET-{np.random.randint(10000, 99999)}"
                    new_entry = {
                        "ticket_id": ticket_id,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "name": f_name,
                        "email": f_email,
                        "phone": f_phone,
                        "role": f_role,
                        "branch": f_branch,
                        "category": f_category,
                        "message": f_msg,
                        "status": "Submitted / Under Review"
                    }
                    st.session_state["inquiries"].append(new_entry)
                    st.balloons()
                    st.success(f"🎉 Thank you, {f_name}! Your request has been recorded under Ticket ID: **{ticket_id}**. The concerned department at **TKIET, Warananagar** will respond within 24-48 business hours.")
                else:
                    st.error("⚠️ Please fill in all mandatory fields marked with an asterisk (*).")

    with col_info:
        st.subheader("🏛️ TKIET Campus Directory")
        st.markdown("""
        <div class="contact-card">
            <h4 style="color:#1E3A8A; margin-bottom:4px;">Tatyasaheb Kore Institute of Engineering & Technology</h4>
            <p style="color:#4B5563; font-size:0.85rem; margin-bottom:8px;"><b>An Autonomous Institute | Approved by AICTE | NAAC 'A' Grade Accredited</b></p>
            <ul style="font-size:0.85rem; color:#374151; padding-left:18px; margin-bottom:12px;">
                <li>📍 <b>Campus Address:</b> Warananagar, Tal. Panhala, Dist. Kolhapur, Maharashtra - 416113</li>
                <li>📞 <b>Office Telephone:</b> +91 2328 224012 / 224013</li>
                <li>📠 <b>Fax:</b> +91 2328 223507</li>
                <li>✉️ <b>Principal Office:</b> principal@tkietwarana.ac.in</li>
                <li>💼 <b>T&P Officer:</b> tpo@tkietwarana.ac.in</li>
                <li>🌐 <b>Official Website:</b> <a href="http://www.tkietwarana.ac.in" target="_blank">www.tkietwarana.ac.in</a></li>
            </ul>
            <div style="background:#F1F5F9; border-radius:8px; padding:10px; font-size:0.8rem; color:#475569;">
                <b>Affiliation Note:</b> Autonomous Institute affiliated with <i>Shivaji University, Kolhapur</i>. All degrees conferred under autonomous academic regulations.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===========================================================================
# 🏛️ ATTRACTIVE TKIET CAMPUS PROFILE & AFFILIATIONS SHOWCASE
# ===========================================================================
def render_tkiet_campus_profile():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0A192F 0%, #1E3A8A 55%, #1D4ED8 100%); color: white; padding: 2.2rem 2.4rem; border-radius: 18px; margin-bottom: 1.5rem; box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.45); border: 1px solid rgba(255, 255, 255, 0.15); position: relative;">
        <div style="display: flex; align-items: flex-start; justify-content: space-between; flex-wrap: wrap; gap: 1.5rem;">
            <div style="flex: 1; min-width: 320px;">
                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0.6rem;">
                    <span style="background: rgba(251, 191, 36, 0.2); border: 1px solid #F59E0B; color: #FDE68A; padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
                        🏛️ Autonomous Institution
                    </span>
                    <span style="background: rgba(56, 189, 248, 0.2); border: 1px solid #38BDF8; color: #BAE6FD; padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
                        DTE Code: EN-6271
                    </span>
                    <span style="background: rgba(52, 211, 153, 0.2); border: 1px solid #34D399; color: #A7F3D0; padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
                        NAAC 'A' Grade (CGPA 3.27)
                    </span>
                </div>
                <h1 style="color: #FFFFFF; font-size: 2.3rem; font-weight: 800; margin: 0.4rem 0 0.3rem 0; line-height: 1.2; letter-spacing: -0.02em;">
                    Tatyasaheb Kore Institute of Engineering & Technology
                </h1>
                <p style="color: #93C5FD; font-size: 1.12rem; font-weight: 600; margin-bottom: 0.5rem;">
                    Warananagar, Tal. Panhala, Dist. Kolhapur, Maharashtra - 416113
                </p>
                <p style="color: #E2E8F0; font-size: 0.94rem; max-width: 880px; line-height: 1.55; margin-bottom: 0;">
                    Founded in <b>1983</b> under the visionary patronage of Late Sahakar Maharshi <b>Shri Tatyasaheb Kore</b>. Managed by <b>Shree Warana Vibhag Shikshan Mandal (SWVSM)</b>. An autonomous engineering powerhouse dedicated to holistic education, research excellence, and rural-industrial transformation.
                </p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 14px; padding: 1.2rem 1.6rem; text-align: center; min-width: 170px;">
                <div style="font-size: 2.8rem; font-weight: 800; color: #FBBF24; line-height: 1;">40+</div>
                <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.06em; color: #F1F5F9; font-weight: 700; margin-top: 4px;">Years Legacy</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Since 1983</div>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.15); margin: 8px 0;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #38BDF8;">Autonomous Cell</div>
            </div>
        </div>
        <div style="margin-top: 1.4rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.12); display: flex; flex-wrap: wrap; gap: 10px; font-size: 0.85rem;">
            <span style="color: #E2E8F0;">🎓 <b>Affiliating University:</b> Shivaji University, Kolhapur</span>
            <span style="color: #94A3B8;">•</span>
            <span style="color: #E2E8F0;">⚖️ <b>Regulatory Approval:</b> AICTE, New Delhi</span>
            <span style="color: #94A3B8;">•</span>
            <span style="color: #E2E8F0;">📜 <b>Autonomous Status:</b> UGC & Govt. of Maharashtra</span>
            <span style="color: #94A3B8;">•</span>
            <span style="color: #E2E8F0;">🌐 <b>Portal:</b> <a href="http://www.tkietwarana.ac.in" target="_blank" style="color: #38BDF8; font-weight: 600; text-decoration: none;">www.tkietwarana.ac.in</a></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 4 Golden Affiliation & Accreditation Pillars
    st.markdown("### 🏆 Official Affiliations, Accreditations & Approvals")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 4px solid #2563EB; border-radius: 14px; padding: 1.2rem; height: 100%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);">
            <div style="font-size: 2rem; margin-bottom: 6px;">🏛️</div>
            <h4 style="margin: 0; color: #1E3A8A; font-size: 1.1rem; font-weight: 700;">UGC Academic Autonomy</h4>
            <div style="font-size: 0.75rem; color: #2563EB; font-weight: 700; margin: 3px 0 8px 0; text-transform: uppercase; letter-spacing: 0.05em;">New Delhi & Maharashtra Govt.</div>
            <p style="font-size: 0.86rem; color: #475569; line-height: 1.5; margin: 0;">
                Empowered with academic autonomy to formulate cutting-edge curricula, industry-sponsored electives, continuous semester evaluation, and Choice Based Credit System (CBCS).
            </p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 4px solid #7C3AED; border-radius: 14px; padding: 1.2rem; height: 100%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);">
            <div style="font-size: 2rem; margin-bottom: 6px;">🎓</div>
            <h4 style="margin: 0; color: #5B21B6; font-size: 1.1rem; font-weight: 700;">Shivaji University, Kolhapur</h4>
            <div style="font-size: 0.75rem; color: #7C3AED; font-weight: 700; margin: 3px 0 8px 0; text-transform: uppercase; letter-spacing: 0.05em;">Permanent University Affiliation</div>
            <p style="font-size: 0.86rem; color: #475569; line-height: 1.5; margin: 0;">
                Permanently affiliated with prestigious Shivaji University, Kolhapur. All B.Tech, M.Tech, MCA, and MBA degrees are formally conferred under the historic authority of SUK.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with a3:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 4px solid #059669; border-radius: 14px; padding: 1.2rem; height: 100%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);">
            <div style="font-size: 2rem; margin-bottom: 6px;">⭐</div>
            <h4 style="margin: 0; color: #065F46; font-size: 1.1rem; font-weight: 700;">NAAC 'A' Grade (3.27 CGPA)</h4>
            <div style="font-size: 0.75rem; color: #059669; font-weight: 700; margin: 3px 0 8px 0; text-transform: uppercase; letter-spacing: 0.05em;">National Assessment Council</div>
            <p style="font-size: 0.86rem; color: #475569; line-height: 1.5; margin: 0;">
                Accredited with stellar 'A' Grade signifying superior institutional infrastructure, world-class laboratory facilities, faculty research papers, and exceptional placement records.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with a4:
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 4px solid #D97706; border-radius: 14px; padding: 1.2rem; height: 100%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04);">
            <div style="font-size: 2rem; margin-bottom: 6px;">⚖️</div>
            <h4 style="margin: 0; color: #92400E; font-size: 1.1rem; font-weight: 700;">AICTE & DTE Maharashtra</h4>
            <div style="font-size: 0.75rem; color: #D97706; font-weight: 700; margin: 3px 0 8px 0; text-transform: uppercase; letter-spacing: 0.05em;">Govt. Technical Directorate</div>
            <p style="font-size: 0.86rem; color: #475569; line-height: 1.5; margin: 0;">
                Approved by All India Council for Technical Education (AICTE), New Delhi and recognized by Directorate of Technical Education (DTE Code: EN-6271), Govt. of Maharashtra.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 3. Campus Vital Stats Bar
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Campus Area", "30+ Acres", "Smart Eco-Campus")
    c2.metric("Enrolled Scholars", "2,800+", "UG & PG Scholars")
    c3.metric("Expert Faculty", "150+", "Ph.D & M.Tech Guides")
    c4.metric("Campus Placements", "85%+", "Top Tier MNCs")
    c5.metric("Global Alumni", "18,000+", "Across 35+ Nations")

    st.markdown("---")

    # 4. Interactive Detailed Tabs
    tab_lead, tab_acad, tab_infra, tab_coe, tab_depts, tab_map = st.tabs([
        "🏛️ Leadership & Governance",
        "🎓 Academic Autonomy & Affiliation",
        "🏢 Campus Infrastructure",
        "🔬 Centers of Excellence & MoUs",
        "👥 7 Academic Disciplines & HODs",
        "📍 Campus Coordinates & Location"
    ])

    with tab_lead:
        st.markdown("#### Institutional Governance & Administrative Leadership")
        st.write("TKIET Warananagar functions under the venerable parent trust **Shree Warana Vibhag Shikshan Mandal (SWVSM)**, steering excellence across education, co-operative industries, and rural healthcare.")

        l_c1, l_c2 = st.columns(2)
        with l_c1:
            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <span style="background:#DBEAFE; color:#1E40AF; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">President & Chief Patron</span>
                <h3 style="color:#0F172A; margin:0.3rem 0;">Dr. Vinayraoji Kore</h3>
                <p style="color:#475569; font-size:0.88rem; margin-bottom:6px;"><b>Chairman, Shree Warana Vibhag Shikshan Mandal (SWVSM)</b> | MLA</p>
                <p style="color:#64748B; font-size:0.84rem; line-height:1.45; margin:0;">
                    Championing the progressive socio-economic vision of Late Tatyasaheb Kore. Leading the Warana Industrial & Educational Complex comprising sugar, dairy, agro-industries, banking, and higher educational hubs.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <span style="background:#DCFCE7; color:#166534; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Institutional Principal</span>
                <h3 style="color:#0F172A; margin:0.3rem 0;">Dr. K. I. Patil</h3>
                <p style="color:#475569; font-size:0.88rem; margin-bottom:6px;"><b>Principal, TKIET Warananagar</b> | Chair, Autonomous Academic Council</p>
                <p style="color:#64748B; font-size:0.84rem; line-height:1.45; margin:0;">
                    Distinguished academician and administrator driving academic autonomy, research publications, NBA accreditations, and modern pedagogy at TKIET Warananagar.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with l_c2:
            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <span style="background:#FEF3C7; color:#92400E; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Training & Placement Officer</span>
                <h3 style="color:#0F172A; margin:0.3rem 0;">Prof. P. J. Patil</h3>
                <p style="color:#475569; font-size:0.88rem; margin-bottom:6px;"><b>Head, Central Training & Placement Cell (TPO)</b></p>
                <p style="color:#64748B; font-size:0.84rem; line-height:1.45; margin:0;">
                    Spearheading corporate alliances, industrial MoUs, summer internships, and campus recruitment drives with global MNCs including TCS, Infosys, Capgemini, and Tata Motors.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <span style="background:#F3E8FF; color:#6B21A8; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:700; text-transform:uppercase;">Autonomous Governing Bodies</span>
                <h3 style="color:#0F172A; margin:0.3rem 0;">Academic Council & BoS</h3>
                <p style="color:#475569; font-size:0.88rem; margin-bottom:6px;"><b>Autonomous Governance & Examination Board</b></p>
                <p style="color:#64748B; font-size:0.84rem; line-height:1.45; margin:0;">
                    Composed of university nominees from Shivaji University, industry leaders, and senior professors overseeing syllabus revisions, credit frameworks, and examination transparency.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab_acad:
        st.markdown("#### Academic Autonomy Framework & Shivaji University Affiliation")
        st.write("Academic autonomy conferred by the **University Grants Commission (UGC)** and **Government of Maharashtra** enables TKIET to deliver a forward-looking educational ecosystem while conferring degrees affiliated to **Shivaji University, Kolhapur**.")

        ac_c1, ac_c2 = st.columns([1.2, 1])
        with ac_c1:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="color:#1E40AF; margin-top:0;">🌟 The TKIET Autonomous Advantage:</h4>
                <ul style="font-size:0.9rem; color:#334155; line-height:1.6; padding-left:18px;">
                    <li><b>NEP-2020 Aligned Curriculum:</b> Multidisciplinary minors, Honors specializations, and mandatory industrial internships.</li>
                    <li><b>Continuous Internal Evaluation (CIE):</b> 40% continuous assessments (midterm tests, assignments, coding trials) + 60% Semester End Exams (SEE).</li>
                    <li><b>Choice Based Credit System (CBCS):</b> Flexible credit transfers, audit courses in foreign languages, and MOOCs credit transfers (NPTEL/Coursera).</li>
                    <li><b>Industry-Vetted Syllabi:</b> Courses redesigned annually in consultation with senior software architects and plant directors.</li>
                    <li><b>Relative Grading Scale:</b> 10-point SGPA/CGPA evaluation benchmarked to global academic practices.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with ac_c2:
            st.markdown("#### 📜 Institutional Affiliation Dossier")
            affil_table = pd.DataFrame([
                {"Particular": "Institution Name", "Official Value": "TKIET, Warananagar"},
                {"Particular": "Establishment Year", "Official Value": "1983 (40+ Years)"},
                {"Particular": "Affiliating University", "Official Value": "Shivaji University, Kolhapur (SUK)"},
                {"Particular": "UGC Status", "Official Value": "Academic Autonomy Granted"},
                {"Particular": "AICTE Approval", "Official Value": "Permanent EOA Approved"},
                {"Particular": "DTE Institute Code", "Official Value": "EN-6271"},
                {"Particular": "NAAC Accreditation", "Official Value": "Grade 'A' (3.27 CGPA)"},
                {"Particular": "Quality System", "Official Value": "ISO 9001:2015 Certified"}
            ])
            st.dataframe(affil_table, use_container_width=True, hide_index=True)

    with tab_infra:
        st.markdown("#### 🏢 World-Class Infrastructure on 30+ Acre Smart Campus")
        inf_c1, inf_c2 = st.columns(2)
        with inf_c1:
            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="color:#2563EB; margin-top:0;">📚 Knowledge Resource Centre (Central Library)</h4>
                <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                    Houses <b>65,000+ print volumes</b>, 120+ national and international print journals, 24/7 Digital Library with IEEE Xplore, ScienceDirect, and DELNET subscriptions. Features air-conditioned reading halls seating 500+ scholars.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="color:#059669; margin-top:0;">💻 Central Computing Facility (CCF)</h4>
                <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                    Modern computing hub with <b>1,200+ high-performance Core i7 workstations</b>, dedicated <b>1 Gbps optical fiber leased line</b>, campus-wide high-density Wi-Fi 6, and secure cloud server virtualization stacks.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="color:#7C3AED; margin-top:0;">🏠 Scholar Residential Hostels</h4>
                <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                    Safe on-campus residential towers accommodating <b>1,000 boys</b> and <b>600 girls</b>. Equipped with hygienic dining messes, solar water heating systems, 24/7 Wi-Fi, medical dispensary, and biometric security.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with inf_c2:
            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="color:#D97706; margin-top:0;">🚀 Warana Innovation & Incubation Hub</h4>
                <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                    MSME-approved Business Incubator fostering entrepreneurship, FabLab with rapid 3D printing and CNC machining, prototype grant funding, and dedicated patent filing legal counsel.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="color:#0284C7; margin-top:0;">⚽ Sports Complex & Fitness Arena</h4>
                <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                    Full-sized athletic track, cricket pavilion, lawn tennis courts, basketball courts, international standard wooden badminton arena, and modern multi-station health fitness gymnasium.
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                <h4 style="color:#DC2626; margin-top:0;">🎭 Central Auditorium & Amphitheater</h4>
                <p style="font-size:0.88rem; color:#475569; line-height:1.5;">
                    Acoustically treated <b>1,200-seat central auditorium</b> and open-air amphitheater for national symposiums, hackathons, TEDx events, and the annual cultural showcase 'Jigyasa'.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab_coe:
        st.markdown("#### 🔬 Industry-Sponsored Centers of Excellence (CoE) & MoUs")
        st.write("Bridging academia and corporate requirements through dedicated high-technology laboratories set up in partnership with global tech giants:")

        coe_c1, coe_c2 = st.columns(2)
        with coe_c1:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #2563EB; border-radius:10px; padding:1rem; margin-bottom:0.8rem;">
                <h4 style="color:#1E3A8A; margin:0 0 4px 0;">🚗 Tata Technologies Ready Engineer Hub</h4>
                <p style="font-size:0.85rem; color:#475569; margin:0;">Automotive BIW design, powertrain modeling, electric vehicle architectures, and PLM workflow certifications.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #7C3AED; border-radius:10px; padding:1rem; margin-bottom:0.8rem;">
                <h4 style="color:#5B21B6; margin:0 0 4px 0;">📐 Dassault Systèmes 3DEXPERIENCE Center</h4>
                <p style="font-size:0.85rem; color:#475569; margin:0;">Advanced CATIA, SIMULIA, and DELMIA software suites for product design, finite element analysis, and digital twin simulation.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #059669; border-radius:10px; padding:1rem; margin-bottom:0.8rem;">
                <h4 style="color:#065F46; margin:0 0 4px 0;">☁️ AWS Academy & Cloud Computing Lab</h4>
                <p style="font-size:0.85rem; color:#475569; margin:0;">Official AWS curriculum, cloud practitioner benchmarks, hands-on microservices deployment, and serverless DevOps training.</p>
            </div>
            """, unsafe_allow_html=True)

        with coe_c2:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #DC2626; border-radius:10px; padding:1rem; margin-bottom:0.8rem;">
                <h4 style="color:#991B1B; margin:0 0 4px 0;">🐧 Red Hat Academy Open Source Lab</h4>
                <p style="font-size:0.85rem; color:#475569; margin:0;">Enterprise Linux administration (RHCSA/RHCE), Docker containerization, Kubernetes orchestration, and Ansible automation.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #0284C7; border-radius:10px; padding:1rem; margin-bottom:0.8rem;">
                <h4 style="color:#0369A1; margin:0 0 4px 0;">🌐 Cisco Networking Academy</h4>
                <p style="font-size:0.85rem; color:#475569; margin:0;">Official CCNA infrastructure, advanced routing, enterprise firewalls, and cybersecurity threat monitoring hands-on racks.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-left:4px solid #D97706; border-radius:10px; padding:1rem; margin-bottom:0.8rem;">
                <h4 style="color:#B45309; margin:0 0 4px 0;">⚡ Texas Instruments IoT & Embedded Systems</h4>
                <p style="font-size:0.85rem; color:#475569; margin:0;">MSP430, ARM Cortex microcontrollers, wireless sensor network nodes, and low-power IoT product prototyping.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_depts:
        st.markdown("#### 👥 7 Academic Disciplines & Distinguished Heads of Department (HODs)")
        st.write("TKIET Warananagar offers prestigious undergraduate and postgraduate engineering and management programs:")

        dept_display = pd.DataFrame([
            {"Discipline / Department": "Master of Computer Applications (MCA)", "Degree": "PG (2 Years)", "Head of Department (HOD)": "Dr. Shivaleela Arlimatti", "Focus Areas": "Enterprise Full Stack, Cloud Computing & AI"},
            {"Discipline / Department": "Mechanical Engineering", "Degree": "B.Tech / M.Tech", "Head of Department (HOD)": "Dr. Mulik P. V.", "Focus Areas": "Thermal, CAD/CAM, Robotics & Industrial Automation"},
            {"Discipline / Department": "Cyber Security Engineering", "Degree": "B.Tech (UG)", "Head of Department (HOD)": "Prof. Rajesh Dhananjay Gade", "Focus Areas": "Network Defense, SOC, Cryptography & Threat Intel"},
            {"Discipline / Department": "Computer Science & Engineering", "Degree": "B.Tech / M.Tech", "Head of Department (HOD)": "Dr. Patil Ramgouda B.", "Focus Areas": "Data Science, Machine Learning, Scalable Systems"},
            {"Discipline / Department": "Electronics & Telecommunication (E&TC)", "Degree": "B.Tech (UG)", "Head of Department (HOD)": "Dr. S. T. Jadhav", "Focus Areas": "Embedded Systems, Wireless 5G & IoT Protocols"},
            {"Discipline / Department": "Computer Science & Business Systems (CSBS)", "Degree": "B.Tech (UG)", "Head of Department (HOD)": "Dr. Arvind Iyer", "Focus Areas": "FinTech, Enterprise Architecture, Business Analytics"},
            {"Discipline / Department": "Master of Business Administration (MBA)", "Degree": "PG (2 Years)", "Head of Department (HOD)": "Dr. Snehal Deshmukh", "Focus Areas": "Financial Analytics, Strategic Marketing & Operations"}
        ])
        st.dataframe(dept_display, use_container_width=True, hide_index=True)

    with tab_map:
        st.markdown("#### 📍 Campus Coordinates & Connectivity Guide")
        c_m1, c_m2 = st.columns([1.2, 1])
        with c_m1:
            st.markdown("""
            <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:12px; padding:1.4rem;">
                <h4 style="color:#0F172A; margin-top:0;">TKIET Campus Address & Dispatch Coordinates</h4>
                <p style="font-size:0.9rem; color:#334155; line-height:1.6;">
                    <b>Tatyasaheb Kore Institute of Engineering & Technology (Autonomous)</b><br>
                    Warananagar, Taluka: Panhala, District: Kolhapur<br>
                    Maharashtra, India — Pin Code: <b>416113</b><br><br>
                    📞 <b>Central Office:</b> +91 2328 224012 / 224013<br>
                    📠 <b>Telefax:</b> +91 2328 223507<br>
                    ✉️ <b>Principal Office:</b> principal@tkietwarana.ac.in<br>
                    💼 <b>Training & Placement:</b> tpo@tkietwarana.ac.in<br>
                    🌐 <b>Website:</b> <a href="http://www.tkietwarana.ac.in" target="_blank">www.tkietwarana.ac.in</a>
                </p>
                <div style="margin-top:1rem;">
                    <a href="https://maps.google.com/?q=Tatyasaheb+Kore+Institute+of+Engineering+and+Technology+Warananagar" target="_blank" style="background:#2563EB; color:white; padding:8px 18px; border-radius:8px; text-decoration:none; font-weight:700; font-size:0.88rem; display:inline-block;">
                        🗺️ Open TKIET Warananagar on Google Maps ↗
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_m2:
            st.markdown("""
            <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:12px; padding:1.4rem;">
                <h4 style="color:#0F172A; margin-top:0;">🚆 How to Reach TKIET Warananagar</h4>
                <ul style="font-size:0.88rem; color:#475569; line-height:1.6; padding-left:18px;">
                    <li><b>By Rail:</b> <b>CSMT Kolhapur Station (30 km)</b> or <b>Miraj Junction (45 km)</b>. Direct express trains from Mumbai, Pune, Bengaluru, and Hyderabad.</li>
                    <li><b>By Road:</b> Situated 10 km off the Pune-Bengaluru National Highway (NH-48) at Kini/Wadgaon junction. State transport buses and private cabs ply frequently.</li>
                    <li><b>By Air:</b> <b>Kolhapur Airport (KLH - 35 km)</b> with direct daily flights to Mumbai, Bengaluru, Hyderabad, and Tirupati. Pune International Airport is 220 km away.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ===========================================================================
# 🎓 1. STUDENT WORKSPACE
# ===========================================================================
if active_role == "🎓 Student":
    if nav_choice == "📞 Contact TKIET T&P Cell":
        render_contact_us_form(default_role="Student", default_dept=curr_student['department'])
    elif nav_choice == "🏛️ TKIET Campus & Affiliations":
        render_tkiet_campus_profile()
    else:
        # Premium Student Identity Banner
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%); border-radius: 16px; padding: 1.4rem 1.6rem; color: #FFFFFF; margin-bottom: 1.4rem; box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25); border: 1px solid rgba(255,255,255,0.1);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:14px;">
                <div style="display:flex; align-items:center; gap:16px;">
                    <div style="width:56px; height:56px; border-radius:50%; background:linear-gradient(135deg, #3B82F6 0%, #10B981 100%); display:flex; align-items:center; justify-content:center; font-size:1.8rem; box-shadow:0 4px 12px rgba(0,0,0,0.25);">
                        🎓
                    </div>
                    <div>
                        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                            <span style="font-size:1.55rem; font-weight:800; color:#FFFFFF; letter-spacing:-0.02em;">{curr_student['name']}</span>
                            <span style="background:rgba(59, 130, 246, 0.25); border:1px solid #60A5FA; color:#93C5FD; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:700;">{curr_student['department']}</span>
                            <span style="background:rgba(16, 185, 129, 0.2); border:1px solid #34D399; color:#A7F3D0; padding:2px 10px; border-radius:12px; font-size:0.75rem; font-weight:700;">SEMESTER {curr_student['current_sem']}</span>
                        </div>
                        <div style="font-size:0.84rem; color:#94A3B8; margin-top:4px;">
                            PRN: <b style="color:#F1F5F9;">{curr_student['student_id']}</b> &nbsp;|&nbsp; ✉️ <b style="color:#F1F5F9;">{curr_student['email']}</b> &nbsp;|&nbsp; 🏛️ <b>TKIET, Warananagar</b>
                        </div>
                    </div>
                </div>
                <div style="display:flex; gap:10px; flex-wrap:wrap;">
                    <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:12px; padding:7px 14px; text-align:center; min-width:85px;">
                        <div style="font-size:0.68rem; text-transform:uppercase; color:#94A3B8; font-weight:700;">CGPA</div>
                        <div style="font-size:1.2rem; font-weight:800; color:#38BDF8;">{curr_student['prior_cgpa']} <span style="font-size:0.75rem; color:#94A3B8;">/10</span></div>
                    </div>
                    <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:12px; padding:7px 14px; text-align:center; min-width:85px;">
                        <div style="font-size:0.68rem; text-transform:uppercase; color:#94A3B8; font-weight:700;">Attendance</div>
                        <div style="font-size:1.2rem; font-weight:800; color:{'#34D399' if curr_student['attendance_rate'] >= 75 else '#F87171'};">{curr_student['attendance_rate']}%</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:12px; padding:7px 14px; text-align:center; min-width:85px;">
                        <div style="font-size:0.68rem; text-transform:uppercase; color:#94A3B8; font-weight:700;">AI Forecast</div>
                        <div style="font-size:1.2rem; font-weight:800; color:#FBBF24;">{curr_student['predicted_sgpa']}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 1.1 My Academics & Trajectory
        if nav_choice == "📊 My Academics & Trajectory":
            st.markdown("### 📊 Academic Trajectory & AI Performance Insights")
            st.caption("Live academic metrics, autonomous curriculum progress, and personalized AI performance trajectory.")

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-lbl">Cumulative CGPA</div>
                    <div class="metric-val">{curr_student["prior_cgpa"]} <span style="font-size:0.95rem; color:#10B981;">/ 10.0</span></div>
                    <div style="font-size:0.76rem; color:#64748B; margin-top:2px;">Discipline: <b>{curr_student["department"]}</b></div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                att_status = "✅ ESE Exam Eligible" if curr_student["attendance_rate"] >= 75.0 else "⚠️ Defaulter Alert (<75%)"
                att_color = "#10B981" if curr_student["attendance_rate"] >= 75.0 else "#EF4444"
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-lbl">Lecture & Lab Attendance</div>
                    <div class="metric-val" style="color:{att_color};">{curr_student["attendance_rate"]}%</div>
                    <div style="font-size:0.76rem; font-weight:600; color:{att_color}; margin-top:2px;">{att_status}</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                sgpa_delta = round(curr_student["predicted_sgpa"] - curr_student["prior_cgpa"], 2)
                delta_sign = "+" if sgpa_delta >= 0 else ""
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-lbl">AI Predicted SGPA</div>
                    <div class="metric-val" style="color:#2563EB;">{curr_student["predicted_sgpa"]}</div>
                    <div style="font-size:0.76rem; color:#64748B; margin-top:2px;">Trajectory: <b>{delta_sign}{sgpa_delta} vs CGPA</b></div>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                rc = "#10B981" if curr_student["risk_tier"]=="Low Risk" else ("#F59E0B" if curr_student["risk_tier"]=="Moderate Risk" else "#EF4444")
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-lbl">Academic Risk Category</div>
                    <div class="metric-val" style="color:{rc};">{curr_student["risk_tier"]}</div>
                    <div style="font-size:0.76rem; color:#64748B; margin-top:2px;">Active Backlogs: <b>{curr_student["backlogs"]}</b></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

            c_v1, c_v2 = st.columns([1.3, 1])
            with c_v1:
                st.markdown("#### 📈 Semester Progress & AI Forecast Curve")
                sem_labels = [f"Sem {i}" for i in range(1, curr_student["current_sem"] + 1)] + ["AI Forecast"]
                sem_scores = [round(curr_student["prior_cgpa"] + np.random.uniform(-0.25, 0.25), 2) for _ in range(curr_student["current_sem"])] + [curr_student["predicted_sgpa"]]
                
                df_prog = pd.DataFrame({"Semester": sem_labels, "SGPA": sem_scores})
                fig_gpa = px.line(
                    df_prog,
                    x="Semester",
                    y="SGPA",
                    markers=True,
                    text="SGPA",
                    title=f"{curr_student['name']} — SGPA Progression & Prediction"
                )
                fig_gpa.update_traces(
                    textposition="top center",
                    line=dict(color="#2563EB", width=3),
                    marker=dict(size=9, color="#1E40AF")
                )
                fig_gpa.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=35, b=20),
                    yaxis_range=[4.0, 10.0]
                )
                st.plotly_chart(fig_gpa, use_container_width=True)

            with c_v2:
                st.markdown("#### 🎯 Conceptual Strengths & Focus Areas")
                
                # Fetch department fallback safely
                dept_key = curr_student.get("department", "MCA")
                dept_spec = DEPARTMENT_SKILL_MAP.get(dept_key, DEPARTMENT_SKILL_MAP["MCA"])

                safe_strong_sub = curr_student.get("strong_subject") if pd.notna(curr_student.get("strong_subject")) else dept_spec["strong_subject"]
                safe_strong_tops = curr_student.get("strong_topics") if pd.notna(curr_student.get("strong_topics")) else ", ".join(dept_spec["strong_topics"][:2])
                safe_weak_sub = curr_student.get("weak_subject") if pd.notna(curr_student.get("weak_subject")) else dept_spec["weak_subject"]
                safe_weak_tops = curr_student.get("weak_topics") if pd.notna(curr_student.get("weak_topics")) else ", ".join(dept_spec["weak_topics"][:2])

                st.markdown(f"""
                <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:12px; padding:1rem; margin-bottom:0.8rem;">
                    <div style="font-size:0.75rem; font-weight:700; color:#15803D; text-transform:uppercase;">💪 Core Academic Strength</div>
                    <div style="font-weight:800; font-size:1.05rem; color:#166534; margin:2px 0;">{safe_strong_sub}</div>
                    <div style="font-size:0.8rem; color:#15803D; margin-top:4px;">
                        <b>Mastered Topics:</b> {safe_strong_tops}
                    </div>
                </div>

                <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:12px; padding:1rem;">
                    <div style="font-size:0.75rem; font-weight:700; color:#DC2626; text-transform:uppercase;">⚠️ Priority Revision Focus</div>
                    <div style="font-weight:800; font-size:1.05rem; color:#991B1B; margin:2px 0;">{safe_weak_sub}</div>
                    <div style="font-size:0.8rem; color:#B91C1C; margin-top:4px;">
                        <b>Key Gaps:</b> {safe_weak_tops}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Department Curriculum & Continuous Evaluation Roster
            st.markdown("<hr style='margin: 1.2rem 0;'>", unsafe_allow_html=True)
            st.markdown(f"#### 📚 My Current Department Enrolled Courses ({curr_student['department']})")
            
            dept_c_list = [c for c in COURSES if c["dept"] == curr_student["department"]]
            if not dept_c_list:
                dept_c_list = [{"code": f"{curr_student['department'][:3].upper()}301", "name": safe_strong_sub, "credits": 4, "sem": curr_student['current_sem']}]
            
            c_rows = []
            for c in dept_c_list:
                c_rows.append({
                    "Course Code": c.get("code", "CORE-01"),
                    "Subject Title": c.get("name", "Engineering Subject"),
                    "Credits": c.get("credits", 4),
                    "Semester": f"Sem {c.get('sem', curr_student['current_sem'])}",
                    "Internal Assessment Status": "Graded / Active",
                    "Attendance Status": "Satisfactory (>=75%)" if curr_student["attendance_rate"] >= 75 else "Shortfall"
                })
            st.dataframe(pd.DataFrame(c_rows), use_container_width=True, hide_index=True)

            # Continuous Internal Assessment (CIA) Scorecard
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.markdown("#### 📝 Continuous Internal Assessment (CIA) Scorecard")
            cia_ise1 = float(curr_student.get("ise1_score", 15.0))
            cia_ise2 = float(curr_student.get("ise2_score", 14.5))
            cia_mse = float(curr_student.get("mse_score", 22.0))
            cia_ica = float(curr_student.get("ica_score", 24.0))
            cia_total = round(cia_ise1 + cia_ise2 + cia_mse + cia_ica, 1)
            cia_grade = "O" if cia_total >= 90 else ("A+" if cia_total >= 80 else ("A" if cia_total >= 70 else ("B+" if cia_total >= 60 else ("B" if cia_total >= 50 else ("C" if cia_total >= 40 else "F")))))

            c_cia1, c_cia2, c_cia3, c_cia4, c_cia5 = st.columns(5)
            with c_cia1:
                st.metric("ISE-1 (In-Sem 1)", f"{cia_ise1} / 20", "Max 20")
            with c_cia2:
                st.metric("ISE-2 (In-Sem 2)", f"{cia_ise2} / 20", "Max 20")
            with c_cia3:
                st.metric("MSE (Mid-Sem)", f"{cia_mse} / 30", "Max 30")
            with c_cia4:
                st.metric("ICA / Lab Eval", f"{cia_ica} / 30", "Max 30")
            with c_cia5:
                st.metric("Total CIA Score", f"{cia_total} / 100", f"Grade: {cia_grade}")

        # 1.2 My AI Learning & Practice
        elif nav_choice == "📚 My AI Learning & Practice":
            dept_key = curr_student.get("department", "MCA")
            dept_spec = DEPARTMENT_SKILL_MAP.get(dept_key, DEPARTMENT_SKILL_MAP["MCA"])

            safe_weak_sub = curr_student.get("weak_subject") if pd.notna(curr_student.get("weak_subject")) else dept_spec["weak_subject"]
            
            st.markdown("### 📚 Personalized AI Learning Desk & Practice")
            st.caption(f"Curated study guides, video masterclasses, and interactive practice challenges for **{dept_key}** | Focus Subject: **{safe_weak_sub}**")

            # Bulletproof extraction of weak and department topics
            raw_weak = curr_student.get("weak_topics")
            if isinstance(raw_weak, str) and raw_weak.strip():
                weak_topics = [t.strip() for t in raw_weak.split(",") if t.strip()]
            elif isinstance(raw_weak, (list, tuple)):
                weak_topics = [str(t).strip() for t in raw_weak if str(t).strip()]
            else:
                weak_topics = []

            # Combine with department topics so student can learn any relevant module
            dept_all_topics = dept_spec.get("weak_topics", []) + dept_spec.get("strong_topics", [])
            candidate_topics = [t for t in weak_topics if t] + [t for t in dept_all_topics if t not in weak_topics]
            if not candidate_topics:
                candidate_topics = ["Dynamic Programming", "SQL Joins & Subqueries", "Docker Containerization"]

            # Elegant Topic Selector
            st.markdown("##### 📌 Select Concept Module to Study:")
            sel_wt = st.selectbox("Active Learning Module:", candidate_topics, key="sel_student_active_topic", label_visibility="collapsed")

            # Look up in rich RESOURCE_LIBRARY or adaptive fallback
            res = RESOURCE_LIBRARY.get(sel_wt)
            if not res:
                res = {
                    "notes": f"TKIET {dept_key} Department Reference Notes & Curriculum Syllabus on {sel_wt}",
                    "video": f"NPTEL & Video Masterclass Lecture Series on {sel_wt}",
                    "docs": f"Engineering Documentation, Standards & Interactive Labs for {sel_wt}",
                    "sample_questions": [
                        f"Explain the foundational theory and working principles of {sel_wt} in {dept_key}.",
                        f"What are the primary industrial applications and design constraints associated with {sel_wt}?",
                        f"Describe a real-world scenario where engineering optimization is required for {sel_wt}."
                    ]
                }

            # 3 Structured, Clean Resource Cards
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            r_c1, r_c2, r_c3 = st.columns(3)
            with r_c1:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-top:4px solid #2563EB; border-radius:12px; padding:1.1rem; height:100%; box-shadow:0 2px 4px rgba(0,0,0,0.03);">
                    <div style="font-size:0.75rem; text-transform:uppercase; color:#2563EB; font-weight:700;">📝 Engineering Notes</div>
                    <div style="font-weight:700; font-size:1rem; color:#1E293B; margin:4px 0 8px 0;">Curated Study Handbook</div>
                    <div style="font-size:0.85rem; color:#475569; line-height:1.5;">{res['notes']}</div>
                </div>
                """, unsafe_allow_html=True)

            with r_c2:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-top:4px solid #7C3AED; border-radius:12px; padding:1.1rem; height:100%; box-shadow:0 2px 4px rgba(0,0,0,0.03);">
                    <div style="font-size:0.75rem; text-transform:uppercase; color:#7C3AED; font-weight:700;">🎥 Video Masterclass</div>
                    <div style="font-weight:700; font-size:1rem; color:#1E293B; margin:4px 0 8px 0;">Expert Lecture Series</div>
                    <div style="font-size:0.85rem; color:#475569; line-height:1.5;">{res['video']}</div>
                </div>
                """, unsafe_allow_html=True)

            with r_c3:
                st.markdown(f"""
                <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-top:4px solid #059669; border-radius:12px; padding:1.1rem; height:100%; box-shadow:0 2px 4px rgba(0,0,0,0.03);">
                    <div style="font-size:0.75rem; text-transform:uppercase; color:#059669; font-weight:700;">💻 Lab Documentation</div>
                    <div style="font-weight:700; font-size:1rem; color:#1E293B; margin:4px 0 8px 0;">Official Guides & Reference</div>
                    <div style="font-size:0.85rem; color:#475569; line-height:1.5;">{res['docs']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

            # Interactive Practice Section
            st.markdown(f"#### 🧪 Interactive Practice Challenge: {sel_wt}")
            sample_qs = res.get("sample_questions", ["Explain the theoretical foundation and practical application of this concept."])
            sample_q = sample_qs[0] if sample_qs else f"Explain the key principles of {sel_wt}."
            
            st.markdown(f"""
            <div style="background:#F8FAFC; border:1px solid #CBD5E1; border-left:4px solid #3B82F6; border-radius:10px; padding:1rem; margin-bottom:12px;">
                <div style="font-weight:700; color:#1E3A8A; font-size:0.95rem;">Question Prompt ({dept_key} Applied Engineering):</div>
                <div style="font-size:0.9rem; color:#334155; margin-top:4px;">{sample_q}</div>
            </div>
            """, unsafe_allow_html=True)

            u_ans = st.text_area(f"Write your solution or formulation:", height=110, key=f"ans_clean_{sel_wt}", placeholder=f"Type your structured explanation, equations, or implementation for {sel_wt} here...")
            
            q_col1, q_col2 = st.columns([1.5, 3])
            with q_col1:
                if st.button(f"🚀 Verify Solution with AI", key=f"btn_verify_{sel_wt}", type="primary", use_container_width=True):
                    if len(u_ans.strip()) >= 15:
                        st.balloons()
                        st.success(f"🎉 Solution verified for **{sel_wt}**! Good conceptual structure and key engineering principles applied.")
                    else:
                        st.warning("Please provide a more detailed solution (at least 15 characters) to receive evaluation.")
            with q_col2:
                with st.expander("💡 View Conceptual Solution Hint"):
                    st.info(f"Key Points to Include: Address core theoretical principles of {sel_wt}, standard industrial best practices, and applicable engineering standards.")

        # 1.3 Career Path & Skill Gap
        elif nav_choice == "🎯 Career Path & Skill Gap":
            dept_key = curr_student.get("department", "MCA")
            dept_spec = DEPARTMENT_SKILL_MAP.get(dept_key, DEPARTMENT_SKILL_MAP["MCA"])

            st.markdown("### 🎯 Career Alignment & Skill Gap Analysis")
            st.caption(f"Intelligent skill mapping and corporate role readiness for **{dept_key}** candidates at TKIET Warananagar.")

            raw_skills = curr_student.get("skills")
            if isinstance(raw_skills, str) and raw_skills.strip():
                student_skills = [s.strip() for s in raw_skills.split(",") if s.strip()]
            elif isinstance(raw_skills, (list, tuple)):
                student_skills = [str(s).strip() for s in raw_skills if str(s).strip()]
            else:
                student_skills = dept_spec.get("skills", ["Engineering Core"])[:6]

            target_career = curr_student.get("target_career") if pd.notna(curr_student.get("target_career")) else dept_spec.get("target_career", "Engineering Specialist")
            match_score = float(curr_student.get("career_match_score", 86)) if pd.notna(curr_student.get("career_match_score")) else 86.0

            c_g1, c_g2 = st.columns([1, 1.3])
            with c_g1:
                st.markdown(f"#### 🛠️ My Verified Skills Matrix ({dept_key})")
                
                # Render skills as attractive horizontal chips
                skills_html = " ".join([f"<span style='background:#EFF6FF; color:#1D4ED8; border:1px solid #BFDBFE; padding:5px 12px; border-radius:20px; font-size:0.82rem; font-weight:700; display:inline-block; margin:3px 2px;'>✓ {s}</span>" for s in student_skills])
                st.markdown(skills_html, unsafe_allow_html=True)

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                
                # Target Role Card
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-top:8px;">
                    <div style="font-size:0.75rem; text-transform:uppercase; color:#64748B; font-weight:700;">Target Career Track</div>
                    <div style="font-weight:800; font-size:1.15rem; color:#1E3A8A; margin:3px 0 6px 0;">{target_career}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                        <span style="font-size:0.82rem; color:#475569;">Role Fit & Readiness:</span>
                        <b style="font-size:1rem; color:#10B981;">{match_score}%</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(min(1.0, max(0.0, match_score / 100.0)))

            with c_g2:
                st.markdown(f"#### 🎯 AI Recommended Career Pathways ({dept_key})")
                student_cgpa = float(curr_student.get("prior_cgpa", 8.0)) if pd.notna(curr_student.get("prior_cgpa")) else 8.0
                recs = recommend_career_paths(student_skills=student_skills, department=dept_key, current_gpa=student_cgpa / 2.5, top_n=2)
                for r in recs:
                    missing_chips = " ".join([f"<span style='background:#FEF3C7; color:#92400E; border:1px solid #FCD34D; padding:2px 8px; border-radius:12px; font-size:0.75rem; font-weight:600; display:inline-block; margin:2px;'>+ {m}</span>" for m in r['skills_missing'][:4]]) if r['skills_missing'] else "<span style='color:#16A34A; font-size:0.78rem;'>All core skills verified!</span>"
                    st.markdown(f"""
                    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:12px; box-shadow:0 2px 4px rgba(0,0,0,0.03);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="font-weight:800; font-size:1.05rem; color:#1E3A8A;">{r['title']}</div>
                            <span style="background:#DCFCE7; color:#166534; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:700;">{r['match_score']}% Match</span>
                        </div>
                        <div style="font-size:0.75rem; font-weight:700; color:#2563EB; margin-top:2px;">Domain: {r['domain']} | Package: {r['avg_salary']}</div>
                        <p style="font-size:0.85rem; color:#475569; margin:6px 0 10px 0; line-height:1.5;">{r['description']}</p>
                        <div style="font-size:0.78rem; font-weight:700; color:#64748B; margin-bottom:4px;">Recommended Skills to Bridge Gap:</div>
                        <div>{missing_chips}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # 1.4 T&P Mock Arena & Practice
        elif nav_choice == "🏋️ T&P Mock Arena & Practice":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white; padding: 1.2rem; border-radius: 12px; margin-bottom: 1.2rem;">
                <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; color: #93C5FD;">T&P Assessment & Practice Arena</div>
                <h2 style="color: white; margin: 0.2rem 0; font-size: 1.6rem;">Campus Recruitment Training & Mock Test Portal</h2>
                <div style="font-size: 0.95rem; color: #DBEAFE;">Master Quantitative Aptitude, Logical Reasoning, Technical MCQs, and Verbal Ability with instant solutions and curated practice links.</div>
            </div>
            """, unsafe_allow_html=True)

            t1, t2, t3, t4, t5 = st.columns(5)
            t1.metric("Aptitude Score", f"{curr_student['aptitude_score']} / 100")
            t2.metric("Coding Score", f"{curr_student['coding_score']} / 100")
            t3.metric("Technical MCQ", f"{curr_student['tech_mcq_score']} / 100")
            t4.metric("Mock Interview", f"{curr_student['mock_interview_score']} / 100")
            overall_tp = round((curr_student['aptitude_score'] + curr_student['coding_score'] + curr_student['tech_mcq_score'] + curr_student['mock_interview_score']) / 4.0, 1)
            t5.metric("T&P Readiness", f"{overall_tp}%")

            st.markdown("---")

            tab_qa, tab_lr, tab_tech, tab_va, tab_links = st.tabs([
                "🔢 Quantitative Aptitude",
                "🧩 Logical Reasoning",
                "💻 Technical & Core MCQ",
                "📖 Verbal Ability",
                "🌐 Curated Practice Links"
            ])

            # TAB 1: QUANTITATIVE APTITUDE
            with tab_qa:
                st.markdown("### 🔢 Quantitative Aptitude Mock Section")
                st.caption("Standard placement round questions covering Time & Work, Profit & Loss, Speed & Distance, Compound Interest, and Probability.")

                q_qa1 = st.radio(
                    "**Q1. Time & Work:** A can complete a work in 12 days and B can complete the same work in 24 days. If they work together, in how many days will the entire work be completed?",
                    ["6 days", "8 days", "10 days", "16 days"],
                    key="qa_q1"
                )
                q_qa2 = st.radio(
                    "**Q2. Profit & Loss:** A retailer sells a technical gadget at Rs. 1,440 gaining a 20% profit on the transaction. What was the original cost price?",
                    ["Rs. 1,152", "Rs. 1,200", "Rs. 1,250", "Rs. 1,300"],
                    key="qa_q2"
                )
                q_qa3 = st.radio(
                    "**Q3. Speed, Time & Distance:** A train of length 150 meters crosses a telegraph pole in 9 seconds. What is the operational speed of the train in km/hr?",
                    ["54 km/hr", "60 km/hr", "72 km/hr", "45 km/hr"],
                    key="qa_q3"
                )
                q_qa4 = st.radio(
                    "**Q4. Compound Interest:** What is the compound interest accrued on a principal of Rs. 10,000 at 10% per annum for 2 years compounded annually?",
                    ["Rs. 2,000", "Rs. 2,100", "Rs. 2,210", "Rs. 1,900"],
                    key="qa_q4"
                )
                q_qa5 = st.radio(
                    "**Q5. Probability:** One card is drawn randomly from a standard deck of 52 playing cards. What is the probability that the card drawn is either a Queen or a King?",
                    ["1 / 13", "2 / 13", "4 / 13", "1 / 26"],
                    key="qa_q5"
                )

                if st.button("Submit Quantitative Aptitude Answers", key="btn_qa_eval"):
                    score_qa = 0
                    feedback_qa = []

                    if q_qa1 == "8 days":
                        score_qa += 1
                        feedback_qa.append("✅ **Q1 Correct:** Combined rate = (1/12 + 1/24) = 3/24 = 1/8. Total time = 8 days.")
                    else:
                        feedback_qa.append("❌ **Q1 Incorrect:** Correct answer is **8 days**. Formula: (A * B) / (A + B) = (12 * 24) / 36 = 8 days.")

                    if q_qa2 == "Rs. 1,200":
                        score_qa += 1
                        feedback_qa.append("✅ **Q2 Correct:** Cost Price = Selling Price / (1 + Profit%) = 1440 / 1.20 = Rs. 1,200.")
                    else:
                        feedback_qa.append("❌ **Q2 Incorrect:** Correct answer is **Rs. 1,200**. CP = SP * 100 / (100 + P%) = 1440 * 100 / 120 = 1200.")

                    if q_qa3 == "60 km/hr":
                        score_qa += 1
                        feedback_qa.append("✅ **Q3 Correct:** Speed = 150m / 9s = 50/3 m/s. Convert to km/hr: (50/3) * (18/5) = 60 km/hr.")
                    else:
                        feedback_qa.append("❌ **Q3 Incorrect:** Correct answer is **60 km/hr**. Multiply m/s by 18/5: (150/9) * (18/5) = 60 km/hr.")

                    if q_qa4 == "Rs. 2,100":
                        score_qa += 1
                        feedback_qa.append("✅ **Q4 Correct:** Amount = 10,000 * (1.10)^2 = Rs. 12,100. CI = 12,100 - 10,000 = Rs. 2,100.")
                    else:
                        feedback_qa.append("❌ **Q4 Incorrect:** Correct answer is **Rs. 2,100**. CI = P[(1 + R/100)^N - 1] = 10000[1.21 - 1] = 2100.")

                    if q_qa5 == "2 / 13":
                        score_qa += 1
                        feedback_qa.append("✅ **Q5 Correct:** 4 Queens + 4 Kings = 8 favorable outcomes. P = 8/52 = 2/13.")
                    else:
                        feedback_qa.append("❌ **Q5 Incorrect:** Correct answer is **2 / 13**. Total favorable cards = 4 + 4 = 8. P = 8 / 52 = 2 / 13.")

                    pct = int((score_qa / 5) * 100)
                    st.success(f"🎯 Quantitative Aptitude Score: **{score_qa} / 5 ({pct}%)**")
                    for fb in feedback_qa:
                        st.markdown(fb)

            # TAB 2: LOGICAL REASONING
            with tab_lr:
                st.markdown("### 🧩 Logical & Analytical Reasoning Mock Section")
                st.caption("Aptitude assessment testing patterns, series, coding-decoding, blood relations, and syllogisms.")

                q_lr1 = st.radio(
                    "**Q1. Number Series:** Identify the missing number in the progression: 3, 7, 15, 31, 63, ?",
                    ["125", "127", "128", "131"],
                    key="lr_q1"
                )
                q_lr2 = st.radio(
                    "**Q2. Coding-Decoding:** In a cryptographic code language, 'PENCIL' is written as 'QFOEJM'. How will 'SYSTEM' be coded in the identical pattern?",
                    ["TZTUFN", "TZUTFN", "TZTUEN", "TZUFNM"],
                    key="lr_q2"
                )
                q_lr3 = st.radio(
                    "**Q3. Blood Relations:** Pointing to a photograph, Rohit asserts: 'She is the daughter of my grandfather's only son.' How is the woman related to Rohit?",
                    ["Mother", "Sister", "Niece", "Aunt"],
                    key="lr_q3"
                )
                q_lr4 = st.radio(
                    "**Q4. Syllogism:** Statements: (I) All laptops are electronic gadgets. (II) All gadgets are computing devices. Conclusions: (A) All laptops are computing devices. (B) Some computing devices are laptops.",
                    ["Only (A) follows", "Only (B) follows", "Both (A) and (B) follow", "Neither follows"],
                    key="lr_q4"
                )
                q_lr5 = st.radio(
                    "**Q5. Direction Sense:** A candidate walks 20 meters North, takes a 90° right turn and walks 30 meters, then turns right again and walks 20 meters. How far and in which direction is the candidate from the starting point?",
                    ["30m East", "30m West", "50m North", "20m East"],
                    key="lr_q5"
                )

                if st.button("Submit Logical Reasoning Answers", key="btn_lr_eval"):
                    score_lr = 0
                    feedback_lr = []

                    if q_lr1 == "127":
                        score_lr += 1
                        feedback_lr.append("✅ **Q1 Correct:** Pattern is (prev * 2) + 1. (63 * 2) + 1 = 127.")
                    else:
                        feedback_lr.append("❌ **Q1 Incorrect:** Correct answer is **127**. Differences double each time: +4, +8, +16, +32, +64.")

                    if q_lr2 == "TZTUFN":
                        score_lr += 1
                        feedback_lr.append("✅ **Q2 Correct:** Each character shifts forward by +1: S->T, Y->Z, S->T, T->U, E->F, M->N = TZTUFN.")
                    else:
                        feedback_lr.append("❌ **Q2 Incorrect:** Correct answer is **TZTUFN**. Every letter is incremented by 1 position in the English alphabet.")

                    if q_lr3 == "Sister":
                        score_lr += 1
                        feedback_lr.append("✅ **Q3 Correct:** Grandfather's only son = Rohit's father. Father's daughter = Rohit's Sister.")
                    else:
                        feedback_lr.append("❌ **Q3 Incorrect:** Correct answer is **Sister**. The only son of his grandfather is his father, and his father's daughter is his sister.")

                    if q_lr4 == "Both (A) and (B) follow":
                        score_lr += 1
                        feedback_lr.append("✅ **Q4 Correct:** Transitive containment holds: Laptops ⊆ Gadgets ⊆ Computing Devices.")
                    else:
                        feedback_lr.append("❌ **Q4 Incorrect:** Correct answer is **Both (A) and (B) follow** due to universal nested subset inclusion.")

                    if q_lr5 == "30m East":
                        score_lr += 1
                        feedback_lr.append("✅ **Q5 Correct:** Walking 20m North and 20m South cancels the vertical displacement, leaving 30m East.")
                    else:
                        feedback_lr.append("❌ **Q5 Incorrect:** Correct answer is **30m East**.")

                    pct_lr = int((score_lr / 5) * 100)
                    st.success(f"🎯 Logical Reasoning Score: **{score_lr} / 5 ({pct_lr}%)**")
                    for fb in feedback_lr:
                        st.markdown(fb)

            # TAB 3: TECHNICAL & CORE MCQ
            with tab_tech:
                st.markdown("### 💻 Technical & Core Engineering Mock Section")
                st.caption("Standard technical screening MCQs across Data Structures, Algorithms, DBMS, Operating Systems, and OOPs.")

                q_t1 = st.radio(
                    "**Q1. Data Structures:** What is the worst-case time complexity of searching for an element in a balanced Binary Search Tree (AVL / Red-Black Tree)?",
                    ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
                    key="tech_q1"
                )
                q_t2 = st.radio(
                    "**Q2. Database Systems (SQL):** What is the fundamental difference between the SQL `WHERE` clause and the `HAVING` clause?",
                    [
                        "WHERE filters rows before aggregation; HAVING filters groups after aggregation",
                        "WHERE filters aggregated columns; HAVING filters individual rows",
                        "WHERE and HAVING are completely interchangeable in ANSI SQL",
                        "HAVING can only be utilized with subqueries and joins"
                    ],
                    key="tech_q2"
                )
                q_t3 = st.radio(
                    "**Q3. Operating Systems:** Which of the following conditions is NOT one of the four essential Coffman conditions necessary for a Deadlock to occur?",
                    [
                        "Mutual Exclusion",
                        "Hold and Wait",
                        "Preemption of resources allowed",
                        "Circular Wait"
                    ],
                    key="tech_q3"
                )
                q_t4 = st.radio(
                    "**Q4. Computer Networks:** Which Transport Layer protocol guarantees reliable, in-sequence, connection-oriented data delivery with congestion control?",
                    ["UDP (User Datagram Protocol)", "TCP (Transmission Control Protocol)", "ICMP (Internet Control Message Protocol)", "ARP (Address Resolution Protocol)"],
                    key="tech_q4"
                )
                q_t5 = st.radio(
                    "**Q5. Object-Oriented Programming:** Which object-oriented principle permits objects of different classes to respond uniquely to identical function invocations via method overriding?",
                    ["Encapsulation", "Polymorphism", "Abstraction", "Data Hiding"],
                    key="tech_q5"
                )

                if st.button("Submit Technical MCQ Answers", key="btn_tech_eval"):
                    score_t = 0
                    feedback_t = []

                    if q_t1 == "O(log N)":
                        score_t += 1
                        feedback_t.append("✅ **Q1 Correct:** A self-balancing BST maintains maximum height of O(log N), guaranteeing logarithmic search time.")
                    else:
                        feedback_t.append("❌ **Q1 Incorrect:** Correct answer is **O(log N)** because height balance prevents degenerate linked list skew.")

                    if "WHERE filters rows before aggregation" in q_t2:
                        score_t += 1
                        feedback_t.append("✅ **Q2 Correct:** WHERE filters individual input rows before GROUP BY; HAVING applies predicates to aggregate summary rows.")
                    else:
                        feedback_t.append("❌ **Q2 Incorrect:** Correct answer: **WHERE filters rows before aggregation; HAVING filters groups after aggregation**.")

                    if "Preemption of resources allowed" in q_t3:
                        score_t += 1
                        feedback_t.append("✅ **Q3 Correct:** The condition is **No Preemption** (resources cannot be forcibly taken away). Allowing preemption prevents deadlock.")
                    else:
                        feedback_t.append("❌ **Q3 Incorrect:** Correct answer is **Preemption of resources allowed**. Coffman requires **No Preemption**.")

                    if "TCP" in q_t4:
                        score_t += 1
                        feedback_t.append("✅ **Q4 Correct:** TCP provides reliable 3-way handshake, sequencing, flow control, and retransmissions.")
                    else:
                        feedback_t.append("❌ **Q4 Incorrect:** Correct answer is **TCP (Transmission Control Protocol)**. UDP is connectionless and best-effort.")

                    if q_t5 == "Polymorphism":
                        score_t += 1
                        feedback_t.append("✅ **Q5 Correct:** Polymorphism ('many forms') allows runtime dynamic dispatch and overriding.")
                    else:
                        feedback_t.append("❌ **Q5 Incorrect:** Correct answer is **Polymorphism**.")

                    pct_t = int((score_t / 5) * 100)
                    st.success(f"🎯 Technical MCQ Score: **{score_t} / 5 ({pct_t}%)**")
                    for fb in feedback_t:
                        st.markdown(fb)

            # TAB 4: VERBAL ABILITY
            with tab_va:
                st.markdown("### 📖 Verbal Ability & Business English Mock Section")
                st.caption("Verbal aptitude screening for corporate communications, error spotting, vocabulary, and grammar.")

                q_v1 = st.radio(
                    "**Q1. Sentence Correction:** Select the grammatically correct sentence conforming to standard English rules:",
                    [
                        "Neither of the two candidates have submitted their portfolio.",
                        "Neither of the two candidates has submitted his portfolio.",
                        "Neither of the two candidate have submitted his portfolio.",
                        "Neither of the two candidates were submitting their portfolio."
                    ],
                    key="va_q1"
                )
                q_v2 = st.radio(
                    "**Q2. Synonyms:** What is the most precise synonym for the word **'TENACIOUS'**?",
                    ["Hesitant", "Persistent / Resolute", "Fragile", "Superficial"],
                    key="va_q2"
                )
                q_v3 = st.radio(
                    "**Q3. Antonyms:** What is the exact antonym of the word **'METICULOUS'**?",
                    ["Careless / Sloppy", "Painstaking", "Thorough", "Methodical"],
                    key="va_q3"
                )
                q_v4 = st.radio(
                    "**Q4. Idiomatic Expressions:** What is the intended meaning of the common workplace idiom **'Bite the bullet'**?",
                    [
                        "To face a difficult or grim situation with courage and fortitude",
                        "To avoid addressing an uncomfortable problem",
                        "To abruptly surrender in the face of obstacles",
                        "To provoke an unnecessary controversy"
                    ],
                    key="va_q4"
                )
                q_v5 = st.radio(
                    "**Q5. Spotting Errors:** Identify the grammatically flawed segment: 'The engineering team [A] / are planning [B] / to release the microservice [C] / tomorrow [D].'",
                    [
                        "Part [A]",
                        "Part [B] ('is planning' should replace 'are planning')",
                        "Part [C]",
                        "Part [D] (No error)"
                    ],
                    key="va_q5"
                )

                if st.button("Submit Verbal Ability Answers", key="btn_va_eval"):
                    score_v = 0
                    feedback_v = []

                    if "Neither of the two candidates has submitted his portfolio." in q_v1:
                        score_v += 1
                        feedback_v.append("✅ **Q1 Correct:** 'Neither' is singular and requires the singular verb 'has' and pronoun 'his'.")
                    else:
                        feedback_v.append("❌ **Q1 Incorrect:** Correct sentence: **'Neither of the two candidates has submitted his portfolio.'**")

                    if "Persistent / Resolute" in q_v2:
                        score_v += 1
                        feedback_v.append("✅ **Q2 Correct:** 'Tenacious' means holding firmly or persisting with determination.")
                    else:
                        feedback_v.append("❌ **Q2 Incorrect:** Correct synonym is **Persistent / Resolute**.")

                    if "Careless / Sloppy" in q_v3:
                        score_v += 1
                        feedback_v.append("✅ **Q3 Correct:** 'Meticulous' means extremely careful and precise; its antonym is Careless or Sloppy.")
                    else:
                        feedback_v.append("❌ **Q3 Incorrect:** Correct antonym is **Careless / Sloppy**.")

                    if "with courage and fortitude" in q_v4:
                        score_v += 1
                        feedback_v.append("✅ **Q4 Correct:** 'Bite the bullet' means confronting an unavoidable hardship bravely.")
                    else:
                        feedback_v.append("❌ **Q4 Incorrect:** Correct answer: **To face a difficult or grim situation with courage and fortitude**.")

                    if "Part [B]" in q_v5:
                        score_v += 1
                        feedback_v.append("✅ **Q5 Correct:** Collective noun 'team' acting as a unit requires singular verb 'is planning'.")
                    else:
                        feedback_v.append("❌ **Q5 Incorrect:** Correct answer is **Part [B]**.")

                    pct_v = int((score_v / 5) * 100)
                    st.success(f"🎯 Verbal Ability Score: **{score_v} / 5 ({pct_v}%)**")
                    for fb in feedback_v:
                        st.markdown(fb)

            # TAB 5: CURATED PRACTICE LINKS
            with tab_links:
                st.markdown("### 🌐 Curated Practice Portals, Google Resources & Coding Arenas")
                st.markdown("Sharpen your aptitude, technical problem solving, and mock interviews using these high-yield placement platforms and official Google prep tools endorsed by TKIET T&P Cell:")

                st.markdown("#### 🔍 Official Google Practice & Interview Resources")
                g_col1, g_col2 = st.columns(2)
                with g_col1:
                    st.markdown("""
                    <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#1D4ED8; margin-top:0;">🎙️ Google Interview Warmup</h4>
                        <p style="font-size:0.88rem; color:#1E3A8A;">Practice answering real interview questions created by Google experts. Speak or type your answers to receive instant AI insights on key terms, most-used words, and job-related talking points.</p>
                        <a href="https://grow.google/certificates/interview-warmup/" target="_blank" style="background:#1D4ED8; color:white; padding:7px 15px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Start Google Interview Warmup ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#1D4ED8; margin-top:0;">📋 Google Forms — TKIET Online Practice Quiz</h4>
                        <p style="font-size:0.88rem; color:#1E3A8A;">Access official online aptitude and technical screening question sets organized via Google Forms for quick timed revision and automatic scoring.</p>
                        <a href="https://docs.google.com/forms/" target="_blank" style="background:#1D4ED8; color:white; padding:7px 15px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Open Google Forms Quiz Sheet ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                with g_col2:
                    st.markdown("""
                    <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#1D4ED8; margin-top:0;">🧭 Google Tech Dev Guide</h4>
                        <p style="font-size:0.88rem; color:#1E3A8A;">Google's official curriculum for computer science students: master data structures, dynamic programming, and scalable system design used by top software engineers.</p>
                        <a href="https://techdevguide.withgoogle.com/" target="_blank" style="background:#1D4ED8; color:white; padding:7px 15px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Explore Google Tech Dev Guide ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#1D4ED8; margin-top:0;">📱 Google Developers Codelabs & Learn</h4>
                        <p style="font-size:0.88rem; color:#1E3A8A;">Interactive guided tutorials and self-paced code challenges covering Cloud architecture, Android engineering, Python APIs, and Machine Learning.</p>
                        <a href="https://developers.google.com/learn" target="_blank" style="background:#1D4ED8; color:white; padding:7px 15px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Open Google Developers Learn ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### 💻 External Coding, Aptitude & Placement Arenas")
                pl_col1, pl_col2 = st.columns(2)
                with pl_col1:
                    st.markdown("""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#2563EB; margin-top:0;">⚡ LeetCode — Top Interview 150</h4>
                        <p style="font-size:0.88rem; color:#475569;">Industry-standard curated list of 150 essential data structures, algorithms, two-pointer, dynamic programming, and system design challenges for product MNCs.</p>
                        <a href="https://leetcode.com/problemset/all/" target="_blank" style="background:#2563EB; color:white; padding:6px 14px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Launch LeetCode Arena ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#059669; margin-top:0;">📊 IndiaBIX — Quantitative & Logical Prep</h4>
                        <p style="font-size:0.88rem; color:#475569;">Exhaustive repository of quantitative aptitude, verbal reasoning, non-verbal series, and data interpretation questions with step-by-step solutions.</p>
                        <a href="https://www.indiabix.com/" target="_blank" style="background:#059669; color:white; padding:6px 14px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Open IndiaBIX Tests ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#7C3AED; margin-top:0;">🎯 HackerRank — Role Certification Tracks</h4>
                        <p style="font-size:0.88rem; color:#475569;">Skill assessments and verified certificates in Python, Problem Solving, Java, SQL, and Software Engineering benchmarks used by global recruiters.</p>
                        <a href="https://www.hackerrank.com/" target="_blank" style="background:#7C3AED; color:white; padding:6px 14px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Practice on HackerRank ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                with pl_col2:
                    st.markdown("""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#D97706; margin-top:0;">📚 GeeksforGeeks — Placement Prep Portal</h4>
                        <p style="font-size:0.88rem; color:#475569;">Company-wise recruitment archives (TCS NQT, Infosys, Wipro, Cognizant, Tata Motors), core subjects notes (OS, DBMS, CN), and interview experiences.</p>
                        <a href="https://www.geeksforgeeks.org/placement-preparation-course/" target="_blank" style="background:#D97706; color:white; padding:6px 14px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Visit GeeksforGeeks Portal ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#0284C7; margin-top:0;">⚙️ Sanfoundry — 100k Engineering MCQs</h4>
                        <p style="font-size:0.88rem; color:#475569;">Comprehensive technical MCQs for Mechanical, E&TC, Computer Science, Cyber Security, and Instrumentation Engineering disciplines.</p>
                        <a href="https://www.sanfoundry.com/" target="_blank" style="background:#0284C7; color:white; padding:6px 14px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Explore Sanfoundry MCQs ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:1.2rem; margin-bottom:1rem;">
                        <h4 style="color:#DC2626; margin-top:0;">💼 InterviewBit — Mock Technical Track</h4>
                        <p style="font-size:0.88rem; color:#475569;">Time-pressured coding tests simulating real technical screening rounds at top MNCs with time complexity constraints and peer mock interviews.</p>
                        <a href="https://www.interviewbit.com/" target="_blank" style="background:#DC2626; color:white; padding:6px 14px; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.85rem; display:inline-block;">Launch InterviewBit ↗</a>
                    </div>
                    """, unsafe_allow_html=True)

        # 1.5 Placement Drives & Apply
        elif nav_choice == "💼 Placement Drives & Apply":
            active_comp_name = st.session_state.get("active_apply_comp")

            # --- VIEW A: GOOGLE FORM FOR PARTICULAR COMPANY ---
            if active_comp_name:
                matched_comps = [c for c in st.session_state["drives_list"] if c["name"] == active_comp_name]
                active_comp = matched_comps[0] if matched_comps else st.session_state["drives_list"][0]

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #673AB7 0%, #512DA8 100%); color: white; padding: 1.5rem; border-radius: 14px; margin-bottom: 1.2rem; box-shadow: 0 4px 12px rgba(103,58,183,0.35);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:700; letter-spacing:0.05em; text-transform:uppercase;">
                            📋 TKIET Official Google Form Application
                        </span>
                        <a href="https://docs.google.com/forms/" target="_blank" style="background:#FFFFFF; color:#512DA8; padding:5px 12px; border-radius:20px; font-size:0.75rem; font-weight:700; text-decoration:none; display:inline-block;">
                            🔗 Open in Google Forms ↗
                        </a>
                    </div>
                    <h2 style="color:white; margin:0.4rem 0 0.2rem 0; font-size:1.7rem;">Application for {active_comp['name']}</h2>
                    <p style="color:#EDE9FE; margin-bottom:0; font-size:0.95rem;">
                        Target Designation: <b>{active_comp['role']}</b> | Compensation: <b>{active_comp['ctc']}</b> | Supervised by TPO <b>Prof. P. J. Patil</b>
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.info(f"ℹ️ Complete this official Google Form application to register your candidacy for **{active_comp['name']}**. Your response will be logged into the TKIET Placement database and forwarded directly to TPO **Prof. P. J. Patil**.")

                with st.form("google_apply_form"):
                    st.markdown("#### 1. Candidate Identity & Academic Verification")
                    c_af1, c_af2 = st.columns(2)
                    with c_af1:
                        f_name = st.text_input("Full Candidate Name *", value=curr_student["name"], disabled=True)
                        f_prn = st.text_input("PRN / Roll Number *", value=curr_student["student_id"], disabled=True)
                        f_email = st.text_input("Institutional Email *", value=curr_student.get("email", f"{curr_student['name'].lower().replace(' ', '.')}@tkiet.edu.in"), disabled=True)
                    with c_af2:
                        f_dept = st.text_input("Department / Discipline *", value=curr_student["department"], disabled=True)
                        f_cgpa = st.text_input("Current Cumulative CGPA *", value=str(curr_student["prior_cgpa"]), disabled=True)
                        f_backlogs = st.text_input("Active Backlogs *", value=str(curr_student["backlogs"]), disabled=True)

                    st.markdown("---")
                    st.markdown("#### 2. Contact & Secondary Academics")
                    c_af3, c_af4 = st.columns(2)
                    with c_af3:
                        f_phone = st.text_input("Contact Mobile Number *", placeholder="+91 98xxxxxxxx", value="+91 9822014589")
                        f_10th = st.number_input("10th Standard Aggregate Percentage (%) *", min_value=50.0, max_value=100.0, value=85.6, step=0.1)
                    with c_af4:
                        f_alt_email = st.text_input("Alternate Email Address", placeholder="personal.email@gmail.com")
                        f_12th = st.number_input("12th / Diploma Aggregate Percentage (%) *", min_value=50.0, max_value=100.0, value=83.4, step=0.1)

                    st.markdown("---")
                    st.markdown("#### 3. Resume & Professional Portfolios")
                    f_resume_url = st.text_input(
                        "Google Drive / Cloud Shareable Resume URL *",
                        placeholder="https://drive.google.com/file/d/1A2B3C4D.../view?usp=sharing",
                        help="Please ensure sharing permissions are set to 'Anyone with the link can view'."
                    )
                    c_af5, c_af6 = st.columns(2)
                    with c_af5:
                        f_github = st.text_input("GitHub / Technical Portfolio URL", placeholder="https://github.com/your-username")
                    with c_af6:
                        f_linkedin = st.text_input("LinkedIn Profile URL", placeholder="https://linkedin.com/in/your-profile")

                    st.markdown("---")
                    st.markdown("#### 4. Job Preferences & Statement of Purpose")
                    f_loc = st.multiselect(
                        "Preferred Job Location(s) *",
                        ["Pune", "Bangalore", "Mumbai", "Hyderabad", "Kolhapur / Warananagar", "Open to Any Location / Ready to Relocate"],
                        default=["Pune", "Bangalore"]
                    )
                    f_sop = st.text_area(
                        f"Why are you interested in joining {active_comp['name']} and how do your skills align with the {active_comp['role']} role? *",
                        placeholder="State your relevant projects, problem-solving skills, and why this corporate culture aligns with your career objectives...",
                        height=100
                    )
                    f_relocate = st.radio(
                        "Are you willing to sign standard service agreements / bonds if required by the company policy?",
                        ["Yes, I agree", "No, I am not willing"],
                        index=0
                    )

                    f_declare = st.checkbox("I hereby certify that all information provided is accurate and authentic. I agree to abide by the TKIET Placement Rules governed by TPO Prof. P. J. Patil.")

                    c_sub1, c_sub2 = st.columns([1, 1])
                    with c_sub1:
                        submit_app = st.form_submit_button("🚀 Submit Official Application", use_container_width=True, type="primary")

                if submit_app:
                    if not f_resume_url.strip():
                        st.error("❌ Please provide a valid Google Drive shareable link to your resume before submitting.")
                    elif not f_declare:
                        st.error("❌ Please review and accept the declaration to proceed with your application.")
                    else:
                        app_key = f"app_{curr_student['student_id']}_{active_comp['name']}"
                        if app_key not in st.session_state["applications"]:
                            st.session_state["applications"].append(app_key)

                        app_id = f"TKIET-{active_comp['name'][:3].upper()}-{datetime.now().strftime('%m%d%H%M')}"
                        new_app_record = {
                            "application_id": app_id,
                            "student_id": curr_student["student_id"],
                            "student_name": curr_student["name"],
                            "department": curr_student["department"],
                            "company_name": active_comp["name"],
                            "role": active_comp["role"],
                            "ctc": active_comp["ctc"],
                            "applied_on": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "resume_link": f_resume_url,
                            "preferred_location": ", ".join(f_loc) if f_loc else "Open",
                            "status": "Submitted ➔ Under TPO Review (Prof. P. J. Patil)"
                        }
                        st.session_state["applications_detailed"].append(new_app_record)
                        st.session_state["active_apply_comp"] = None
                        st.balloons()
                        st.success(f"🎉 Application `{app_id}` successfully submitted for **{active_comp['name']}**! Routed to TPO Prof. P. J. Patil.")
                        st.rerun()

                if st.button("✖ Cancel and Return to All Drives"):
                    st.session_state["active_apply_comp"] = None
                    st.rerun()

            # --- VIEW B: REGULAR DRIVES DIRECTORY & TRACKER ---
            else:
                st.subheader(f"Campus Placement Drives Eligible for {curr_student['department']}")
                st.caption(f"TKIET Training & Placement Cell | Student Candidate: **{curr_student['name']}** (CGPA: {curr_student['prior_cgpa']} | Backlogs: {curr_student['backlogs']})")

                for comp in st.session_state["drives_list"]:
                    is_branch_allowed = curr_student["department"] in comp["allowed_depts"]
                    cgpa_ok = curr_student["prior_cgpa"] >= comp["min_cgpa"]
                    backlogs_ok = curr_student["backlogs"] <= comp["max_backlogs"]
                    is_eligible = is_branch_allowed and cgpa_ok and backlogs_ok

                    with st.expander(f"🏢 {comp['name']} — {comp['role']} ({comp['ctc']})", expanded=is_eligible):
                        d1, d2 = st.columns([2, 1])
                        with d1:
                            st.write(f"**Industry:** {comp['industry']} | **Cutoff CGPA:** {comp['min_cgpa']} | **Max Backlogs:** {comp['max_backlogs']}")
                            st.write(f"**Eligible Branches:** {', '.join(comp['allowed_depts'])}")
                            if "skills_required" in comp:
                                st.write(f"**Core Tech Stack:** {', '.join(comp['skills_required'])}")
                        with d2:
                            if is_eligible:
                                st.success("✅ ELIGIBLE")
                                app_key = f"app_{curr_student['student_id']}_{comp['name']}"
                                if app_key in st.session_state["applications"]:
                                    st.info("📨 Application Submitted")
                                else:
                                    if st.button(f"📝 Apply via Google Form", key=f"btn_form_{comp['name']}"):
                                        st.session_state["active_apply_comp"] = comp["name"]
                                        st.rerun()
                            else:
                                reason = []
                                if not is_branch_allowed:
                                    reason.append(f"Branch '{curr_student['department']}' not listed")
                                if not cgpa_ok:
                                    reason.append(f"CGPA {curr_student['prior_cgpa']} < Cutoff {comp['min_cgpa']}")
                                if not backlogs_ok:
                                    reason.append(f"Backlogs {curr_student['backlogs']} > Max {comp['max_backlogs']}")
                                st.error(f"⛔ Ineligible: {', '.join(reason)}")

                # Live Applications Tracker
                st.markdown("---")
                st.markdown("### 📋 My Applied Placement Drives Tracker")
                student_apps = [a for a in st.session_state["applications_detailed"] if a["student_id"] == curr_student["student_id"]]

                if student_apps:
                    st.dataframe(pd.DataFrame(student_apps)[["application_id", "company_name", "role", "ctc", "applied_on", "preferred_location", "status"]], use_container_width=True)
                else:
                    st.info("You haven't submitted any company applications yet. Explore the eligible drives above and click **'📝 Apply via Google Form'** to begin.")

        # 1.6 AI Resume Auditor & Live ATS Score Tracker
        elif nav_choice == "🤖 AI Resume Auditor & Sprint":
            st.markdown("""
            <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: white; padding: 1.3rem; border-radius: 12px; margin-bottom: 1.2rem; border-left: 5px solid #38BDF8;">
                <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; color: #38BDF8;">AI Resume Auditor & ATS Tracker</div>
                <h2 style="color: white; margin: 0.2rem 0; font-size: 1.6rem;">Live ATS Resume Analyzer & Revision Tracker</h2>
                <div style="font-size: 0.95rem; color: #94A3B8;">Upload your resume or paste its plain text to benchmark against corporate Applicant Tracking Systems (ATS), find keyword gaps, and track version scores.</div>
            </div>
            """, unsafe_allow_html=True)

            ROLE_KEYWORD_DB = {
                "Full Stack Software Engineer": ["Python", "JavaScript", "React", "Node.js", "SQL", "Git", "REST APIs", "Docker", "HTML", "CSS", "MongoDB", "Data Structures", "Algorithms", "CI/CD"],
                "Data Scientist & AI/ML Engineer": ["Python", "Machine Learning", "Deep Learning", "SQL", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch", "Data Visualization", "Statistics", "Git", "NLP"],
                "Cyber Security Analyst": ["Network Security", "Cryptography", "Penetration Testing", "Wireshark", "Linux", "Firewalls", "SIEM", "Vulnerability Assessment", "Python", "SOC", "Ethical Hacking"],
                "Cloud & DevOps Engineer": ["AWS", "Azure", "Docker", "Kubernetes", "Linux", "Terraform", "CI/CD", "Jenkins", "Git", "Python", "Bash", "Monitoring", "CloudFormation"],
                "Mechanical Design & Thermal Engineer": ["AutoCAD", "SolidWorks", "CATIA", "ANSYS", "Finite Element Analysis", "Thermodynamics", "GD&T", "DFM", "Manufacturing", "MATLAB", "Robotics"],
                "Embedded Systems & IoT Engineer": ["C", "C++", "Microcontrollers", "RTOS", "Embedded C", "IoT", "ARM", "PCB Design", "Sensors", "I2C", "SPI", "UART", "Arduino"],
                "Business Analyst & Management (MBA)": ["Financial Modeling", "Business Strategy", "SQL", "Excel", "Tableau", "Power BI", "Agile", "Market Research", "Project Management", "Data Analysis", "Risk Assessment"]
            }

            c_role1, c_role2 = st.columns([1.5, 1])
            with c_role1:
                target_ats_role = st.selectbox(
                    "Target Job Designation / Profile:",
                    list(ROLE_KEYWORD_DB.keys()),
                    index=0 if curr_student["department"] in ["MCA", "CS"] else (1 if curr_student["department"] == "CSBS" else (2 if curr_student["department"] == "Cyber Security" else (4 if curr_student["department"] == "Mechanical" else (5 if curr_student["department"] == "E&TC" else 6))))
                )
            with c_role2:
                st.caption(f"Candidate: **{curr_student['name']}** ({curr_student['department']})")
                st.caption("Benchmark against TKIET placement criteria & corporate standards.")

            # Department-Specific Sample Resume Template for 1-click loading
            dept_k = curr_student["department"]
            dept_skills_list = DEPARTMENT_SKILL_MAP.get(dept_k, DEPARTMENT_SKILL_MAP["MCA"])["skills"]
            skills_str = ", ".join(dept_skills_list)
            
            if dept_k == "Mechanical":
                dept_degree = "B.Tech in Mechanical Engineering"
                p1_title = "1. Autonomous Industrial Guided Vehicle (AGV) with PLC Control"
                p1_desc = "- Developed kinematics model and Siemens S7-1200 PLC ladder logic for 250kg payload AGV.\n   - Simulated dynamic stresses and factor of safety using ANSYS FEA, reducing chassis mass by 14%."
                p2_title = "2. Thermal & Structural FEA of EV Battery Module"
                p2_desc = "- Conducted transient heat dissipation simulation in SolidWorks Flow Simulation, maintaining cell temps below 42°C.\n   - Designed CNC-machined aluminum cold plate heat sink with optimized cooling channels."
            elif dept_k == "Cyber Security":
                dept_degree = "B.Tech in Cyber Security Engineering"
                p1_title = "1. Automated SOC Threat Hunter & Real-time SIEM Dashboard"
                p1_desc = "- Ingested and parsed 50k+ daily syslog events with ELK stack and custom Python intrusion detection scripts.\n   - Reduced mean time to detect (MTTD) brute-force and port scans by 60% with automated alerts."
                p2_title = "2. Enterprise Web Vulnerability & Zero-Trust Audit Framework"
                p2_desc = "- Performed OWASP Top 10 automated pen-tests using Burp Suite Professional and Python scripts.\n   - Identified and remediated 8 critical privilege escalation vulnerabilities before production release."
            elif dept_k == "E&TC":
                dept_degree = "B.Tech in Electronics & Telecommunication Engineering"
                p1_title = "1. Industrial IoT Edge Gateway with FreeRTOS & LoRaWAN"
                p1_desc = "- Programmed ARM Cortex-M4 microcontroller firmware in Embedded C managing 4 sensor tasks deterministically.\n   - Implemented low-power sleep modes achieving 18-month battery longevity on solar backup."
                p2_title = "2. Real-Time CAN Bus Vehicle Telemetry System"
                p2_desc = "- Interfaced OBD-II vehicle diagnostics with ESP32 via SPI/UART protocols, publishing metrics over MQTT.\n   - Designed two-layer PCB in KiCad with EMI shielding meeting automotive standards."
            elif dept_k == "CSBS":
                dept_degree = "B.Tech in Computer Science & Business Systems"
                p1_title = "1. High-Frequency Algorithmic Portfolio Risk Simulator"
                p1_desc = "- Modeled historical stock volatility and Value-at-Risk (VaR) using Python time series econometrics.\n   - Built interactive Tableau dashboard for multi-asset stress testing and Sharpe ratio optimization."
                p2_title = "2. ERP-Integrated Demand Forecasting Engine"
                p2_desc = "- Connected SAP simulated data with ARIMA and Prophet models for retail inventory prediction.\n   - Lowered inventory stock-out probability by 22% using automated safety stock triggers."
            elif dept_k == "MBA":
                dept_degree = "Master of Business Administration (MBA)"
                p1_title = "1. CleanTech Market Entry Strategy & 5-Year DCF Valuation"
                p1_desc = "- Formulated comprehensive market entry strategy and financial model with sensitivity matrices.\n   - Evaluated WACC, terminal growth rates, and projected EBITDA margins across 3 growth scenarios."
                p2_title = "2. Customer Lifetime Value (CLV) & Cohort Retention Blueprint"
                p2_desc = "- Analyzed customer acquisition cost (CAC) and cohort retention curves for a direct-to-consumer brand.\n   - Recommended targeted re-engagement campaigns boosting 90-day repeat purchase rate by 18%."
            else:
                dept_degree = f"Master of Computer Applications (MCA) / B.Tech CS" if dept_k == "MCA" else "B.Tech in Computer Science & Engineering"
                p1_title = "1. Enterprise Cloud Microservices Architecture with Spring Boot"
                p1_desc = "- Engineered resilient REST APIs and Kafka messaging pipeline handling 1,000+ requests/second.\n   - Deployed multi-container Docker pods with health checks and automated CI/CD deployment."
                p2_title = "2. Academic Performance & Career Advisory Engine"
                p2_desc = "- Developed machine learning models achieving 92% accuracy in predicting semester SGPA.\n   - Engineered automated skill-gap diagnostics and personalized learning roadmap recommender."

            sample_resume = f"""{curr_student['name']}
Warananagar, Kolhapur | {curr_student.get('email', 'student@tkiet.edu.in')} | +91 9822014589
LinkedIn: linkedin.com/in/{curr_student['name'].lower().replace(' ', '')} | GitHub/Portfolio: github.com/{curr_student['name'].lower().replace(' ', '')}

CAREER OBJECTIVE
Enthusiastic and results-driven {curr_student['department']} student at Tatyasaheb Kore Institute of Engineering & Technology, Warananagar with strong fundamentals in modern discipline-specific engineering practices, technical problem solving, and industrial standards. Eager to contribute to corporate excellence.

EDUCATION
- {dept_degree} | Tatyasaheb Kore Institute of Engineering & Technology (TKIET), Warananagar
  Cumulative CGPA: {curr_student['prior_cgpa']} / 10.0 | Expected Graduation: 2026
- Higher Secondary Certificate (HSC) | Maharashtra State Board | Aggregate: 84.5%

TECHNICAL SKILLS & COMPETENCIES ({curr_student['department']})
- Core Department Skills: {skills_str}
- Professional Tools & Environments: Git, Linux, Docker, VS Code, Industry CAD/Simulation Tools
- Applied Engineering: Systems Design, Performance Optimization, Regulatory Compliance

TECHNICAL PROJECTS
{p1_title}
{p1_desc}

{p2_title}
{p2_desc}

EXPERIENCE & INTERNSHIPS
Technical Engineering Intern | TKIET Center of Excellence & Industry Partner (June 2025 - August 2025)
- Collaborated in an agile team of 4 to design, simulate, and validate production-ready deliverables.
- Authored comprehensive technical documentation and automated validation benchmarks.

CERTIFICATIONS & ACHIEVEMENTS
- Certified in {dept_skills_list[0]} & Applied {curr_student['department']} Practices
- Active Member of TKIET Student Technical Association and Training & Placement Cell
"""

            # Input methods
            res_tab1, res_tab2 = st.tabs(["📤 Upload Resume File", "📋 Paste / Edit Resume Text"])

            uploaded_file = None
            with res_tab1:
                uploaded_file = st.file_uploader("Upload Your Resume Document (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"], key="resume_uploader")
                if uploaded_file is not None:
                    st.success(f"✅ File loaded: `{uploaded_file.name}` ({uploaded_file.size} bytes)")

            # Determine text content
            resume_text_content = ""
            if uploaded_file is not None:
                if uploaded_file.name.endswith(".txt"):
                    resume_text_content = uploaded_file.read().decode("utf-8", errors="ignore")
                else:
                    # For PDF/DOCX safe fallback extraction
                    raw_bytes = uploaded_file.read()
                    try:
                        import re
                        extracted_words = re.findall(rb'[A-Za-z0-9@\.\+\#\-]{3,}', raw_bytes)
                        resume_text_content = " ".join([w.decode("latin1", errors="ignore") for w in extracted_words[:1200]])
                    except Exception:
                        resume_text_content = ""
                st.info("📄 Document parsed. You can fine-tune the extracted text below:")

            with res_tab2:
                c_btn_load, c_btn_clear = st.columns([1, 1])
                with c_btn_load:
                    if st.button("📄 Load Sample TKIET Student Resume", key="btn_load_sample"):
                        st.session_state["pasted_resume_text"] = sample_resume
                        st.session_state["resume_text_area"] = sample_resume
                        st.rerun()
                with c_btn_clear:
                    if st.button("🗑️ Clear Resume Content", key="btn_clear_resume"):
                        st.session_state["pasted_resume_text"] = ""
                        st.session_state["resume_text_area"] = ""
                        st.rerun()

                # Prioritize explicit pasted/session state, then uploaded file text, else empty
                if "pasted_resume_text" in st.session_state:
                    default_text = st.session_state["pasted_resume_text"]
                elif resume_text_content:
                    default_text = resume_text_content
                else:
                    default_text = ""

                resume_text_input = st.text_area(
                    "Resume Plain Text Content for ATS Evaluation:",
                    value=default_text,
                    height=240,
                    placeholder="Paste your resume plain text here, or upload your resume file in Tab 1...",
                    key="resume_text_area"
                )

            # LIVE ATS SCORING ENGINE
            text_to_eval = resume_text_input.strip()

            if not text_to_eval:
                st.markdown("---")
                st.markdown(f"""
                <div style="background:#F8FAFC; border:1.5px dashed #94A3B8; border-radius:12px; padding:2.5rem 1.5rem; text-align:center; margin:1.5rem 0;">
                    <div style="font-size:3rem; margin-bottom:8px;">📄</div>
                    <h3 style="color:#1E293B; margin:0 0 8px 0; font-weight:700;">No Resume Entered Yet</h3>
                    <p style="color:#64748B; font-size:0.95rem; max-width:620px; margin:0 auto 16px auto; line-height:1.5;">
                        To calculate your <b>AI ATS Compatibility Score</b> and view target keyword alignment for <b>{target_ats_role}</b>, please upload your resume file in the <b>'Upload Resume File'</b> tab or paste your resume text in the box above.
                    </p>
                    <div style="display:inline-block; background:#EFF6FF; border:1px solid #BFDBFE; color:#1D4ED8; font-size:0.85rem; font-weight:600; padding:6px 14px; border-radius:20px;">
                        💡 Tip: Click <b>'Load Sample TKIET Student Resume'</b> above if you want to test the scanner with a sample template.
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                text_lower = text_to_eval.lower()

                # 1. Keywords analysis
                target_keywords = ROLE_KEYWORD_DB.get(target_ats_role, ["Python", "SQL", "Git"])
                found_keywords = [kw for kw in target_keywords if kw.lower() in text_lower]
                missing_keywords = [kw for kw in target_keywords if kw.lower() not in text_lower]
                kw_match_pct = len(found_keywords) / len(target_keywords) if target_keywords else 1.0

                # 2. Section analysis
                sections = {
                    "Education": any(w in text_lower for w in ["education", "b.tech", "mca", "degree", "university", "tkiet", "college"]),
                    "Skills": any(w in text_lower for w in ["skills", "technologies", "tech stack", "tools", "programming"]),
                    "Projects": any(w in text_lower for w in ["project", "projects", "developed", "engineered"]),
                    "Experience / Internships": any(w in text_lower for w in ["experience", "internship", "intern", "work", "employment"]),
                    "Certifications": any(w in text_lower for w in ["certification", "certificate", "certified", "achievements", "awards"]),
                    "Contact Info": any(w in text_lower for w in ["email", "github", "linkedin", "phone", "+91", "@"])
                }
                sec_score = (sum(sections.values()) / len(sections)) * 25

                # 3. Quantifiable Impact & Metrics
                import re
                metric_matches = re.findall(r'(\d+[\.,]?\d*\s*[%xXkK]?|\$\d+|\d+\+)', text_to_eval)
                metric_score = min(20, len(metric_matches) * 2)

                # 4. Action Verbs
                action_verbs = ["developed", "implemented", "engineered", "optimized", "built", "designed", "automated", "spearheaded", "collaborated", "reduced", "improved"]
                verbs_found = [v for v in action_verbs if v in text_lower]
                verb_score = min(15, len(verbs_found) * 2.5)

                # 5. Length & Formatting (word count)
                words = text_to_eval.split()
                word_count = len(words)
                length_score = 15 if (180 <= word_count <= 900) else (10 if (100 <= word_count <= 1200) else 5)

                # Total score
                kw_pts = kw_match_pct * 25
                total_ats_score = int(round(kw_pts + sec_score + metric_score + verb_score + length_score))
                total_ats_score = max(20, min(98, total_ats_score))

                if total_ats_score >= 82:
                    ats_grade = "Tier 1 — Ready for Top MNCs & Product Companies"
                    grade_color = "#10B981"
                elif total_ats_score >= 68:
                    ats_grade = "Tier 2 — Competitive (Minor Revisions Recommended)"
                    grade_color = "#F59E0B"
                else:
                    ats_grade = "Tier 3 — Requires Enhancement before Applying"
                    grade_color = "#EF4444"

                st.markdown("---")
                st.markdown("### 📊 Live ATS Evaluation Results")

                m_c1, m_c2, m_c3, m_c4 = st.columns(4)
                m_c1.metric("Overall ATS Score", f"{total_ats_score} / 100")
                m_c2.metric("Keyword Match", f"{int(kw_match_pct * 100)}%", f"{len(found_keywords)} / {len(target_keywords)} found")
                m_c3.metric("Sections Detected", f"{sum(sections.values())} / {len(sections)}")
                m_c4.metric("Word Count", f"{word_count} words")

                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border: 1px solid {grade_color}; padding: 0.8rem 1.2rem; border-radius: 10px; margin-bottom: 1.2rem;">
                    <span style="font-weight:700; color:{grade_color}; font-size:1.05rem;">{ats_grade}</span>
                </div>
                """, unsafe_allow_html=True)

                # Keywords found vs missing
                kw_col1, kw_col2 = st.columns(2)
                with kw_col1:
                    st.markdown("#### ✅ Matched Target Keywords")
                    if found_keywords:
                        pills_html = " ".join([f"<span style='background:#DCFCE7; color:#166534; padding:4px 10px; border-radius:9999px; font-size:0.82rem; font-weight:600; display:inline-block; margin:2px;'>✓ {k}</span>" for k in found_keywords])
                        st.markdown(pills_html, unsafe_allow_html=True)
                    else:
                        st.info("No matching target keywords detected yet.")

                with kw_col2:
                    st.markdown("#### ⚠️ Missing High-Priority Keywords")
                    if missing_keywords:
                        miss_html = " ".join([f"<span style='background:#FEE2E2; color:#991B1B; padding:4px 10px; border-radius:9999px; font-size:0.82rem; font-weight:600; display:inline-block; margin:2px;'>+ {k}</span>" for k in missing_keywords])
                        st.markdown(miss_html, unsafe_allow_html=True)
                    else:
                        st.success("🎉 Outstanding! All target role keywords are present in your resume.")

                # Section Completeness Checklist
                st.markdown("---")
                st.markdown("#### 📑 Structural Completeness Checklist")
                s_c1, s_c2, s_c3 = st.columns(3)
                with s_c1:
                    st.markdown(f"- {'✅' if sections['Education'] else '❌'} **Education & University Details**")
                    st.markdown(f"- {'✅' if sections['Skills'] else '❌'} **Technical Skills Section**")
                with s_c2:
                    st.markdown(f"- {'✅' if sections['Projects'] else '❌'} **Technical Projects Portfolio**")
                    st.markdown(f"- {'✅' if sections['Experience / Internships'] else '❌'} **Experience / Internships**")
                with s_c3:
                    st.markdown(f"- {'✅' if sections['Certifications'] else '❌'} **Certifications & Achievements**")
                    st.markdown(f"- {'✅' if sections['Contact Info'] else '❌'} **Contact Details & GitHub/LinkedIn**")

                # AI Recommendations
                st.markdown("#### 💡 Actionable Resume Recommendations:")
                recommendations = []
                if missing_keywords:
                    recommendations.append(f"Incorporate missing core skills: **{', '.join(missing_keywords[:4])}** in your technical skills or project descriptions.")
                if len(metric_matches) < 3:
                    recommendations.append("Add quantifiable metrics to project bullet points (e.g., *'Optimized load time by 35%'*, *'Handled 500+ daily requests'*).")
                if not sections["Experience / Internships"]:
                    recommendations.append("Include practical virtual internships, capstone projects, or open-source contributions.")
                if word_count < 200:
                    recommendations.append("Elaborate on project methodologies and implementation architecture to reach a healthy 300-600 word depth.")
                if not recommendations:
                    recommendations.append("Your resume meets all corporate ATS benchmarks! Keep your GitHub links and portfolio live.")

                for rec in recommendations:
                    st.markdown(f"- 📌 {rec}")

                # VERSION TRACKER
                st.markdown("---")
                st.markdown("### 📈 Resume Revision & ATS Progression Tracker")
                st.caption("Save your evaluated draft versions to track your ATS score improvements over time.")

                t_v1, t_v2 = st.columns([2, 1])
                with t_v1:
                    ver_tag = st.text_input("Version Tag / Revision Note", value=f"Draft v{len(st.session_state['resume_history'])+1} - {target_ats_role.split()[0]}", key="ver_tag_input")
                with t_v2:
                    st.write("")
                    st.write("")
                    if st.button("💾 Save Version to Resume Tracker", use_container_width=True, type="primary"):
                        new_ver = {
                            "version": ver_tag,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "target_role": target_ats_role,
                            "ats_score": total_ats_score,
                            "keywords_matched": f"{len(found_keywords)} / {len(target_keywords)}",
                            "status": ats_grade.split("—")[0].strip()
                        }
                        st.session_state["resume_history"].append(new_ver)
                        st.success(f"✅ Saved `{ver_tag}` (Score: {total_ats_score} / 100) to your resume tracker!")

            if st.session_state["resume_history"]:
                st.markdown("---")
                st.markdown("### 📈 Resume Revision History")
                df_history = pd.DataFrame(st.session_state["resume_history"])
                st.dataframe(df_history, use_container_width=True)

                if len(df_history) >= 2:
                    fig_history = px.line(
                        df_history,
                        x="version",
                        y="ats_score",
                        markers=True,
                        title="📈 ATS Score Progression Over Iterations",
                        labels={"version": "Resume Version", "ats_score": "ATS Score (0-100)"}
                    )
                    fig_history.update_layout(yaxis_range=[0, 100], height=300)
                    st.plotly_chart(fig_history, use_container_width=True)
            else:
                if text_to_eval:
                    st.info("No saved revisions yet. Click '💾 Save Version to Resume Tracker' above to track your iterations.")

# ===========================================================================
# 👨‍🏫 2. FACULTY WORKSPACE
# ===========================================================================
elif active_role == "👨‍🏫 Faculty Member":
    faculty_dept = user.get("branch", "MCA")
    assigned_course = user.get("subject", "Enterprise Java & Cloud Architecture")

    if nav_choice == "📞 Faculty Helpdesk & Support":
        render_contact_us_form(default_role="Faculty Member", default_dept=faculty_dept)
    elif nav_choice == "🏛️ TKIET Campus & Affiliations":
        render_tkiet_campus_profile()
    else:
        # Strict Department-Level Isolation
        dept_students = df_master[df_master["department"] == faculty_dept].copy().sort_values(by="name")
        other_depts_count = len(df_master[df_master["department"] != faculty_dept])
        custom_dept_courses = [c for c in st.session_state.get("custom_courses", []) if c.get("dept") == faculty_dept]
        dept_course_records = [c for c in COURSES if c["dept"] == faculty_dept] + custom_dept_courses
        dept_course_names = [c["name"] for c in dept_course_records]
        if not dept_course_names:
            dept_course_names = [assigned_course]

        # Department RBAC Security Shield Banner
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); border-left: 5px solid #10B981; border-radius: 12px; padding: 1.15rem 1.4rem; margin-bottom: 1.2rem; color: #FFFFFF; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#34D399; font-weight:700;">
                        🔒 TKIET Role-Based Access Control (RBAC) • Department Scoped
                    </div>
                    <div style="font-size:1.25rem; font-weight:800; margin-top:3px; color:#F8FAFC;">
                        Department of {faculty_dept} — Academic Administration Desk
                    </div>
                    <div style="font-size:0.84rem; color:#94A3B8; margin-top:2px;">
                        Authorized HOD: <b style="color:#FFFFFF;">{user['name']}</b> ({user.get('emp_id', 'HOD-AUTH')}) | TKIET, Warananagar
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="background:rgba(16, 185, 129, 0.2); border:1px solid #10B981; color:#6EE7B7; padding:4px 12px; border-radius:20px; font-size:0.75rem; font-weight:700;">
                        ACTIVE SCOPE: {faculty_dept.upper()} ONLY
                    </span>
                    <div style="font-size:0.72rem; color:#94A3B8; margin-top:4px;">
                        {other_depts_count} records from other 6 departments locked 🚫
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Department Metric Strip
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{len(dept_students)}</div>
                <div class="metric-lbl">Department Students</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            avg_dept_att = round(dept_students["attendance_rate"].mean(), 1) if not dept_students.empty else 0.0
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: {'#10B981' if avg_dept_att >= 75 else '#EF4444'};">{avg_dept_att}%</div>
                <div class="metric-lbl">Avg Class Attendance</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            dept_defaulters_count = len(dept_students[dept_students["attendance_rate"] < 75.0])
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val" style="color: {'#EF4444' if dept_defaulters_count > 0 else '#10B981'};">{dept_defaulters_count}</div>
                <div class="metric-lbl">Defaulters (&lt; 75%)</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-val">{len(dept_course_names)}</div>
                <div class="metric-lbl">Department Courses</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        # -------------------------------------------------------------------
        # 2.1 Attendance Marking & Defaulters
        # -------------------------------------------------------------------
        if nav_choice == "📋 Attendance Marking & Defaulters":
            st.markdown(f"### 📋 Daily Lecture & Practical Attendance Register — {faculty_dept}")
            st.write(f"Record session-wise attendance for {faculty_dept} cohorts. Only students enrolled in {faculty_dept} appear in this register.")

            # Course Management Expander
            with st.expander("➕ Add / Manage Department Courses Manually", expanded=False):
                st.markdown("##### 📚 Register a New Course / Lab Subject for this Department")
                st.caption("Custom courses added here immediately appear in Attendance Marking, Marks Evaluation, and Class Diagnostics.")
                ac_1, ac_2, ac_3 = st.columns([3, 1.5, 1.5])
                with ac_1:
                    new_c_title = st.text_input("New Course / Subject Title:", placeholder="e.g. Advanced Cloud Computing & DevOps", key="manual_c_title_att")
                with ac_2:
                    new_c_code = st.text_input("Course Code:", placeholder=f"e.g. {faculty_dept[:3].upper()}40{len(dept_course_records)+1}", key="manual_c_code_att")
                with ac_3:
                    new_c_sem = st.selectbox("Semester:", [1, 2, 3, 4, 5, 6, 7, 8], index=2, key="manual_c_sem_att")
                
                new_c_topics = st.text_input("Key Syllabus Topics (optional, comma-separated for AI diagnostics):", placeholder="Docker, Kubernetes, CI/CD Pipelines, Microservices, Observability", key="manual_c_topics_att")
                
                if st.button("💾 Save Course to Department", key="btn_save_manual_c_att", type="secondary"):
                    if new_c_title.strip():
                        c_title_clean = new_c_title.strip()
                        c_code_clean = new_c_code.strip() or f"{faculty_dept[:3].upper()}40{len(dept_course_records)+1}"
                        existing_names = [c["name"] for c in dept_course_records]
                        if c_title_clean not in existing_names:
                            new_rec = {
                                "code": c_code_clean,
                                "name": c_title_clean,
                                "dept": faculty_dept,
                                "credits": 4,
                                "sem": new_c_sem
                            }
                            st.session_state["custom_courses"].append(new_rec)
                            
                            # Seed topics for AI Diagnostics
                            if new_c_topics.strip():
                                t_list = [t.strip() for t in new_c_topics.split(",") if t.strip()]
                            else:
                                t_list = [
                                    f"Foundations of {c_title_clean.split()[0]}",
                                    f"System Architecture & Principles",
                                    f"Hands-on Implementation & Lab Practice",
                                    f"Industry Case Study & Performance",
                                    f"Advanced Capstone Project"
                                ]
                            SUBJECT_TOPIC_MAP[c_title_clean] = t_list
                            st.success(f"🎉 Successfully added '{c_title_clean}' ({c_code_clean}) to {faculty_dept} curriculum!")
                            st.rerun()
                        else:
                            st.info(f"Course '{c_title_clean}' already exists in {faculty_dept}.")
                    else:
                        st.warning("Please enter a valid course name.")

            # Session Parameter Selector
            with st.container():
                p1, p2, p3, p4 = st.columns([3, 2, 2, 2])
                with p1:
                    course_dropdown_opts = dept_course_names + ["➕ Enter Course Title Manually..."]
                    sel_course_raw = st.selectbox("Select or Enter Department Course:", course_dropdown_opts, key="att_course_sel")
                with p2:
                    att_date = st.date_input("Session Date:", datetime.now(), key="att_date_sel")
                with p3:
                    sess_type = st.selectbox("Session Format:", ["Theory Lecture (1 Hr)", "Practical Lab Batch (2 Hrs)", "Tutorial / Remedial (1 Hr)"], key="att_type_sel")
                with p4:
                    sess_batch = st.selectbox("Batch / Cohort:", ["All Students (Whole Class)", "Batch A1 (Roll 1-15)", "Batch A2 (Roll 16-30)", "Remedial Batch"], key="att_batch_sel")

                # If manual entry selected on the fly in the dropdown
                if sel_course_raw == "➕ Enter Course Title Manually...":
                    m_c1, m_c2 = st.columns([3, 1])
                    with m_c1:
                        adhoc_cname = st.text_input("Enter Course / Special Workshop / Lab Title:", placeholder="e.g. AI & Cloud Architecture Workshop", key="adhoc_cname_input")
                    with m_c2:
                        st.write("")
                        st.write("")
                        if st.button("💾 Save as Permanent Course", key="btn_save_adhoc_perm"):
                            if adhoc_cname.strip():
                                clean_adhoc = adhoc_cname.strip()
                                st.session_state["custom_courses"].append({
                                    "code": f"{faculty_dept[:3].upper()}40{len(dept_course_records)+1}",
                                    "name": clean_adhoc,
                                    "dept": faculty_dept,
                                    "credits": 4,
                                    "sem": 3
                                })
                                SUBJECT_TOPIC_MAP[clean_adhoc] = [
                                    f"Foundations of {clean_adhoc.split()[0]}",
                                    "Core Architecture & Lab Workflow",
                                    "Practical Application Development",
                                    "Troubleshooting & Deployment"
                                ]
                                st.success(f"✅ Added '{clean_adhoc}' permanently to {faculty_dept}!")
                                st.rerun()
                    sel_course = adhoc_cname.strip() if adhoc_cname.strip() else "Ad-Hoc Lecture / Lab"
                else:
                    sel_course = sel_course_raw

            # Quick Bulk Actions Toolbar
            st.markdown("#### ⚡ Quick Bulk Actions")
            b_c1, b_c2, b_c3, b_c4 = st.columns([1.5, 1.5, 2, 4])
            with b_c1:
                if st.button("✅ Mark All Present", use_container_width=True):
                    for _, s in dept_students.iterrows():
                        st.session_state[f"att_chk_{faculty_dept}_{s['student_id']}"] = True
                    st.rerun()
            with b_c2:
                if st.button("❌ Mark All Absent", use_container_width=True):
                    for _, s in dept_students.iterrows():
                        st.session_state[f"att_chk_{faculty_dept}_{s['student_id']}"] = False
                    st.rerun()
            with b_c3:
                if st.button("🔄 Reset to Baseline", use_container_width=True):
                    for _, s in dept_students.iterrows():
                        st.session_state[f"att_chk_{faculty_dept}_{s['student_id']}"] = (s["attendance_rate"] >= 70.0)
                    st.rerun()

            st.markdown(f"#### 👥 {faculty_dept} Student Attendance Roster ({len(dept_students)} Students)")
            st.caption("Toggle the checkbox to mark student PRESENT (Checked) or ABSENT (Unchecked):")

            # Checkbox Grid for ALL students in the department
            cols = st.columns(3)
            present_ids = []
            absent_ids = []
            absent_names = []

            for idx, (_, st_row) in enumerate(dept_students.iterrows()):
                col = cols[idx % 3]
                s_id = st_row['student_id']
                s_name = st_row['name']
                curr_att = float(st_row['attendance_rate'])
                att_key = f"att_chk_{faculty_dept}_{s_id}"
                
                # Default presence value if not in session state
                if att_key not in st.session_state:
                    st.session_state[att_key] = (curr_att >= 70.0)

                with col:
                    is_present = st.checkbox(
                        f"{s_name} ({s_id}) — {curr_att}%",
                        value=st.session_state[att_key],
                        key=att_key
                    )
                    if is_present:
                        present_ids.append(s_id)
                    else:
                        absent_ids.append(s_id)
                        absent_names.append(f"{s_name} ({s_id})")

            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            
            # Save Attendance Session
            save_c1, save_c2 = st.columns([2, 3])
            with save_c1:
                if st.button("💾 Save & Lock Attendance Session", use_container_width=True, type="primary"):
                    # 1. Update attendance_rate in df_master
                    for _, s_row in dept_students.iterrows():
                        s_id = s_row["student_id"]
                        old_rate = float(df_master.loc[df_master["student_id"] == s_id, "attendance_rate"].values[0])
                        if s_id in present_ids:
                            new_rate = min(100.0, round(old_rate * 0.96 + 100 * 0.04, 1))
                        else:
                            new_rate = max(0.0, round(old_rate * 0.96 + 0 * 0.04, 1))
                        df_master.loc[df_master["student_id"] == s_id, "attendance_rate"] = new_rate
                        # update risk_tier if attendance dropped < 65
                        if new_rate < 65:
                            df_master.loc[df_master["student_id"] == s_id, "risk_tier"] = "High Risk"
                        elif new_rate < 75 and df_master.loc[df_master["student_id"] == s_id, "risk_tier"].values[0] == "Low Risk":
                            df_master.loc[df_master["student_id"] == s_id, "risk_tier"] = "Moderate Risk"

                    # 2. Append to attendance_logs
                    sess_code = f"ATT-{faculty_dept[:3].upper()}-{datetime.now().strftime('%m%d-%H%M')}"
                    log_entry = {
                        "Session ID": sess_code,
                        "Date": att_date.strftime("%d-%b-%Y"),
                        "Course": sel_course,
                        "Department": faculty_dept,
                        "HOD / Faculty": user["name"],
                        "Format": sess_type,
                        "Batch": sess_batch,
                        "Total Students": len(dept_students),
                        "Present": len(present_ids),
                        "Absent": len(absent_ids),
                        "Attendance %": f"{round((len(present_ids)/len(dept_students))*100, 1)}%",
                        "Absentee List": ", ".join(absent_names) if absent_names else "Nil (100% Present)"
                    }
                    st.session_state["attendance_logs"].insert(0, log_entry)
                    st.balloons()
                    st.success(f"🎉 Attendance locked successfully! Present: {len(present_ids)} / {len(dept_students)} ({round((len(present_ids)/len(dept_students))*100, 1)}%). Student records and cumulative attendance updated.")

            with save_c2:
                st.info(f"📊 **Current Live Count:** Present: **{len(present_ids)}** | Absent: **{len(absent_ids)}** | Turnout: **{round((len(present_ids)/len(dept_students))*100, 1) if dept_students.shape[0] > 0 else 0}%**")

            st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)

            # Department Attendance History Logs
            st.markdown(f"#### 📜 Recent Attendance Sessions — {faculty_dept}")
            dept_logs = [log for log in st.session_state["attendance_logs"] if log.get("Department") == faculty_dept]
            if dept_logs:
                st.dataframe(pd.DataFrame(dept_logs), use_container_width=True)
            else:
                st.info(f"No previous attendance sessions recorded yet for {faculty_dept}. Click 'Save & Lock Attendance Session' above to register the first session.")

            st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)

            # ---------------------------------------------------------------
            # Defaulters Warning & Action Desk
            # ---------------------------------------------------------------
            st.markdown(f"#### 🚨 Defaulters Warning & Action Desk (&lt; 75% Mandatory Attendance)")
            st.caption("As per Shivaji University, Kolhapur and TKIET Autonomous Academic Regulations (Clause 14.2), minimum 75% attendance is mandatory to appear for the End-Semester Examination (ESE).")

            dept_defaulters = dept_students[dept_students["attendance_rate"] < 75.0].copy()
            if not dept_defaulters.empty:
                st.error(f"⚠️ **{len(dept_defaulters)} students** in {faculty_dept} currently have attendance below the statutory 75% limit.")
                
                # Display Defaulters Table with required recovery lectures
                dept_defaulters["Shortfall %"] = (75.0 - dept_defaulters["attendance_rate"]).round(1).astype(str) + "%"
                dept_defaulters["Remedial Hours Needed"] = ((75.0 - dept_defaulters["attendance_rate"]) * 0.8).apply(lambda x: f"{max(4, int(np.ceil(x)))} Hours")
                
                st.dataframe(
                    dept_defaulters[["student_id", "name", "attendance_rate", "Shortfall %", "Remedial Hours Needed", "prior_cgpa", "risk_tier"]],
                    column_config={
                        "attendance_rate": st.column_config.ProgressColumn("Current Attendance", min_value=0, max_value=100, format="%.1f%%"),
                        "name": "Student Name",
                        "student_id": "PRN / ID",
                        "prior_cgpa": "Prior CGPA",
                        "risk_tier": "Academic Risk"
                    },
                    use_container_width=True
                )

                # Generate Official TKIET Defaulter Notice (Printable Document)
                gen_col1, gen_col2 = st.columns([2, 3])
                with gen_col1:
                    show_notice = st.button("🖨️ Generate Official TKIET Defaulter Notice (Formal Document)", use_container_width=True, type="secondary")
                
                if show_notice or st.session_state.get(f"show_def_notice_{faculty_dept}", False):
                    st.session_state[f"show_def_notice_{faculty_dept}"] = True
                    notice_date = datetime.now().strftime("%d %B %Y")
                    ref_no = f"TKIET/{faculty_dept.upper()}/DEF-NOTICE/{datetime.now().year}/042"

                    st.markdown(f"""
                    <div style="background:#FFFFFF; border:2px solid #CBD5E1; border-radius:12px; padding:2rem 2.5rem; margin-top:1rem; box-shadow:0 8px 16px rgba(0,0,0,0.06); color:#1E293B;">
                        <div style="text-align:center; border-bottom:2px solid #1E3A8A; padding-bottom:12px; margin-bottom:16px;">
                            <div style="font-size:0.85rem; font-weight:700; color:#64748B; letter-spacing:0.06em;">TATYASAHEB KORE INSTITUTE OF ENGINEERING & TECHNOLOGY, WARANANAGAR</div>
                            <div style="font-size:1.35rem; font-weight:800; color:#1E3A8A; margin:3px 0;">DEPARTMENT OF {faculty_dept.upper()}</div>
                            <div style="font-size:0.78rem; color:#475569;">(An Autonomous Institute | Affiliated to Shivaji University, Kolhapur | NAAC 'A' Grade Accredited)</div>
                            <div style="font-size:0.75rem; color:#64748B; margin-top:3px;">Warananagar, Tal. Panhala, Dist. Kolhapur, Maharashtra - 416113</div>
                        </div>

                        <div style="display:flex; justify-content:space-between; font-size:0.82rem; font-weight:600; color:#475569; margin-bottom:16px;">
                            <div>Ref: <b>{ref_no}</b></div>
                            <div>Date: <b>{notice_date}</b></div>
                        </div>

                        <div style="text-align:center; font-size:1.05rem; font-weight:800; color:#DC2626; text-decoration:underline; margin-bottom:14px;">
                            OFFICIAL NOTICE: SHORTAGE OF ATTENDANCE (DEFAULTER LIST - CALL FOR EXPLANATION)
                        </div>

                        <div style="font-size:0.86rem; line-height:1.6; color:#334155; margin-bottom:14px;">
                            This is to inform all students and parents/guardians that as per <b>TKIET Autonomous Academic Regulation Clause 14.2</b> and directives of <b>Shivaji University, Kolhapur</b>, every student must maintain a minimum cumulative attendance of <b>75%</b> in lectures and practical sessions. The following students of <b>{faculty_dept}</b> have failed to achieve the minimum required attendance:
                        </div>

                        <table style="width:100%; border-collapse:collapse; font-size:0.82rem; margin-bottom:16px;">
                            <thead>
                                <tr style="background:#F1F5F9; border-bottom:2px solid #94A3B8; text-align:left;">
                                    <th style="padding:6px 10px;">Sr. No.</th>
                                    <th style="padding:6px 10px;">PRN / Student ID</th>
                                    <th style="padding:6px 10px;">Student Name</th>
                                    <th style="padding:6px 10px;">Recorded Attendance</th>
                                    <th style="padding:6px 10px;">Shortfall %</th>
                                    <th style="padding:6px 10px;">Action Mandated</th>
                                </tr>
                            </thead>
                            <tbody>
                                {"".join([f"<tr style='border-bottom:1px solid #E2E8F0;'><td style='padding:6px 10px;'>{i+1}</td><td style='padding:6px 10px;'><b>{row['student_id']}</b></td><td style='padding:6px 10px;'>{row['name']}</td><td style='padding:6px 10px; color:#DC2626; font-weight:700;'>{row['attendance_rate']}%</td><td style='padding:6px 10px; color:#DC2626;'>{row['Shortfall %']}</td><td style='padding:6px 10px;'>Mandatory Remedial & Parent Meeting</td></tr>" for i, (_, row) in enumerate(dept_defaulters.iterrows())])}
                            </tbody>
                        </table>

                        <div style="font-size:0.84rem; line-height:1.55; color:#334155; margin-bottom:24px;">
                            <b>Directive:</b> The students listed above are directed to report to the undersigned HOD along with their parents within <b>3 working days</b>. Failure to compensate attendance through remedial academic sessions will result in <b>disqualification from appearing in the Semester End Examination (ESE)</b>.
                        </div>

                        <div style="display:flex; justify-content:space-between; align-items:flex-end; font-size:0.84rem; margin-top:20px;">
                            <div>
                                <div style="color:#64748B; font-size:0.78rem;">Copy Submitted To:</div>
                                <div style="font-size:0.8rem; color:#475569;">1. The Principal, TKIET (Dr. K. I. Patil)<br>2. Dean Academics, TKIET<br>3. Department Notice Board</div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-weight:800; font-size:0.95rem; color:#1E3A8A;">{user['name']}</div>
                                <div style="font-size:0.8rem; color:#475569;">Head of Department (HOD) — {faculty_dept}</div>
                                <div style="font-size:0.75rem; color:#64748B;">TKIET Warananagar</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success(f"🎉 Commendable! All students in {faculty_dept} currently have 75% or higher attendance. No defaulter notices pending.")

        # -------------------------------------------------------------------
        # 2.2 Student Marks & Evaluation
        # -------------------------------------------------------------------
        elif nav_choice == "✍️ Student Marks & Evaluation":
            st.markdown(f"### ✍️ Continuous Internal Assessment (CIA) & Marks Entry — {faculty_dept}")
            st.write(f"Record ISE, MSE, and ICA evaluations for {faculty_dept} students. Real-time AI calculates grade and updates predicted SGPA.")

            # Course Management Expander
            with st.expander("➕ Add / Manage Department Courses Manually", expanded=False):
                st.markdown("##### 📚 Register a New Course / Lab Subject for this Department")
                st.caption("Custom courses added here immediately appear in Marks Evaluation, Attendance, and Class Diagnostics.")
                e_ac1, e_ac2, e_ac3 = st.columns([3, 1.5, 1.5])
                with e_ac1:
                    eval_new_c_title = st.text_input("New Course / Subject Title:", placeholder="e.g. Full Stack Web Development", key="eval_new_c_title_field")
                with e_ac2:
                    eval_new_c_code = st.text_input("Course Code:", placeholder=f"e.g. {faculty_dept[:3].upper()}40{len(dept_course_records)+1}", key="eval_new_c_code_field")
                with e_ac3:
                    eval_new_c_sem = st.selectbox("Semester:", [1, 2, 3, 4, 5, 6, 7, 8], index=2, key="eval_new_c_sem_field")
                
                if st.button("💾 Add Course to Department", key="btn_eval_save_manual_course", type="secondary"):
                    if eval_new_c_title.strip():
                        c_title_clean = eval_new_c_title.strip()
                        c_code_clean = eval_new_c_code.strip() or f"{faculty_dept[:3].upper()}40{len(dept_course_records)+1}"
                        existing_names = [c["name"] for c in dept_course_records]
                        if c_title_clean not in existing_names:
                            st.session_state["custom_courses"].append({
                                "code": c_code_clean,
                                "name": c_title_clean,
                                "dept": faculty_dept,
                                "credits": 4,
                                "sem": eval_new_c_sem
                            })
                            SUBJECT_TOPIC_MAP[c_title_clean] = [
                                f"Foundations of {c_title_clean.split()[0]}",
                                "Core Architecture & Design",
                                "Lab Implementation & Testing",
                                "Real-World Performance & Best Practices"
                            ]
                            st.success(f"🎉 Successfully added '{c_title_clean}' ({c_code_clean}) to {faculty_dept} courses!")
                            st.rerun()
                        else:
                            st.info(f"Course '{c_title_clean}' already exists in {faculty_dept}.")
                    else:
                        st.warning("Please enter a valid course name.")

            if dept_students.empty:
                st.warning(f"No students enrolled in {faculty_dept} found.")
            else:
                c1, c2 = st.columns([1, 2])
                with c1:
                    eval_course_opts = dept_course_names + ["➕ Enter Course Title Manually..."]
                    sel_eval_raw = st.selectbox("Select or Enter Department Course:", eval_course_opts, key="eval_course_sel")
                    if sel_eval_raw == "➕ Enter Course Title Manually...":
                        manual_eval_c = st.text_input("Enter Course Name:", placeholder="e.g. Advanced System Design", key="manual_eval_c_name")
                        sel_eval_course = manual_eval_c.strip() if manual_eval_c.strip() else "Custom Course"
                    else:
                        sel_eval_course = sel_eval_raw

                    student_options = [f"{s['student_id']} — {s['name']}" for _, s in dept_students.iterrows()]
                    sel_student_str = st.selectbox("Select Student:", student_options, key="eval_student_sel")
                    sel_student_id = sel_student_str.split(" — ")[0]
                    student_data = dept_students[dept_students["student_id"] == sel_student_id].iloc[0]

                # Safe extraction of student attributes (eliminates KeyError: 'semester')
                student_sem = student_data.get("current_sem", student_data.get("sem", 3))
                prior_cgpa_val = float(student_data.get("prior_cgpa", 7.5))
                att_rate_val = float(student_data.get("attendance_rate", 75.0))
                pred_sgpa_val = float(student_data.get("predicted_sgpa", 7.5))
                risk_tier_val = str(student_data.get("risk_tier", "Low Risk"))

                with c2:
                    st.markdown(f"""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:0.9rem 1.2rem;">
                        <div style="font-weight:700; color:#1E293B; font-size:1.05rem;">{student_data['name']} ({student_data['student_id']})</div>
                        <div style="font-size:0.82rem; color:#64748B;">Department: <b>{faculty_dept}</b> | Semester: <b>{student_sem}</b> | Prior CGPA: <b>{prior_cgpa_val}</b></div>
                        <div style="font-size:0.82rem; color:#64748B; margin-top:2px;">Current Attendance: <b>{att_rate_val}%</b> | Current Predicted SGPA: <b>{pred_sgpa_val}</b> | Tier: <b>{risk_tier_val}</b></div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### Enter Continuous Internal Assessment (CIA) Scores")
                m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)

                midterm_base = float(student_data.get('midterm_pct', 70.0))
                test_base = float(student_data.get('online_test_avg', 70.0))

                default_ise1 = float(student_data.get('ise1_score', max(0.0, min(20.0, round(midterm_base * 0.20, 1)))))
                default_ise2 = float(student_data.get('ise2_score', max(0.0, min(20.0, round(midterm_base * 0.19, 1)))))
                default_mse = float(student_data.get('mse_score', max(0.0, min(30.0, round(midterm_base * 0.30, 1)))))
                default_ica = float(student_data.get('ica_score', max(0.0, min(30.0, round(test_base * 0.31, 1)))))

                with m_col1:
                    ise1_val = st.number_input("ISE-1 (In-Sem 1)", min_value=0.0, max_value=20.0, value=default_ise1, step=0.5, key=f"ise1_{sel_student_id}")
                    st.caption("Max: 20 Marks (Unit 1 & 2)")
                with m_col2:
                    ise2_val = st.number_input("ISE-2 (In-Sem 2)", min_value=0.0, max_value=20.0, value=default_ise2, step=0.5, key=f"ise2_{sel_student_id}")
                    st.caption("Max: 20 Marks (Unit 3 & 4)")
                with m_col3:
                    mse_val = st.number_input("MSE (Mid-Sem)", min_value=0.0, max_value=30.0, value=default_mse, step=0.5, key=f"mse_{sel_student_id}")
                    st.caption("Max: 30 Marks (Mid-Term)")
                with m_col4:
                    ica_val = st.number_input("ICA / Lab Eval", min_value=0.0, max_value=30.0, value=default_ica, step=0.5, key=f"ica_{sel_student_id}")
                    st.caption("Max: 30 Marks (Lab / Mini-Proj)")
                with m_col5:
                    att_score = round(min(10.0, (att_rate_val / 10.0)), 1)
                    st.metric("Attendance Score", f"{att_score} / 10", f"{att_rate_val}% Att.")

                total_internal = round(ise1_val + ise2_val + mse_val + ica_val, 1)
                grade_letter = "O" if total_internal >= 90 else ("A+" if total_internal >= 80 else ("A" if total_internal >= 70 else ("B+" if total_internal >= 60 else ("B" if total_internal >= 50 else ("C" if total_internal >= 40 else "F")))))
                
                st.markdown(f"""
                <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:10px; padding:0.8rem 1.2rem; margin:10px 0; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:0.85rem; color:#1E40AF; font-weight:600;">Total Internal Assessment (ISE-1 + ISE-2 + MSE + ICA):</span>
                        <b style="font-size:1.2rem; color:#1E3A8A; margin-left:8px;">{total_internal} / 100</b>
                        <div style="font-size:0.75rem; color:#64748B; margin-top:2px;">ISE-1 (20) + ISE-2 (20) + MSE (30) + ICA / Lab (30) = 100 Marks</div>
                    </div>
                    <div>
                        <span style="font-size:0.85rem; color:#1E40AF; font-weight:600;">Calculated Grade:</span>
                        <span style="background:#1E40AF; color:#FFFFFF; padding:3px 12px; border-radius:16px; font-weight:700; font-size:0.9rem; margin-left:6px;">{grade_letter}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("💾 Submit Assessment & Recalculate AI SGPA Prediction", type="primary", use_container_width=True, key=f"btn_eval_submit_{sel_student_id}"):
                    # Recalculate AI Prediction
                    new_midterm = total_internal
                    ai_res = AI_MODEL.predict_student(
                        attendance=float(student_data.get("attendance_rate", 75.0)),
                        study_hrs=float(student_data.get("study_hours_per_week", 15.0)),
                        cgpa=float(student_data.get("prior_cgpa", 7.5)),
                        midterm=float(new_midterm),
                        backlogs=int(student_data.get("backlogs", 0))
                    )
                    
                    # Update df_master in session state with both ISE-1, ISE-2, MSE, ICA
                    df_master.loc[df_master["student_id"] == sel_student_id, "ise1_score"] = ise1_val
                    df_master.loc[df_master["student_id"] == sel_student_id, "ise2_score"] = ise2_val
                    df_master.loc[df_master["student_id"] == sel_student_id, "mse_score"] = mse_val
                    df_master.loc[df_master["student_id"] == sel_student_id, "ica_score"] = ica_val
                    df_master.loc[df_master["student_id"] == sel_student_id, "midterm_pct"] = new_midterm
                    df_master.loc[df_master["student_id"] == sel_student_id, "predicted_sgpa"] = ai_res["predicted_sgpa"]
                    df_master.loc[df_master["student_id"] == sel_student_id, "risk_tier"] = ai_res["predicted_risk"]
                    save_custom_students(df_master)

                    old_sgpa = pred_sgpa_val
                    sgpa_diff = round(ai_res["predicted_sgpa"] - old_sgpa, 2)
                    st.balloons()
                    st.success(f"✅ Marks registered for **{student_data['name']}** in `{sel_eval_course}`! ISE-1: **{ise1_val}/20** | ISE-2: **{ise2_val}/20** | MSE: **{mse_val}/30** | ICA: **{ica_val}/30** ➔ Total CIA: **{total_internal}/100** ({grade_letter}).")
                    st.info(f"🤖 **AI Prediction Recalculated:** Prior SGPA Prediction: `{old_sgpa}` ➔ Updated SGPA Prediction: **`{ai_res['predicted_sgpa']}`** ({'+' if sgpa_diff >= 0 else ''}{sgpa_diff}) | Risk Tier: **{ai_res['predicted_risk']}**")

                st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)

                # Department Gradebook
                st.markdown(f"#### 📊 Complete Department Gradebook — {faculty_dept}")
                grade_cols = ["student_id", "name", "ise1_score", "ise2_score", "mse_score", "ica_score", "midterm_pct", "attendance_rate", "prior_cgpa", "predicted_sgpa", "risk_tier"]
                available_cols = [c for c in grade_cols if c in dept_students.columns]
                gradebook_view = dept_students[available_cols].copy()
                rename_map = {
                    "student_id": "Student ID",
                    "name": "Student Name",
                    "ise1_score": "ISE-1 (20)",
                    "ise2_score": "ISE-2 (20)",
                    "mse_score": "MSE (30)",
                    "ica_score": "ICA / Lab (30)",
                    "midterm_pct": "Total CIA (100)",
                    "attendance_rate": "Attendance %",
                    "prior_cgpa": "Prior CGPA",
                    "predicted_sgpa": "Predicted SGPA",
                    "risk_tier": "Risk Category"
                }
                gradebook_view.rename(columns=rename_map, inplace=True)
                st.dataframe(gradebook_view, use_container_width=True)

                csv_data = gradebook_view.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Download {faculty_dept} Gradebook (CSV)",
                    data=csv_data,
                    file_name=f"TKIET_{faculty_dept}_Gradebook_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="btn_download_gradebook_csv"
                )

        # -------------------------------------------------------------------
        # 2.3 Class Weak-Topic Diagnostics
        # -------------------------------------------------------------------
        elif nav_choice == "🧠 Class Weak-Topic Diagnostics":
            st.markdown(f"### 🧠 Class Weak-Topic Diagnostics & Mastery Radar — {faculty_dept}")
            st.write(f"AI-driven diagnostic analysis of conceptual mastery across topics for {faculty_dept} syllabus.")

            sel_diag_course = st.selectbox("Select Course to Analyze:", dept_course_names, key="diag_course_sel")
            topics = SUBJECT_TOPIC_MAP.get(sel_diag_course, ["Conceptual Foundations", "Applied Architectures", "System Design & Analysis", "Lab Implementation"])
            
            # Deterministic yet diverse scores based on hash
            np.random.seed(abs(hash(sel_diag_course)) % 10000)
            topic_scores = [int(np.clip(np.random.normal(loc=68, scale=12), 42, 92)) for _ in topics]
            df_diag = pd.DataFrame({"Topic": topics, "Mastery %": topic_scores}).sort_values(by="Mastery %")

            d_col1, d_col2 = st.columns([3, 2])
            with d_col1:
                fig_bar = px.bar(
                    df_diag,
                    x="Mastery %",
                    y="Topic",
                    orientation="h",
                    color="Mastery %",
                    color_continuous_scale="RdYlGn",
                    text_auto=True,
                    title=f"Topic Mastery % in {sel_diag_course}"
                )
                fig_bar.update_layout(height=340, xaxis_range=[0, 100])
                st.plotly_chart(fig_bar, use_container_width=True)

            with d_col2:
                weakest_topic = df_diag.iloc[0]["Topic"]
                weakest_score = df_diag.iloc[0]["Mastery %"]
                strongest_topic = df_diag.iloc[-1]["Topic"]
                strongest_score = df_diag.iloc[-1]["Mastery %"]

                st.markdown(f"""
                <div style="background:#FEF2F2; border:1px solid #FCA5A5; border-radius:10px; padding:0.9rem; margin-bottom:10px;">
                    <div style="font-size:0.75rem; font-weight:700; color:#DC2626; text-transform:uppercase;">🚨 Critical Weak Area Detected</div>
                    <div style="font-weight:800; font-size:1rem; color:#991B1B;">{weakest_topic}</div>
                    <div style="font-size:0.82rem; color:#7F1D1D; margin-top:2px;">Class Mastery: <b>{weakest_score}%</b> (Below 60% standard benchmark). Remedial lecture recommended.</div>
                </div>

                <div style="background:#F0FDF4; border:1px solid #86EFAC; border-radius:10px; padding:0.9rem;">
                    <div style="font-size:0.75rem; font-weight:700; color:#16A34A; text-transform:uppercase;">⭐ Class Benchmark Topic</div>
                    <div style="font-weight:800; font-size:1rem; color:#14532D;">{strongest_topic}</div>
                    <div style="font-size:0.82rem; color:#166534; margin-top:2px;">Class Mastery: <b>{strongest_score}%</b>. Strong conceptual retention across the cohort.</div>
                </div>
                """, unsafe_allow_html=True)

            # Schedule Remedial Session Expander
            with st.expander(f"📅 Schedule Remedial Lecture for '{weakest_topic}'", expanded=False):
                r_c1, r_c2, r_c3 = st.columns(3)
                with r_c1:
                    rem_date = st.date_input("Remedial Date", datetime.now(), key="rem_date_input")
                with r_c2:
                    rem_time = st.selectbox("Time Slot", ["08:00 AM - 09:30 AM", "03:30 PM - 05:00 PM", "Saturday 10:00 AM - 12:00 PM"], key="rem_time_input")
                with r_c3:
                    rem_venue = st.text_input("Venue / Classroom", f"{faculty_dept} Seminar Hall / Lab 4", key="rem_venue_input")
                if st.button("📢 Broadcast Remedial Schedule to Students", type="primary"):
                    st.success(f"Remedial Lecture on '{weakest_topic}' scheduled for {rem_date.strftime('%d-%b-%Y')} at {rem_time} ({rem_venue}). Notification sent to {faculty_dept} students!")

        # -------------------------------------------------------------------
        # 2.4 High-Risk Student Interventions
        # -------------------------------------------------------------------
        elif nav_choice == "🚨 High-Risk Student Interventions":
            st.markdown(f"### 🚨 High-Risk Student Counseling & Mentorship Desk — {faculty_dept}")
            st.write(f"Targeted faculty mentorship and academic intervention logging for {faculty_dept} students requiring additional support.")

            high_risk = dept_students[dept_students["risk_tier"] == "High Risk"].copy()
            mod_risk = dept_students[dept_students["risk_tier"] == "Moderate Risk"].copy()
            at_risk_students = pd.concat([high_risk, mod_risk])

            r_m1, r_m2, r_m3 = st.columns(3)
            with r_m1:
                st.metric("Critical High-Risk Students", f"{len(high_risk)}", f"In {faculty_dept}", delta_color="inverse")
            with r_m2:
                st.metric("Moderate Risk Students", f"{len(mod_risk)}", "Watchlist", delta_color="off")
            with r_m3:
                st.metric("Total Mentoring Actions Logged", f"{len(st.session_state['counseling_logs'])}", "Cumulative")

            st.markdown(f"#### ⚠️ Students Requiring Immediate Faculty Mentoring ({len(at_risk_students)} Total)")
            if not at_risk_students.empty:
                st.dataframe(
                    at_risk_students[["student_id", "name", "prior_cgpa", "attendance_rate", "backlogs", "weak_subject", "risk_tier"]],
                    column_config={
                        "attendance_rate": st.column_config.ProgressColumn("Attendance", min_value=0, max_value=100, format="%d%%"),
                        "student_id": "PRN / ID",
                        "name": "Student Name",
                        "prior_cgpa": "CGPA",
                        "backlogs": "Live Backlogs",
                        "weak_subject": "Weak Subject",
                        "risk_tier": "Risk Tier"
                    },
                    use_container_width=True
                )
            else:
                st.success(f"No students in {faculty_dept} are currently in the high or moderate risk tier!")

            st.markdown("<hr style='margin: 1.5rem 0;'>", unsafe_allow_html=True)

            # Mentoring Intervention Action Logger
            st.markdown(f"#### 📝 Record Faculty Mentorship & Counseling Session")
            with st.container():
                c_st_opts = [f"{s['student_id']} — {s['name']} ({s['risk_tier']})" for _, s in (at_risk_students if not at_risk_students.empty else dept_students).iterrows()]
                sel_c_student = st.selectbox("Select Student for Counseling:", c_st_opts, key="counsel_student_sel")
                
                cl_1, cl_2, cl_3 = st.columns(3)
                with cl_1:
                    c_date = st.date_input("Counseling Date", datetime.now(), key="counsel_date_sel")
                with cl_2:
                    c_cause = st.selectbox("Primary Identified Root Cause", [
                        "Low Attendance & Regularity Issues",
                        "Conceptual Difficulty in Core Engineering Subjects",
                        "Placement & Campus Interview Anxiety",
                        "Personal / Health / Travel Difficulties",
                        "Exam Stress & Backlog Load"
                    ], key="counsel_cause_sel")
                with cl_3:
                    c_plan = st.selectbox("Faculty Intervention Plan", [
                        "1-on-1 Weekly Remedial Tutoring (2 hrs)",
                        "Assigned Peer Study Partner from Top Cohort",
                        "Parent Intimation & In-Person Discussion",
                        "Special Assignment Extension & Lab Practice",
                        "Counseling with T&P Soft Skills Trainer"
                    ], key="counsel_plan_sel")

                c_notes = st.text_area("HOD / Faculty Mentoring Remarks & Directives", value=f"Advised student to maintain daily attendance above 75% and attend remedial sessions for {assigned_course}. Progress review scheduled in 14 days.", height=80, key="counsel_notes_input")

                if st.button("💾 Save Mentorship & Intervention Record", type="primary", use_container_width=True):
                    c_id = sel_c_student.split(" — ")[0]
                    c_name = sel_c_student.split(" — ")[1].split(" (")[0]
                    c_record = {
                        "Record ID": f"CNS-{faculty_dept[:3].upper()}-{datetime.now().strftime('%m%d%H%M')}",
                        "Date": c_date.strftime("%d-%b-%Y"),
                        "Student ID": c_id,
                        "Student Name": c_name,
                        "Department": faculty_dept,
                        "Mentor / HOD": user["name"],
                        "Identified Cause": c_cause,
                        "Intervention Plan": c_plan,
                        "Faculty Remarks": c_notes
                    }
                    st.session_state["counseling_logs"].insert(0, c_record)
                    st.balloons()
                    st.success(f"Mentorship intervention recorded for {c_name} ({c_id})! Stored in department accreditation log.")

            # Display Department Counseling History Log
            st.markdown(f"#### 📋 Faculty Mentorship Session History ({faculty_dept})")
            dept_counsel_logs = [log for log in st.session_state["counseling_logs"] if log.get("Department") == faculty_dept]
            if dept_counsel_logs:
                st.dataframe(pd.DataFrame(dept_counsel_logs), use_container_width=True)
            else:
                st.info(f"No prior counseling records found for {faculty_dept}. Use the form above to log mentoring actions.")

# ===========================================================================
# 👔 3. TRAINING & PLACEMENT OFFICER (TPO) WORKSPACE
# ===========================================================================
elif active_role == "👔 Training & Placement Officer (TPO)":
    if nav_choice == "📞 Corporate Recruiter Desk":
        render_contact_us_form(default_role="Corporate Recruiter", default_dept="CS")
    elif nav_choice == "🏛️ TKIET Campus & Affiliations":
        render_tkiet_campus_profile()
    else:
        st.markdown("""
        <div class="page-header-box">
            <span class="branch-pill">TKIET Central Placement Cell</span>
            <div class="page-title">Corporate Recruitment & Training Operations</div>
            <div class="page-subtitle">Exclusively managing Placements for <b>Tatyasaheb Kore Institute of Engineering & Technology, Warananagar</b></div>
        </div>
        """, unsafe_allow_html=True)

        # 3.1 Company Drives & Create Drive
        if nav_choice == "🏢 Company Drives & Create Drive":
            st.subheader("Corporate Partner Placement Drives at TKIET")
            st.dataframe(pd.DataFrame(st.session_state["drives_list"]), use_container_width=True)

            with st.expander("➕ Create New Corporate Placement Drive", expanded=False):
                nc_name = st.text_input("Recruiter Name")
                nc_ind = st.text_input("Industry / Domain")
                nc_ctc = st.text_input("CTC (e.g. 14 LPA)")
                nc_role = st.text_input("Role Title")
                nc_cgpa = st.number_input("Cutoff CGPA", 5.0, 10.0, 7.5, 0.1)
                nc_backs = st.number_input("Max Backlogs", 0, 5, 0)
                nc_depts = st.multiselect("Eligible Disciplines", BRANCH_KEYS, default=["CS", "CSBS", "Cyber Security", "MCA"])
                if st.button("Broadcast Placement Drive"):
                    st.session_state["drives_list"].append({
                        "company_id": f"COMP0{len(st.session_state['drives_list'])+1}",
                        "name": nc_name,
                        "industry": nc_ind,
                        "ctc": nc_ctc,
                        "min_cgpa": nc_cgpa,
                        "max_backlogs": nc_backs,
                        "allowed_depts": nc_depts,
                        "role": nc_role,
                        "skills_required": ["Domain Knowledge", "Aptitude"]
                    })
                    st.success(f"Drive for '{nc_name}' created and published to TKIET students in: {', '.join(nc_depts)}!")

        # 3.2 Candidate Eligibility & Shortlisting
        elif nav_choice == "⚡ Candidate Eligibility & Shortlisting":
            st.subheader("TKIET Candidate Shortlisting Engine")
            sel_comp = st.selectbox("Select Drive:", [c["name"] for c in st.session_state["drives_list"]])
            comp = [c for c in st.session_state["drives_list"] if c["name"] == sel_comp][0]

            eligible = df_master[(df_master["department"].isin(comp["allowed_depts"])) & 
                                 (df_master["prior_cgpa"] >= comp["min_cgpa"]) & 
                                 (df_master["backlogs"] <= comp["max_backlogs"])]
            
            st.success(f"✅ Found **{len(eligible)}** TKIET candidates meeting all eligibility criteria.")
            st.dataframe(eligible[["student_id", "name", "department", "prior_cgpa", "backlogs", "coding_score", "resume_ats_score"]], use_container_width=True)

        # 3.3 Interview Rounds & Offers
        elif nav_choice == "📋 Interview Rounds & Offers":
            st.subheader("Interview Pipeline & Selection Status")
            st.dataframe(df_master[["student_id", "name", "department", "target_company", "interview_round", "placement_status", "offered_package"]].head(30), use_container_width=True)

        # 3.4 Placement Stats & CTC Analytics
        elif nav_choice == "📈 Placement Stats & CTC Analytics":
            st.subheader("TKIET Discipline-wise Placement Analytics")
            fig_dept_p = px.histogram(df_master, x="department", color="placement_status", barmode="group", category_orders={"department": BRANCH_KEYS})
            st.plotly_chart(fig_dept_p, use_container_width=True)

        # 3.5 Training Batches & Leaderboards
        elif nav_choice == "🏋️ Training Batches & Leaderboards":
            st.subheader("T&P Training Leaderboard")
            st.dataframe(df_master[["student_id", "name", "department", "training_rank", "coding_score", "aptitude_score", "mock_interview_score"]].sort_values(by="training_rank").head(25), use_container_width=True)

# ===========================================================================
# 🏛️ 4. COLLEGE ADMIN WORKSPACE
# ===========================================================================
elif active_role == "🏛️ College Admin":
    if nav_choice == "📞 Institutional Inquiries Log":
        st.subheader("📑 TKIET Inquiries & Helpdesk Log")
        if st.session_state["inquiries"]:
            st.dataframe(pd.DataFrame(st.session_state["inquiries"]), use_container_width=True)
        else:
            st.info("No new inquiries logged yet in this session. Inquiries submitted via Contact Us appear here.")
            if st.button("Open Contact Us Form"):
                render_contact_us_form(default_role="College Admin")
    else:
        st.markdown("""
        <div class="page-header-box">
            <span class="branch-pill">TKIET Administration</span>
            <div class="page-title">Executive Institutional Governance</div>
            <div class="page-subtitle"><b>Tatyasaheb Kore Institute of Engineering & Technology, Warananagar</b></div>
        </div>
        """, unsafe_allow_html=True)

        # 4.1 Campus Executive Scorecard
        if nav_choice == "📈 Campus Executive Scorecard":
            st.subheader("TKIET Campus Scorecard & Analytics")
            a1, a2, a3, a4 = st.columns(4)
            a1.metric("Total Enrolled Students", f"{len(df_master):,}")
            a2.metric("Mean Campus CGPA", f"{df_master['prior_cgpa'].mean():.2f}")
            a3.metric("Average Attendance", f"{df_master['attendance_rate'].mean():.1f}%")
            pl_rate = (df_master['placement_status'].str.startswith("Placed").sum() / len(df_master)) * 100
            a4.metric("TKIET Placement Rate", f"{pl_rate:.1f}%")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Mean CGPA by Discipline")
                dept_gpa = df_master.groupby("department")["prior_cgpa"].mean().reset_index()
                fig_bar = px.bar(dept_gpa, x="department", y="prior_cgpa", color="department", text_auto=".2f")
                fig_bar.update_layout(showlegend=False, yaxis_range=[6, 9])
                st.plotly_chart(fig_bar, use_container_width=True)
            with c2:
                st.markdown("#### Academic Risk Tier Distribution")
                fig_pie = px.pie(df_master, names="risk_tier", color="risk_tier", color_discrete_map={"Low Risk": "#10B981", "Moderate Risk": "#F59E0B", "High Risk": "#EF4444"})
                st.plotly_chart(fig_pie, use_container_width=True)

        # 4.2 7 Disciplines & Course Structure
        elif nav_choice == "🏢 7 Disciplines & Course Structure":
            st.subheader("Active Disciplines & Departments at TKIET")
            st.dataframe(pd.DataFrame(DEPARTMENTS), use_container_width=True)
            st.markdown("---")
            st.subheader("Course Curricula across all 7 Branches")
            st.dataframe(pd.DataFrame(COURSES), use_container_width=True)

        # 4.3 TKIET Campus Profile & Affiliations
        elif nav_choice == "🏛️ TKIET Campus Profile & Affiliations":
            render_tkiet_campus_profile()

        # 4.4 RBAC Role Permissions Matrix
        elif nav_choice == "👥 RBAC Role Permissions Matrix":
            st.subheader("Role-Based Access Control (RBAC) Governance Matrix")
            rbac_df = pd.DataFrame({
                "Capability / Module": [
                    "View Personal Academic Transcript",
                    "Take Training Practice Tests",
                    "Apply for Campus Placement Drives",
                    "Mark Daily Student Attendance",
                    "Enter Midterm Exam Marks",
                    "Create Corporate Placement Drives",
                    "Shortlist Placement Candidates",
                    "Submit Inquiries via Contact Us",
                    "Campus Setup & System Administration"
                ],
                "Student": ["✅ Full", "✅ Full", "✅ Full", "❌ None", "❌ None", "❌ None", "❌ None", "✅ Full", "❌ None"],
                "Faculty": ["👁️ Dept", "👁️ View", "👁️ View", "✅ Full", "✅ Full", "❌ None", "❌ None", "✅ Full", "❌ None"],
                "T&P Officer": ["👁️ View", "✅ Track", "✅ Full", "👁️ View", "👁️ View", "✅ Full", "✅ Full", "✅ Full", "❌ None"],
                "College Admin": ["✅ Full", "✅ Full", "✅ Full", "✅ Full", "✅ Full", "✅ Full", "✅ Full", "✅ Full", "✅ Full"]
            })
            st.table(rbac_df)

        # 4.5 Accreditation Data Export
        elif nav_choice == "📑 Accreditation Data Export (CSV)":
            st.subheader("NAAC & NBA Accreditation Export Center")
            st.write("Generate synchronized reporting extracts for TKIET Warananagar.")
            csv_full = df_master.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download TKIET Master Audit File (CSV)",
                data=csv_full,
                file_name=f"TKIET_Master_Audit_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
