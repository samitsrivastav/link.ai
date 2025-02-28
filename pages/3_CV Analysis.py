import streamlit as st
from util import logo
import google.generativeai as genai
import PyPDF2
import os

genai.configure(api_key="AIzaSyDu33zc9s4j6QnmI8yOySl7-cbYx6JWT0o")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills_llm(resume_text):
    prompt = f"""
    You are an AI career advisor. Analyze the following resume and extract all technical skills mentioned.

    Resume:
    {resume_text}

    Return only the skills as a **comma-separated list**.
    """
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    if response.text:
        skills = response.text.split(",")
        return [skill.strip().lower() for skill in skills]
    return []

def identify_best_role(user_skills, role_requirements):
    role_scores = {}
    for role, required_skills in role_requirements.items():
        matched_skills = user_skills.intersection(set(required_skills))
        score = len(matched_skills) / len(required_skills)
        role_scores[role] = score
    best_role = max(role_scores, key=role_scores.get)
    return best_role, role_scores[best_role]

def generate_career_recommendation(resume_text, best_role, missing_skills):
    prompt = f"""
    A user uploaded their resume. Based on their skills, they are best suited for **{best_role}**.
    🔹 **Missing Skills**: {', '.join(missing_skills)}
    Provide structured recommendations.
    """
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    return response.text if response.text else "No recommendation generated."

role_requirements = {
    "Data Scientist": [
        "python", "machine learning", "data science", "tensorflow", "pandas", "sql", 
        "numpy", "scikit-learn", "data visualization", "jupyter", "statistics", 
        "experiment design", "r", "spark", "tableau", "power bi", "feature engineering",
        "a/b testing", "time series analysis", "nlp", "big data"
    ],
    
    "Web Developer": [
        "html", "css", "javascript", "react", "node.js", "express", 
        "typescript", "responsive design", "git", "rest api", "graphql", 
        "webpack", "sass/scss", "redux", "vue.js", "angular", "mongodb", 
        "postgresql", "web security", "aws/azure", "testing"
    ],
    
    "AI Engineer": [
        "python", "deep learning", "tensorflow", "pytorch", "nlp",
        "computer vision", "reinforcement learning", "neural networks", "gans", 
        "transformers", "hugging face", "keras", "data pipelines", "mlops", 
        "model deployment", "optimization", "cloud ml platforms", "kubernetes",
        "vector databases", "rag systems", "prompt engineering", "llm fine-tuning"
    ],
    
    "Cybersecurity Specialist": [
        "cybersecurity", "penetration testing", "ethical hacking", "network security",
        "vulnerability assessment", "security architecture", "incident response", 
        "threat intelligence", "siem", "cryptography", "secure coding", "digital forensics", 
        "risk assessment", "identity management", "security compliance", "malware analysis", 
        "cloud security", "osint", "soc operations", "red teaming"
    ],
    
    "Cloud Engineer": [
        "aws", "azure", "gcp", "devops", "docker", 
        "terraform", "cloud architecture", "iam", "serverless", "lambda/functions", 
        "s3/blob storage", "ec2/vm instances", "rds/managed databases", "vpc/networking", 
        "load balancing", "auto-scaling", "monitoring", "cost optimization", 
        "cloudformation", "cloud security", "multi-cloud strategies"
    ],
    
    "DevOps Engineer": [
        "devops", "ci/cd", "docker", "kubernetes", "ansible",
        "jenkins", "github actions", "gitlab ci", "infrastructure as code", "terraform", 
        "monitoring", "prometheus", "grafana", "logging", "elk stack", "shell scripting", 
        "python automation", "version control", "configuration management", "site reliability", 
        "incident management", "performance optimization"
    ]
}

# Streamlit UI
st.set_page_config(page_title="link.ai", layout="wide")

# Sidebar for assessment info
with st.sidebar:
    logo()

st.header("Upload your resume (PDF)")
uploaded_file = st.file_uploader("", type=["pdf"])

if uploaded_file:
    with open("uploaded_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    resume_text = extract_text_from_pdf("uploaded_resume.pdf")
    st.subheader("Extracted Resume Text:")
    st.text(resume_text[:500])
    extracted_skills = extract_skills_llm(resume_text)
    st.subheader("Extracted Skills:")
    st.write(extracted_skills)
    best_role, match_score = identify_best_role(set(extracted_skills), role_requirements)
    st.subheader(f"🎯 Recommended Role: {best_role} ({match_score * 100:.2f}% match)")
    missing_skills = set(role_requirements.get(best_role, [])) - set(extracted_skills)
    skill_gap_report = {"Required Skills": list(role_requirements.get(best_role, [])), "Missing Skills": list(missing_skills)}
    st.subheader("📢 Skill Gap Analysis:")
    st.write(skill_gap_report)
    career_advice = generate_career_recommendation(resume_text, best_role, skill_gap_report["Missing Skills"])
    st.subheader("📢 Career Recommendation:")
    st.write(career_advice)
