import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

def load_job_dataset(filepath: str = "data/job_roles.csv") -> pd.DataFrame:
    return pd.read_csv(filepath)

def calculate_matches(cleaned_resume: str, job_df: pd.DataFrame) -> List[Dict]:
    results = []
    vectorizer = TfidfVectorizer()
    job_descriptions = job_df['Required Skills'].tolist()
    corpus = [cleaned_resume] + job_descriptions
    
    tfidf_matrix = vectorizer.fit_transform(corpus)
    resume_vector = tfidf_matrix[0:1]
    job_vectors = tfidf_matrix[1:]
    
    similarities = cosine_similarity(resume_vector, job_vectors)[0]
    
    for idx, row in job_df.iterrows():
        score = int(min(similarities[idx] * 100, 100))
        results.append({
            "role": row['Job Role'],
            "score": score,
            "required_skills": [s.strip().lower() for s in row['Required Skills'].split(',')]
        })
        
    return sorted(results, key=lambda x: x['score'], reverse=True)
