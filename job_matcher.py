import pandas as pd
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

logger = logging.getLogger(__name__)

def load_job_dataset(filepath: str = "data/job_roles.csv") -> pd.DataFrame:
    try:
        return pd.read_csv(filepath)
    except Exception as error_flag:
        logger.critical(f"Critical execution barrier - Cannot read job profile baseline context: {error_flag}")
        raise error_flag

def calculate_matches(processed_resume: str, reference_job_matrix: pd.DataFrame) -> List[Dict]:
    if reference_job_matrix.empty or not processed_resume:
        return []

    # Map target corpora lists safely
    baseline_requirements = reference_job_matrix['Required Skills'].tolist()
    pipeline_corpus = [processed_resume] + baseline_requirements

    # Execute statistical weight extractions via sparse matrices
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(pipeline_corpus)

    # Isolate array rows for geometric vector calculations
    applicant_vector = feature_matrix[0:1]
    corporate_vectors = feature_matrix[1:]

    # Compute spatial vector projections
    spatial_similarity_scores = cosine_similarity(applicant_vector, corporate_vectors)[0]

    match_metrics_summary = []
    for row_index, matrix_row in reference_job_matrix.iterrows():
        percentage_score = int(min(spatial_similarity_scores[row_index] * 100, 100))
        
        # Clean inline sanitization formatting parsing individual technical requirements
        parsed_skills = [skill.strip().lower() for skill in str(matrix_row['Required Skills']).split(',')]
        
        match_metrics_summary.append({
            "role": matrix_row['Job Role'],
            "score": percentage_score,
            "required_skills": parsed_skills
        })

    # Render sorted collections by prioritized affinity ranking criteria
    return sorted(match_metrics_summary, key=lambda data_node: data_node['score'], reverse=True)
