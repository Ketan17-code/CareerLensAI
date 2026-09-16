import re
from pathlib import Path
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(__file__).parent
MODEL = joblib.load(BASE / "model" / "career_model.joblib")

SKILLS = {
    "Python","Java","C++","HTML","CSS","JavaScript","React","Node.js","Express","MongoDB",
    "SQL","MySQL","Data Structures","Algorithms","Machine Learning","Deep Learning",
    "TensorFlow","PyTorch","Scikit-learn","Pandas","NumPy","NLP","Computer Vision",
    "Statistics","Data Analysis","Matplotlib","Seaborn","Power BI","Tableau","Excel",
    "Cybersecurity","Network Security","Linux","Ethical Hacking","Penetration Testing",
    "Wireshark","Firewall","Cryptography","SIEM","Kali Linux","AWS","Azure","GCP",
    "Docker","Kubernetes","Terraform","Jenkins","CI/CD","Cloud Computing","Networking",
    "REST API","Git","Bootstrap","TypeScript","Spring","Debugging","Testing","OOP",
    "Flask","Reporting","Dashboard","Visualization","Frontend"
}
ROLE_SKILLS = {
    "AI/ML Engineer":["Python","Machine Learning","Deep Learning","TensorFlow","PyTorch","Scikit-learn","Pandas","NumPy","NLP","Computer Vision","SQL","Flask"],
    "Data Scientist":["Python","Statistics","Machine Learning","Pandas","NumPy","SQL","Data Analysis","Matplotlib","Seaborn","Scikit-learn","Power BI","Tableau"],
    "Web Developer":["HTML","CSS","JavaScript","React","Node.js","Express","MongoDB","Git","REST API","Bootstrap","TypeScript","Frontend"],
    "Software Developer":["Java","C++","Python","Data Structures","Algorithms","Git","SQL","OOP","REST API","Spring","Debugging","Testing"],
    "Data Analyst":["Excel","SQL","Power BI","Tableau","Python","Pandas","Data Analysis","Statistics","Visualization","Reporting","Dashboard","MySQL"],
    "Cyber Security":["Cybersecurity","Network Security","Linux","Ethical Hacking","Penetration Testing","Wireshark","Firewall","Cryptography","Python","SIEM","Kali Linux"],
    "Cloud Engineer":["AWS","Azure","GCP","Docker","Kubernetes","Linux","Terraform","Jenkins","CI/CD","Python","Cloud Computing","Networking"]
}

def extract_text(path):
    ext = path.suffix.lower()
    if ext == ".txt":
        return path.read_text(errors="ignore")
    if ext == ".pdf":
        try:
            import pdfplumber
            with pdfplumber.open(path) as pdf:
                return "\n".join((p.extract_text() or "") for p in pdf.pages)
        except ImportError:
            raise RuntimeError("PDF support needs pdfplumber. Run: pip install -r requirements.txt")
    if ext == ".docx":
        try:
            from docx import Document
            doc = Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            raise RuntimeError("DOCX support needs python-docx. Run: pip install -r requirements.txt")
    raise RuntimeError("Unsupported file type.")

def clean(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def detect_skills(text):
    low = clean(text)
    found=[]
    for skill in sorted(SKILLS, key=len, reverse=True):
        if skill.lower() in low and skill not in found:
            found.append(skill)
    return found

def analyze_resume(path, target_role):
    text = extract_text(path)
    if len(clean(text)) < 40:
        raise RuntimeError("Resume text is too short. Upload a readable resume.")
    cleaned = clean(text)
    prediction = MODEL.predict([cleaned])[0]
    probabilities = MODEL.predict_proba([cleaned])[0]
    classes = MODEL.classes_
    confidence = float(max(probabilities) * 100)

    found = detect_skills(text)
    required = ROLE_SKILLS.get(target_role, ROLE_SKILLS["AI/ML Engineer"])
    matched = [s for s in required if s.lower() in {x.lower() for x in found}]
    missing = [s for s in required if s not in matched]
    match_pct = round(len(matched)/len(required)*100)

    sections = ["education","experience","projects","skills","certifications","summary","achievements"]
    section_hits = sum(1 for s in sections if s in cleaned)
    keyword_score = min(100, round((len(found)/12)*100))
    section_score = round(section_hits/len(sections)*100)
    length_score = 100 if 350 <= len(cleaned) <= 5000 else 70 if len(cleaned) >= 150 else 35
    ats = round(keyword_score*0.45 + section_score*0.30 + length_score*0.25)
    score = round(match_pct*0.45 + ats*0.35 + confidence*0.20)

    suggestions=[]
    if missing: suggestions.append("Add or strengthen: " + ", ".join(missing[:5]))
    if "projects" not in cleaned: suggestions.append("Add a Projects section with technologies and measurable results.")
    if "experience" not in cleaned: suggestions.append("Add internship, freelance, volunteer, or practical experience.")
    if "certifications" not in cleaned: suggestions.append("Add relevant certifications or courses if you have completed them.")
    if len(cleaned) < 350: suggestions.append("Add more evidence: project outcomes, tools used, and measurable achievements.")
    suggestions = suggestions[:5]

    return {
        "predicted_role": prediction,
        "confidence": round(confidence,1),
        "target_role": target_role,
        "score": score,
        "ats_score": ats,
        "match_percentage": match_pct,
        "skills": found,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions,
        "word_count": len(cleaned.split()),
        "section_count": section_hits
    }
