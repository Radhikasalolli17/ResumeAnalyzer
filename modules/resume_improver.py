import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

class AIResumeAssistant:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.available = True
        else:
            self.available = False
            self.model = None

    def _generate(self, prompt, fallback_msg="AI features require GEMINI_API_KEY in .env"):
        if not self.available: return fallback_msg
        try:
            return self.model.generate_content(prompt).text
        except Exception as e:
            return f"AI Error: {str(e)}"

    def analyze_resume_quality(self, parsed_resume):
        prompt = f"Analyze the quality of the following resume sections and provide specific improvement suggestions. Resume Data: {parsed_resume}"
        return self._generate(prompt)

    def improve_project_description(self, project_text):
        prompt = f"Improve the following project description using the STAR method without inventing details. Original: {project_text}"
        return self._generate(prompt)

    def generate_professional_summary(self, parsed_resume, target_role):
        prompt = f"Generate a concise 3-5 sentence professional summary for a {target_role} role based ONLY on this resume data: {parsed_resume}. Do not fabricate any experience."
        return self._generate(prompt)

    def generate_interview_questions(self, parsed_resume, target_role, jd_text=""):
        prompt = f"Generate 5 categories of interview questions for a {target_role} role based on this resume and job description. Resume Skills: {parsed_resume.get('skills')}, Experience: {parsed_resume.get('experience')}, JD: {jd_text}"
        return self._generate(prompt)

    def generate_learning_roadmap(self, missing_skills):
        if not missing_skills: return "No missing skills identified."
        prompt = f"Create a 4-week learning roadmap to acquire the following missing skills: {', '.join(missing_skills)}."
        return self._generate(prompt)
        
    def chat_with_resume(self, parsed_resume, user_question):
         prompt = f"You are an AI assistant answering questions about a specific resume. Resume Data: {parsed_resume}. User Question: {user_question}. Answer accurately based ONLY on the provided resume data."
         return self._generate(prompt)

    def generate_cover_letter(self, parsed_resume, target_role, jd_text):
        prompt = f"Generate a professional cover letter for a {target_role} role based on the following resume and job description. Resume: {parsed_resume}, JD: {jd_text}. DO NOT fabricate any experience."
        return self._generate(prompt)
