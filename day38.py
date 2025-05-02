# pip install pdfplumber sklearn sentence-transformers pandas
import pdfplumber
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast & accurate

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text
def rank_resumes(resume_folder, job_description):
    scores = []
    job_embedding = model.encode([job_description])[0]

    for filename in os.listdir(resume_folder):
        if filename.endswith('.pdf'):
            full_path = os.path.join(resume_folder, filename)
            resume_text = extract_text_from_pdf(full_path)
            resume_embedding = model.encode([resume_text])[0]
            similarity = cosine_similarity([job_embedding], [resume_embedding])[0][0]
            scores.append((filename, similarity))

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores
def main():
    job_desc = input("📋 Enter the job description:\n")
    folder = input("📁 Enter path to folder containing resumes: ").strip()

    print("🧠 Scanning and ranking resumes...")
    ranked = rank_resumes(folder, job_desc)
    df = pd.DataFrame(ranked, columns=["Resume", "Relevance Score"])
    df.to_csv("ranked_resumes.csv", index=False)
    print("✅ Done! Results saved to 'ranked_resumes.csv'")
    print(df)