"""
AI & Machine Learning Engine for EduPlan AI
Powers Module 2, 3, 4, 5, 6, and 7:
- Predictive Performance & Risk Classifier
- Weak Topic Diagnostics & Personalized Revision Scheduler
- Career Skill Gap Matching & Roadmap Generator
- Placement Eligibility & Interview Readiness Engine
- AI Resume Improvement & Practice Plan Generator
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

# ---------------------------------------------------------------------------
# 1. Curated Learning Resources & Question Bank (Module 3) - All 7 Departments
# ---------------------------------------------------------------------------
RESOURCE_LIBRARY = {
    # --- Computer Science (CS) ---
    "Dynamic Programming": {
        "notes": "MIT 6.006 Lecture Notes on Memoization & Subproblems",
        "video": "NeetCode Dynamic Programming Masterclass (YouTube)",
        "docs": "GeeksforGeeks DP Blueprint & LeetCode 75",
        "sample_questions": [
            "Explain the difference between Top-down memoization and Bottom-up tabulation.",
            "Write the state recurrence for the 0/1 Knapsack problem.",
            "Given an integer array nums, return the length of the longest strictly increasing subsequence."
        ]
    },
    "Graph Traversal (BFS/DFS)": {
        "notes": "Stanford Graph Algorithms Handout: Adjacency Lists and Visited States",
        "video": "Abdul Bari Graph Theory & Shortest Path Algorithms",
        "docs": "Algorithmica Graph Theory Compendium",
        "sample_questions": [
            "What is the time and space complexity of BFS on an adjacency matrix vs list?",
            "How do you detect a cycle in a directed graph using DFS and recursion stack?",
            "Explain Dijkstra's single-source shortest path algorithm and its priority queue optimization."
        ]
    },
    "Binary Search Trees": {
        "notes": "Data Structures: BST Operations, Balanced AVL Trees, and Rotations",
        "video": "Abdul Bari Binary Search Trees & Tree Traversal (Inorder, Preorder, Postorder)",
        "docs": "GeeksforGeeks Self-Balancing Trees & LeetCode BST Curated List",
        "sample_questions": [
            "How do you validate if a given Binary Tree satisfies the Binary Search Tree property?",
            "Explain AVL Tree left and right rotations with balancing factors (-1, 0, 1).",
            "Write the algorithm to find the lowest common ancestor (LCA) in a BST."
        ]
    },
    "SQL Joins & Subqueries": {
        "notes": "Relational Algebra to SQL: Cardinality, Equi-joins and Outer Joins",
        "video": "Kaggle Intermediate SQL & Alex The Analyst Portfolio Series",
        "docs": "PostgreSQL Official Documentation on Query Optimization & EXPLAIN ANALYZE",
        "sample_questions": [
            "What is the operational difference between a LEFT JOIN and a FULL OUTER JOIN?",
            "Write a query to find the 2nd highest salary from an Employee table using a subquery.",
            "Explain correlated subqueries and why Window Functions (e.g. DENSE_RANK) are often faster."
        ]
    },
    "Indexing & B-Trees": {
        "notes": "Database Internals: Clustered vs Non-Clustered B+ Tree Indices",
        "video": "Hussein Nasser Database Indexing In-Depth",
        "docs": "Use The Index, Luke! SQL Indexing Guide",
        "sample_questions": [
            "Why do relational databases use B+ trees instead of standard Binary Search Trees for disk storage?",
            "What happens to INSERT performance when you create 10 indices on a single table?",
            "Explain what a Covering Index is and how it satisfies an Index-Only Scan."
        ]
    },

    # --- Master of Computer Applications (MCA) ---
    "Spring Boot Microservices": {
        "notes": "Cloud Native Java: Dependency Injection, Spring Boot Starters, Eureka Registry, and Gateway",
        "video": "Java Brains Spring Boot & Microservices Full Architecture Course",
        "docs": "Spring.io Official Documentation & Architecture Reference Guides",
        "sample_questions": [
            "Explain Inversion of Control (IoC) and Dependency Injection (DI) in Spring Boot.",
            "How does Spring Boot Autoconfiguration work using @EnableAutoConfiguration and conditional annotations?",
            "Describe how an API Gateway handles routing, rate limiting, and JWT validation in microservices."
        ]
    },
    "RESTful API Security": {
        "notes": "API Security: JWT Tokens, OAuth2 Authorization Code Flow, CORS, and Rate Limiting",
        "video": "OAuth 2.0 and OpenID Connect (OIDC) in Plain English (YouTube)",
        "docs": "RFC 7519 JSON Web Token (JWT) Standard & OWASP API Security Top 10",
        "sample_questions": [
            "Explain the structure of a JWT (Header, Payload, Signature) and why secrets shouldn't be in payloads.",
            "What is the Cross-Origin Resource Sharing (CORS) preflight request (OPTIONS) and how is it secured?",
            "Explain the architectural difference between 401 Unauthorized and 403 Forbidden HTTP status codes."
        ]
    },
    "Docker Containerization": {
        "notes": "Docker Engine Architecture: Namespaces, Cgroups, and Layer Caching",
        "video": "TechWorld with Nana Docker Complete Tutorial for Beginners",
        "docs": "Docker Official Docs: Best practices for writing Dockerfiles",
        "sample_questions": [
            "What is the fundamental architectural difference between a Docker Container and a Virtual Machine?",
            "Explain multi-stage Docker builds and how they reduce production image size.",
            "How do Docker volumes persist data across container restarts?"
        ]
    },
    "React Component Lifecycle": {
        "notes": "Modern Frontend: Functional Components, Hooks (useState, useEffect, useMemo), and Virtual DOM",
        "video": "Dan Abramov React Philosophy & Official React.dev Interactive Tutorial",
        "docs": "React.dev Official Documentation on State & Side Effects",
        "sample_questions": [
            "Explain the Virtual DOM reconciliation algorithm (Diffing) and how keys optimize list rendering.",
            "What is the difference between useEffect with an empty dependency array vs no array?",
            "How do useMemo and useCallback prevent unnecessary re-renders in complex component trees?"
        ]
    },
    "Node.js & Express": {
        "notes": "Asynchronous JavaScript: Event Loop, Non-blocking I/O, Middleware Pipeline, and Express Routers",
        "video": "Academind Node.js & Express.js - The Complete Guide",
        "docs": "Node.js Official Documentation & Express.js API Reference",
        "sample_questions": [
            "Explain the Node.js Event Loop phases (Timers, Pending Callbacks, Poll, Check, Close).",
            "What is middleware in Express and how does calling next() control the request-response cycle?",
            "How do you handle unhandled promise rejections and asynchronous errors in production Node.js apps?"
        ]
    },

    # --- Mechanical Engineering (Mechanical) ---
    "Carnot Cycle & Entropy": {
        "notes": "Engineering Thermodynamics Principles: Carnot Cycle, Clausius Inequality, and Entropy Generation",
        "video": "NPTEL Thermodynamics Masterclass by Prof. S.K. Som (IIT Kharagpur)",
        "docs": "NIST Thermodynamic Properties & Standard Cycle Solver Documentation",
        "sample_questions": [
            "Explain the Carnot Theorem and derive the efficiency formula for a Carnot heat engine.",
            "What is the Clausius inequality and how does it establish the definition of entropy?",
            "Calculate the maximum theoretical thermal efficiency of a power plant operating between 600°C and 30°C."
        ]
    },
    "Heat Conduction & Convection": {
        "notes": "Fourier's Law, Newton's Law of Cooling, and Dimensionless Convective Numbers (Nu, Re, Pr)",
        "video": "MIT OpenCourseWare Thermal Energy & Heat Transfer Series",
        "docs": "Incropera Fundamentals of Heat and Mass Transfer Guide",
        "sample_questions": [
            "Derive the one-dimensional steady-state heat conduction equation through a composite cylindrical wall.",
            "Define the physical significance of the Nusselt Number and Reynolds Number in forced convection.",
            "Explain the concept of critical thickness of insulation for a small electrical wire or pipe."
        ]
    },
    "Rankine Power Cycles": {
        "notes": "Steam Power Plants: Ideal Rankine Cycle, Superheating, and Reheat Regenerative Optimization",
        "video": "IIT Kharagpur Applied Thermodynamics: Vapor Power Cycles",
        "docs": "Thermodynamic Steam Tables and Mollier Diagram Blueprint",
        "sample_questions": [
            "How does reheating of steam improve turbine blade life and thermal efficiency in a Rankine cycle?",
            "Explain the regenerative feedwater heating process and its thermodynamic advantages.",
            "Draw the T-s diagram of an ideal reheat-regenerative Rankine cycle."
        ]
    },
    "SolidWorks 3D Modeling": {
        "notes": "Parametric CAD Modeling: Feature Trees, Geometric Relations, and Assembly Mates",
        "video": "SOLIDWORKS CSWP Certification Training Course (YouTube)",
        "docs": "Dassault Systèmes SOLIDWORKS Official Design Handbook",
        "sample_questions": [
            "What is the difference between an Under-defined, Fully-defined, and Over-defined sketch in SolidWorks?",
            "Explain the function of Mates (Coincident, Concentric, Distance) in mechanical assembly modeling.",
            "How do you perform design table-driven configurations in parametric 3D parts?"
        ]
    },
    "Finite Element Analysis (FEA)": {
        "notes": "Finite Element Method Formulation: Discretization, Shape Functions, and Stress Tensors",
        "video": "ANSYS Mechanical FEA Simulation Mastery Series",
        "docs": "ANSYS User Documentation & Meshing Best Practices",
        "sample_questions": [
            "Explain the role of element quality and mesh convergence in structural stress analysis.",
            "What is Von Mises stress and how is it used to predict ductile material failure?",
            "Distinguish between static structural analysis and transient modal vibration analysis."
        ]
    },
    "PLC & SCADA Basics": {
        "notes": "Industrial Automation: Ladder Logic, Relays, Timers, Counters, and HMI Protocols",
        "video": "Siemens SIMATIC S7-1200 / Allen Bradley PLC Automation Course",
        "docs": "IEC 61131-3 Programming Languages for Industrial Automation",
        "sample_questions": [
            "Write a basic Ladder Logic diagram for a motor Start/Stop circuit with seal-in latch.",
            "What is the difference between Normally Open (NO) and Normally Closed (NC) contacts in PLC programming?",
            "Explain how SCADA communicates with RTUs and PLCs via Modbus/OPC-UA."
        ]
    },

    # --- Cyber Security Engineering ---
    "OWASP Top 10 Exploitation": {
        "notes": "Web Application Security Blueprint: SQLi, XSS, CSRF, SSRF, and Broken Access Control",
        "video": "PortSwigger Web Security Academy Deep Dive by Rana Khalil",
        "docs": "OWASP Foundation Official Web Security Testing Guide (WSTG)",
        "sample_questions": [
            "Explain the difference between Stored XSS, Reflected XSS, and DOM-based XSS with remediation strategies.",
            "How do parameterized SQL queries prevent SQL injection at the database engine level?",
            "Describe a Server-Side Request Forgery (SSRF) attack scenario and how to mitigate it in cloud environments."
        ]
    },
    "Network Vulnerability Scanning": {
        "notes": "Host Discovery, Port Auditing, Service Fingerprinting, and Vulnerability Assessment",
        "video": "Network Security Auditing with Nmap, Nessus, and Wireshark",
        "docs": "Nmap Network Scanning by Gordon Lyon & NIST NVD CVE Database",
        "sample_questions": [
            "Explain the difference between a TCP SYN Stealth scan (-sS) and a TCP Connect scan (-sT) in Nmap.",
            "How does banner grabbing assist an analyst in identifying vulnerable service versions?",
            "What is CVSS scoring and how do Base, Temporal, and Environmental metrics determine risk priority?"
        ]
    },
    "Burp Suite & Metasploit": {
        "notes": "Offensive Security Protocols: Proxy Interception, Repeater, Intruder, and Payload Exploitation",
        "video": "The Cyber Mentor Practical Ethical Hacking Masterclass",
        "docs": "OffSec Penetration Testing Documentation & Metasploit Unleashed",
        "sample_questions": [
            "How do you configure upstream proxies and SSL interception certificates in Burp Suite?",
            "Explain the difference between staged and non-staged payloads in the Metasploit Framework.",
            "What precautions must be taken during penetration testing to prevent denial-of-service in production?"
        ]
    },
    "RSA & Elliptic Curve Math": {
        "notes": "Asymmetric Cryptography: Euler's Totient, Prime Factorization, Discrete Logs, and ECDSA",
        "video": "Computerphile Cryptography Series: Diffie-Hellman, RSA, and Elliptic Curves",
        "docs": "RFC 8446 TLS 1.3 Cryptographic Standards & NIST FIPS 186-4",
        "sample_questions": [
            "Why is Elliptic Curve Cryptography (ECC) preferred over RSA for mobile and IoT devices?",
            "Explain key generation in RSA: selection of p, q, n, phi(n), e, and calculation of private exponent d.",
            "How does the Diffie-Hellman Key Exchange achieve forward secrecy across untrusted networks?"
        ]
    },
    "Zero-Trust Firewalls": {
        "notes": "Next-Gen Network Defense: Micro-segmentation, Identity-Aware Proxies, and Packet Inspection",
        "video": "John Kindervag Zero Trust Architecture & Palo Alto Networks Blueprint",
        "docs": "NIST SP 800-207 Zero Trust Architecture Guidelines",
        "sample_questions": [
            "What is the foundational premise of 'Never Trust, Always Verify' in Zero-Trust Architecture?",
            "Explain Stateful Packet Inspection (SPI) vs Deep Packet Inspection (DPI) in Next-Gen Firewalls.",
            "How does micro-segmentation contain lateral movement of attackers within a data center?"
        ]
    },
    "SIEM Log Threat Hunting": {
        "notes": "Security Information & Event Management: Syslog Ingestion, Correlation Rules, and MITRE ATT&CK",
        "video": "Splunk Enterprise Security & Elastic SIEM Threat Hunting Tutorial",
        "docs": "Splunk Documentation & MITRE ATT&CK Enterprise Framework",
        "sample_questions": [
            "Write a search query logic to detect Pass-the-Hash or abnormal privilege escalation in Windows Event Logs.",
            "Explain how correlation rules link multiple low-severity alerts into a high-severity security incident.",
            "Map a typical ransomware kill chain to the MITRE ATT&CK matrix."
        ]
    },

    # --- Electronics & Telecommunication (E&TC) ---
    "ARM Cortex Architecture": {
        "notes": "32-bit Embedded Computing: ARM Cortex-M Pipeline, Registers, Memory Map, and NVIC",
        "video": "FastBit Embedded Brain Academy: ARM Cortex-M Microcontroller Programming",
        "docs": "ARM Cortex-M Generic User Guide & STM32 Reference Manual",
        "sample_questions": [
            "Explain the Nested Vectored Interrupt Controller (NVIC) and how priority grouping works in ARM Cortex-M.",
            "What is the difference between Thread Mode and Handler Mode, and Privileged vs Unprivileged execution?",
            "Explain memory-mapped I/O and how peripheral registers are accessed using C pointers."
        ]
    },
    "UART/SPI/I2C Protocols": {
        "notes": "Serial Communication Protocols: Timing Diagrams, Clock Polarity (CPOL/CPHA), and Multi-Master Bus",
        "video": "Embedded Serial Protocols In-Depth: I2C, SPI, UART by Microchip / Phil's Lab",
        "docs": "NXP I2C Bus Specification & Motorola SPI Application Notes",
        "sample_questions": [
            "Compare UART, SPI, and I2C in terms of pin count, speed, transmission distance, and synchronization.",
            "Explain how I2C handles bus arbitration and clock stretching in multi-master setups.",
            "What do CPOL (Clock Polarity) and CPHA (Clock Phase) settings represent in SPI mode 0, 1, 2, and 3?"
        ]
    },
    "Real-Time OS (RTOS)": {
        "notes": "Deterministic Embedded Systems: Task Scheduling, Preemption, Mutexes, Semaphores, and Queue Management",
        "video": "FreeRTOS Fundamentals and Practical ESP32 Kernel Tutorial",
        "docs": "FreeRTOS Official Kernel Documentation & API Reference",
        "sample_questions": [
            "Explain Priority Inversion in RTOS and how Priority Inheritance Mutexes solve it.",
            "What is the difference between a Binary Semaphore, Counting Semaphore, and Mutex?",
            "How does the RTOS SysTick timer manage task time slicing and delay functions?"
        ]
    },
    "MQTT & CoAP Protocols": {
        "notes": "Lightweight IoT Messaging: Publish-Subscribe Pattern, QoS Levels, and UDP-based CoAP",
        "video": "IoT Communication Protocols Masterclass by IBM Developer",
        "docs": "OASIS MQTT v5.0 Specification & Eclipse Paho Documentation",
        "sample_questions": [
            "Explain the differences between MQTT QoS 0 (At most once), QoS 1 (At least once), and QoS 2 (Exactly once).",
            "Why is MQTT preferred over HTTP for battery-powered sensor nodes?",
            "How does the MQTT Last Will and Testament (LWT) feature alert subscribers of unexpected client disconnects?"
        ]
    },

    # --- Computer Science & Business Systems (CSBS) ---
    "Predictive Sales Forecasting": {
        "notes": "Business Analytics: Time Series Decomposition (Trend, Seasonality, Residuals), ARIMA, and Prophet",
        "video": "Forecasting Principles & Practice by Rob J Hyndman (Monash University)",
        "docs": "Meta Prophet & Statsmodels Time Series Analysis Documentation",
        "sample_questions": [
            "What is stationarity in a time series and how does the Augmented Dickey-Fuller (ADF) test verify it?",
            "Explain the components of an ARIMA(p, d, q) model and how ACF/PACF plots guide parameter choice.",
            "How do you evaluate sales forecast accuracy using MAPE, RMSE, and MAE metrics?"
        ]
    },
    "ERP SAP Architecture": {
        "notes": "Enterprise Systems: 3-Tier Architecture, SAP S/4HANA Core Modules (MM, SD, FI/CO), and Data Integration",
        "video": "SAP Enterprise Architecture & Business Process Integration Masterclass",
        "docs": "SAP S/4HANA Enterprise Cloud Reference Architecture",
        "sample_questions": [
            "Explain the 3-tier client-server architecture of SAP (Presentation, Application, Database layers).",
            "Describe the integration touchpoints between the Sales & Distribution (SD) and Materials Management (MM) modules.",
            "How does in-memory column-oriented database processing in SAP HANA accelerate real-time analytics?"
        ]
    },
    "Time Series Econometrics": {
        "notes": "Financial Analytics: Autoregressive Models, Volatility Clustering (ARCH/GARCH), and Cointegration",
        "video": "Econometrics with R / Python by Ben Lambert (Oxford)",
        "docs": "Greene's Econometric Analysis & Statsmodels Econometrics Blueprint",
        "sample_questions": [
            "Explain Granger Causality and how it tests whether one financial time series forecasts another.",
            "What is volatility clustering and why are GARCH models used to model financial asset returns?",
            "Explain the concept of cointegration in pairs trading and econometric equilibrium."
        ]
    },
    "Design Sprint Prototyping": {
        "notes": "Design Thinking: 5-Day Google Ventures Sprint (Understand, Diverge, Decide, Prototype, Test)",
        "video": "Google Ventures Design Sprint Walkthrough by Jake Knapp",
        "docs": "Stanford d.school Design Thinking Bootleg Guide",
        "sample_questions": [
            "What is the objective of the 'How Might We' (HMW) framework during the empathy phase?",
            "Explain why user testing with just 5 representative users reveals ~85% of usability issues.",
            "Distinguish between low-fidelity paper wireframes and high-fidelity interactive Figma prototypes."
        ]
    },

    # --- Master of Business Administration (MBA) ---
    "DCF Financial Modeling": {
        "notes": "Corporate Valuation: Free Cash Flow to Firm (FCFF), Terminal Value, WACC, and Sensitivity Tables",
        "video": "Aswath Damodaran (NYU Stern) Corporate Valuation & DCF Course",
        "docs": "Corporate Finance Institute (CFI) Financial Modeling Guidelines",
        "sample_questions": [
            "Walk through how you calculate Unlevered Free Cash Flow starting from Operating Income (EBIT).",
            "Explain the Weighted Average Cost of Capital (WACC) and how Capital Asset Pricing Model (CAPM) determines cost of equity.",
            "How do you calculate Terminal Value using the Gordon Growth Perpetuity Method vs Exit Multiple Method?"
        ]
    },
    "Capital Asset Pricing Model": {
        "notes": "Portfolio Theory: Risk-free Rate, Beta (Systematic Risk), Market Risk Premium, and Security Market Line",
        "video": "MIT Sloan Finance Theory: Modern Portfolio Theory and CAPM",
        "docs": "Investopedia Educational Finance Guide: Understanding CAPM",
        "sample_questions": [
            "Define Beta and explain the difference between systematic (undiversifiable) and unsystematic risk.",
            "How does the Security Market Line (SML) identify whether a stock is overvalued or undervalued?",
            "What are the key simplifying assumptions of CAPM and where does it face real-world limitations?"
        ]
    },
    "Customer Lifetime Value (CLV)": {
        "notes": "Strategic Marketing: Cohort Retention, Churn Rate, Customer Acquisition Cost (CAC), and CLV:CAC Ratio",
        "video": "Wharton Customer Analytics Masterclass by Prof. Peter Fader",
        "docs": "Harvard Business Review: The Value of Keeping the Right Customers",
        "sample_questions": [
            "Derive the basic formula for Customer Lifetime Value (CLV = Margin * Retention / (1 + Discount - Retention)).",
            "Why is a CLV to CAC ratio of 3:1 considered the golden standard for scalable SaaS businesses?",
            "Explain how cohort retention curves help diagnose product-market fit."
        ]
    },
    "Brand Positioning": {
        "notes": "Marketing Strategy: Keller's Brand Equity Pyramid, Perceptual Mapping, and Value Propositions",
        "video": "Philip Kotler Marketing Management Principles & Positioning Case Studies",
        "docs": "Kellogg School of Management Strategic Marketing Framework",
        "sample_questions": [
            "Construct a Perceptual Positioning Map comparing top automotive or consumer tech brands.",
            "What are Points of Parity (POPs) vs Points of Difference (PODs) in brand strategy?",
            "Explain how the Net Promoter Score (NPS) correlates with brand loyalty and organic referral growth."
        ]
    }
}

DEFAULT_RESOURCE = {
    "notes": "Comprehensive Engineering Reference Handbook & Lecture Notes",
    "video": "NPTEL & MIT OpenCourseWare Video Lecture Series",
    "docs": "Developer Documentation & Interactive Code Playgrounds",
    "sample_questions": [
        "Explain the core theoretical principles underlying this subject.",
        "Derive the mathematical formulation or algorithmic implementation.",
        "Solve a practical scenario-based design problem using this concept."
    ]
}

# ---------------------------------------------------------------------------
# 2. Predictive Performance Model
# ---------------------------------------------------------------------------
class AcademicAIEngine:
    def __init__(self):
        self.gpa_model = RandomForestRegressor(n_estimators=80, random_state=42)
        self.risk_model = RandomForestClassifier(n_estimators=80, random_state=42)
        self.is_trained = False

    def train(self, df_master: pd.DataFrame):
        features = ["attendance_rate", "study_hours_per_week", "prior_cgpa", "midterm_pct", "backlogs"]
        X = df_master[features]
        y_gpa = df_master["predicted_sgpa"]
        y_risk = df_master["risk_tier"]

        self.gpa_model.fit(X, y_gpa)
        self.risk_model.fit(X, y_risk)
        self.is_trained = True

    def predict_student(self, attendance: float, study_hrs: float, cgpa: float, midterm: float, backlogs: int) -> Dict[str, Any]:
        X_test = pd.DataFrame([{
            "attendance_rate": attendance,
            "study_hours_per_week": study_hrs,
            "prior_cgpa": cgpa,
            "midterm_pct": midterm,
            "backlogs": backlogs
        }])
        pred_gpa = round(float(self.gpa_model.predict(X_test)[0]), 2)
        pred_risk = self.risk_model.predict(X_test)[0]
        risk_probs = dict(zip(self.risk_model.classes_, [round(float(p), 2) for p in self.risk_model.predict_proba(X_test)[0]]))

        return {
            "predicted_sgpa": max(3.0, min(10.0, pred_gpa)),
            "predicted_risk": pred_risk,
            "probabilities": risk_probs
        }

# ---------------------------------------------------------------------------
# 3. AI Module 7: Career & Placement Assistant Logic
# ---------------------------------------------------------------------------
def analyze_resume_ats(skills: List[str], target_role: str, projects_count: int, has_github: bool, has_internship: bool) -> Dict[str, Any]:
    """
    Evaluates student resume score (0-100) and produces actionable AI suggestions.
    """
    base_score = 40
    feedback = []
    missing_items = []

    # Skill volume
    skill_pts = min(25, len(skills) * 4)
    base_score += skill_pts

    # Project checks
    if projects_count >= 3:
        base_score += 15
        feedback.append("✅ Strong portfolio with 3+ technical projects.")
    elif projects_count == 2:
        base_score += 10
        feedback.append("⚠️ Good project foundation, but adding 1 production-grade full-stack/ML project is recommended.")
    else:
        base_score += 5
        missing_items.append("Add at least 2 end-to-end deployed projects with live demo URLs.")

    # GitHub profile
    if has_github:
        base_score += 10
        feedback.append("✅ Active GitHub profile linked with consistent commit history.")
    else:
        missing_items.append("Add your GitHub profile showcasing clean, documented code and README files.")

    # Internship experience
    if has_internship:
        base_score += 10
        feedback.append("✅ Practical industry internship experience included.")
    else:
        missing_items.append("Complete a 4-8 week virtual internship or Open Source contribution (GSoC/Hacktoberfest).")

    # Target role keyword density
    role_keywords = {
        "Data Scientist": ["Python", "Machine Learning", "SQL", "Pandas", "Statistics"],
        "Full Stack Software Engineer": ["React", "Node.js", "SQL", "Git", "REST APIs"],
        "Cloud Solutions Architect": ["AWS", "Docker", "Kubernetes", "Linux"]
    }
    required = role_keywords.get(target_role, ["Python", "SQL", "Git"])
    missing_core = [k for k in required if k not in skills]
    if missing_core:
        missing_items.append(f"Target role keywords missing from resume: {', '.join(missing_core)}")

    ats_score = min(98, base_score)
    grade = "Excellent (Interview Ready)" if ats_score >= 85 else ("Competitive" if ats_score >= 70 else "Needs Improvement")

    return {
        "ats_score": ats_score,
        "grade": grade,
        "strengths": feedback,
        "actionable_improvements": missing_items
    }

def generate_personalized_study_plan(weak_topics: List[str], available_hrs: float) -> List[Dict[str, str]]:
    """
    Creates an adaptive 4-week personalized study and revision schedule.
    """
    schedule = []
    days = ["Week 1: Foundations & Concept Clarification",
            "Week 2: Deep Dive & Code Implementation",
            "Week 3: Practice Problem Solving & Time Trials",
            "Week 4: Mock Testing & Comprehensive Revision"]

    daily_hrs = round(available_hrs / 6.0, 1)

    for i, week_title in enumerate(days):
        topic_idx = i % len(weak_topics) if weak_topics else 0
        current_topic = weak_topics[topic_idx] if weak_topics else "General Engineering Mathematics"
        res = RESOURCE_LIBRARY.get(current_topic, DEFAULT_RESOURCE)

        schedule.append({
            "phase": week_title,
            "focus_topic": current_topic,
            "daily_target": f"{daily_hrs} hours/day",
            "primary_resource": res["video"],
            "deliverable": f"Solve 15 practice questions from {res['notes']}"
        })

    return schedule
