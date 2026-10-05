import pandas as pd
from typing import List, Dict, Set

def load_skill_dictionary(filepath: str = "data/skill_dictionary.csv") -> Dict[str, str]:
    try:
        df = pd.read_csv(filepath)
        return dict(zip(df['Skill'].str.lower(), df['Category']))
    except Exception:
        return {}

def extract_skills(cleaned_text: str, skill_dict: Dict[str, str]) -> Dict[str, List[str]]:
    found_skills: Set[str] = set()
    words = cleaned_text.split()
    
    for skill in skill_dict.keys():
        if len(skill.split()) > 1:
            if skill in cleaned_text:
                found_skills.add(skill)
        else:
            if skill in words:
                found_skills.add(skill)
                
    categorized: Dict[str, List[str]] = {}
    for skill in found_skills:
        cat = skill_dict[skill]
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(skill.title())
        
    return categorized
