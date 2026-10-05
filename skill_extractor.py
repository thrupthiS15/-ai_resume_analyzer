import pandas as pd
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def load_skill_dictionary(filepath: str = "data/skill_dictionary.csv") -> Dict[str, str]:
    try:
        source_frame = pd.read_csv(filepath)
        # Fast, clean dictionary comprehension parsing data rows efficiently
        return {str(row['Skill']).strip().lower(): str(row['Category']).strip() 
                for _, row in source_frame.iterrows()}
    except Exception as error_flag:
        logger.error(f"Failed to load vocabulary registry mapping file from {filepath}: {error_flag}")
        return {}

def extract_skills(normalized_text: str, skill_registry: Dict[str, str]) -> Dict[str, List[str]]:
    if not normalized_text or not skill_registry:
        return {}

    individual_tokens = set(normalized_text.split())
    discovered_skills = set()

    for target_skill in skill_registry.keys():
        # Check phrase metrics or isolated terms using set lookup intersections
        if ' ' in target_skill:
            if target_skill in normalized_text:
                discovered_skills.add(target_skill)
        elif target_skill in individual_tokens:
            discovered_skills.add(target_skill)

    # Populate organized technical categories dynamically
    categorized_metrics = {}
    for validated_skill in discovered_skills:
        skill_group = skill_registry[validated_skill]
        categorized_metrics.setdefault(skill_group, []).append(validated_skill.title())

    return categorized_metrics
