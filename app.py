import streamlit as st
import pandas as pd
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_dataset, calculate_matches
from roadmap_generator import analyze_gaps_and_roadmap

st.set_page_config(page_title="AI Resume Analyzer", layout="wide", page_icon="📊")
st.title("📊 AI Resume Analyzer & Job Recommendation System")

skill_dict = load_skill_dictionary()
job_df = load_job_dataset()

uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX format)", type=["pdf", "docx"])

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    with st.spinner("Extracting content safely..."):
        if file_type == "pdf":
            raw_text = extract_text_from_pdf(uploaded_file)
        else:
            raw_text = extract_text_from_docx(uploaded_file)
            
    if not raw_text.strip():
        st.error("Could not extract legible text. Please upload a clear document.")
    else:
        cleaned_text = clean_text(raw_text)
        categorized_skills = extract_skills(cleaned_text, skill_dict)
        match_results = calculate_matches(cleaned_text, job_df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💡 Extracted Competencies")
            if not categorized_skills:
                st.info("No predefined skills detected. Update data/skill_dictionary.csv.")
            else:
                for category, skills in categorized_skills.items():
                    st.markdown(f"**{category}**")
                    st.write(", ".join(skills))
            
            st.subheader("🎯 Job Match Rankings")
            match_display_df = pd.DataFrame(match_results)[["role", "score"]].rename(
                columns={"role": "Target Role", "score": "Match Score (%)"}
            )
            st.dataframe(match_display_df, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("🔍 Skill-Gap & Roadmap Analysis")
            available_roles = [r['role'] for r in match_results]
            selected_role = st.selectbox("Select a target role to analyze gaps:", available_roles)
            
            target_info = next(item for item in match_results if item["role"] == selected_role)
            gap_analysis = analyze_gaps_and_roadmap(categorized_skills, target_info["required_skills"])
            
            st.metric(label=f"Match Score for {selected_role}", value=f"{target_info['score']}%")
            
            st.markdown("##### ✅ Skills Found in Resume")
            st.write(", ".join(gap_analysis["matched"]) if gap_analysis["matched"] else "*None detected.*")
                
            st.markdown("##### ⚠️ Missing or Weak Skills")
            if gap_analysis["missing"]:
                st.write(", ".join(gap_analysis["missing"]))
                st.markdown("##### 🗺️ Suggested Learning Roadmap")
                for step in gap_analysis["roadmap"]:
                    st.markdown(f"- {step}")
            else:
                st.success("Perfect alignment! You possess all documented baseline metrics for this role.")
