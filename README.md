# CareerLens AI — Intelligent Resume Analyzer

CareerLens AI is an AI/ML-based resume analysis system that analyzes a candidate's resume and provides career-related insights.

The system uses **Natural Language Processing (NLP), TF-IDF, and Logistic Regression** to analyze resume text, predict a suitable career category, compare skills with a selected target role, calculate an ATS-style score, and provide recommendations for improving the resume.

---

## 🚀 Features

* 📄 Supports PDF, DOCX, and TXT resumes
* 🧹 Resume text extraction and NLP preprocessing
* 🔎 Automatic technical skill extraction
* 🤖 AI-based career role prediction
* 📊 TF-IDF text feature extraction
* 🧠 Logistic Regression machine learning model
* 🎯 Target-role skill matching
* 📈 ATS-style resume score
* ⚠️ Missing skill identification
* 💡 Personalized resume improvement recommendations
* 🌐 Modern Flask web interface
* 📱 Responsive frontend design
* 📊 Interactive analysis chart
* 🖨️ Printable analysis report

---

## 🧠 How the System Works

The complete workflow of CareerLens AI is:

```text
Resume Upload
      ↓
Text Extraction
      ↓
NLP Cleaning
      ↓
Skill Extraction
      ↓
TF-IDF Feature Extraction
      ↓
Logistic Regression
      ↓
Career Role Prediction
      ↓
Target Role Skill Matching
      ↓
ATS-Style Score
      ↓
Skill Gap Analysis
      ↓
Recommendations
      ↓
Final Resume Analysis
```

---

## 🛠️ Technologies Used

| Technology          | Purpose                      |
| ------------------- | ---------------------------- |
| Python              | Main programming language    |
| Flask               | Web application backend      |
| Pandas              | Dataset processing           |
| NumPy               | Numerical operations         |
| Scikit-learn        | Machine learning             |
| TF-IDF              | Text feature extraction      |
| Logistic Regression | Career-role classification   |
| Joblib              | Saving/loading trained model |
| pdfplumber          | PDF text extraction          |
| python-docx         | DOCX text extraction         |
| HTML                | Frontend structure           |
| CSS                 | Frontend styling             |
| JavaScript          | Frontend interaction         |
| Chart.js            | Analysis visualization       |

---

## 📂 Project Structure

```text
CareerLensAI/
│
├── app.py
├── analyzer.py
├── train_model.py
├── requirements.txt
├── README.md
├── sample_resume.txt
│
├── data/
│   └── resume_dataset.csv
│
├── model/
│   └── career_model.joblib
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── uploads/
```

---

# ⚙️ Installation and Setup

## 1. Check Python

CareerLens AI requires Python.

Check your Python version:

```cmd
py --version
```

or:

```cmd
python --version
```

Python 3.10 or newer is recommended.

---

## 2. Open the Project Folder

Open the `CareerLensAI` folder in **VS Code**.

Open:

```text
Terminal → New Terminal
```

Make sure the terminal is inside the `CareerLensAI` folder.

You can verify this by running:

```cmd
dir
```

You should see:

```text
app.py
analyzer.py
train_model.py
requirements.txt
data
model
templates
static
```

---

## 3. Create Virtual Environment

### Windows

```cmd
py -m venv ven
```
