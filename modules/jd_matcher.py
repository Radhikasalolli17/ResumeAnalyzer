from sentence_transformers import SentenceTransformer, util

class JDMatcher:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception:
            self.model = None

    def calculate_similarity(self, text1, text2):
        if not self.model or not text1 or not text2:
            return 0.0
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        return round(util.cos_sim(emb1, emb2)[0][0].item() * 100, 2)
    
    def match_skills(self, resume_skills, jd_skills):
        if not jd_skills: return [], resume_skills
        r_skills_lower = [s.lower() for s in resume_skills]
        jd_skills_lower = [s.lower() for s in jd_skills]
        matched = [js.title() for js in jd_skills_lower if js in r_skills_lower]
        missing = [js.title() for js in jd_skills_lower if js not in r_skills_lower]
        return matched, missing

    def analyze_match(self, resume_text, jd_text, resume_skills, jd_skills):
        overall_match = self.calculate_similarity(resume_text, jd_text)
        matched, missing = self.match_skills(resume_skills, jd_skills)
        return {
            "overall_match_percentage": overall_match,
            "matched_skills": matched,
            "missing_skills": missing
        }
