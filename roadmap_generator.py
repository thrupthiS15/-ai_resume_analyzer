from typing import List, Dict

def analyze_gaps_and_roadmap(extracted_skills_dict: Dict[str, List[str]], required_skills: List[str]) -> Dict:
    flat_extracted = []
    for skills in extracted_skills_dict.values():
        flat_extracted.extend([s.lower() for s in skills])
        
    flat_extracted_set = set(flat_extracted)
    matched = [s.title() for s in required_skills if s in flat_extracted_set]
    missing = [s.title() for s in required_skills if s not in flat_extracted_set]
    
    roadmap = []
    for index, skill in enumerate(missing, start=1):
        roadmap.append(f"Week {index}: Master fundamentals and core labs for **{skill}**")
        
    return {"matched": matched, "missing": missing, "roadmap": roadmap}
