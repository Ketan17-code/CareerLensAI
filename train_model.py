from pathlib import Path
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE = Path(__file__).parent
data = pd.read_csv(BASE / "data" / "resume_dataset.csv")
X_train, X_test, y_train, y_test = train_test_split(
    data["resume_text"], data["role"], test_size=0.2, random_state=42, stratify=data["role"]
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), stop_words="english", sublinear_tf=True)),
    ("classifier", LogisticRegression(max_iter=2000, random_state=42))
])
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("Test Accuracy:", round(accuracy_score(y_test, pred)*100, 2), "%")
print(classification_report(y_test, pred))

(BASE/"model").mkdir(exist_ok=True)
joblib.dump(model, BASE / "model" / "career_model.joblib")
print("Saved: model/career_model.joblib")
