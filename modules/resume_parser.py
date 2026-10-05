import re
import spacy
from pdfminer.high_level import extract_text, extract_pages

class ResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = ""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            import spacy.cli
            spacy.cli.download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        self.details = {
            "name": "", "email": "", "phone": "", "summary": "",
            "education": [], "skills": [], "experience": [],
            "projects": [], "certifications": [], "achievements": [],
            "languages": [], "no_of_pages": 0, "raw_text": ""
        }
        self.parse()

    def parse(self):
        try:
            self.text = extract_text(self.pdf_path)
            self.details["raw_text"] = self.text
            self.details["no_of_pages"] = len(list(extract_pages(self.pdf_path)))
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return
        
        self.extract_email()
        self.extract_phone()
        self.extract_name()
        self.extract_skills()
        self.extract_sections()
    
    def extract_email(self):
        match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', self.text)
        if match: self.details["email"] = match.group()

    def extract_phone(self):
        match = re.search(r'(\+\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', self.text)
        if match: self.details["phone"] = match.group()

    def extract_name(self):
        doc = self.nlp(self.text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                self.details["name"] = ent.text
                break
        if not self.details["name"]:
            words = self.text.split()
            if len(words) >= 2: self.details["name"] = f"{words[0]} {words[1]}"
                
    def extract_skills(self):
        common_skills = ['python', 'java', 'c++', 'javascript', 'react', 'django', 'sql', 'mysql', 'mongodb', 
                         'machine learning', 'data science', 'html', 'css', 'aws', 'docker', 'kubernetes', 'node.js',
                         'express.js', 'git', 'linux', 'azure', 'gcp', 'spring boot', 'pandas', 'numpy', 'tensorflow',
                         'pytorch', 'scikit-learn']
        text_lower = self.text.lower()
        self.details["skills"] = [skill.title() for skill in common_skills if re.search(rf'\b{re.escape(skill)}\b', text_lower)]

    def extract_sections(self):
        sections = {
            "experience": ["experience", "employment", "work history", "professional experience"],
            "education": ["education", "academic background", "qualifications"],
            "projects": ["projects", "personal projects", "academic projects"],
            "certifications": ["certifications", "certificates", "courses"],
            "achievements": ["achievements", "awards", "honors"],
            "summary": ["summary", "objective", "profile", "about me"]
        }
        lines = self.text.split('\n')
        current_section = None
        for line in lines:
            line_cleaned = line.strip().lower()
            if not line_cleaned: continue
            found_section = False
            for section, keywords in sections.items():
                if any(line_cleaned == kw or line_cleaned.startswith(kw + ":") for kw in keywords):
                    current_section = section
                    found_section = True
                    break
            if not found_section and current_section:
                if isinstance(self.details[current_section], list):
                    self.details[current_section].append(line.strip())
                elif isinstance(self.details[current_section], str):
                    self.details[current_section] += line.strip() + " "
                    
        for key in ["experience", "education", "projects", "certifications", "achievements"]:
            if isinstance(self.details[key], list) and self.details[key]:
                self.details[key] = "\n".join(self.details[key])
            else:
                self.details[key] = ""
        
        if isinstance(self.details["summary"], str):
             self.details["summary"] = self.details["summary"].strip()

    def get_extracted_data(self):
        return self.details
