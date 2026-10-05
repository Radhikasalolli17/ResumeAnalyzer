class ATSScorer:
    def __init__(self, weights=None):
        self.weights = weights or {
            "skills_match": 0.30,
            "experience": 0.25,
            "education": 0.15,
            "projects": 0.15,
            "section_completeness": 0.15
        }

    def score_resume(self, parsed_resume, jd_match_results):
        score_breakdown = {k: 0 for k in self.weights.keys()}
        score_breakdown["formatting"] = 100
        
        matched_skills = jd_match_results.get("matched_skills", [])
        missing_skills = jd_match_results.get("missing_skills", [])
        total_jd_skills = len(matched_skills) + len(missing_skills)
        if total_jd_skills > 0:
            score_breakdown["skills_match"] = (len(matched_skills) / total_jd_skills) * 100
        elif parsed_resume.get("skills"):
            score_breakdown["skills_match"] = 80
            
        score_breakdown["experience"] = 100 if parsed_resume.get("experience") else 0
        score_breakdown["education"] = 100 if parsed_resume.get("education") else 0
        score_breakdown["projects"] = 100 if parsed_resume.get("projects") else 0
            
        sections = ["name", "email", "phone", "skills", "experience", "education"]
        filled_sections = sum(1 for sec in sections if parsed_resume.get(sec))
        score_breakdown["section_completeness"] = (filled_sections / len(sections)) * 100
        
        total_score = sum(score_breakdown[k] * self.weights.get(k, 0) for k in self.weights.keys())
        return {
            "total_score": round(total_score, 2),
            "breakdown": {k: round(v, 2) for k, v in score_breakdown.items()}
        }
