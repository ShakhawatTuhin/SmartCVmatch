import re
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def lemmatize_skill(skill):
    # Lemmatize each word in the skill phrase
    return ' '.join(lemmatizer.lemmatize(word) for word in skill.split())

def extract_skills_from_cv(cv_text):
    skills = set()
    for line in cv_text.splitlines():
        if ':' in line:
            skill_part = line.split(':', 1)[1]
            skill_part = skill_part.lower()
            skill_part = re.sub(r'\(.*?\)', '', skill_part)
            for skill in re.split(r'[;,]', skill_part):
                skill = skill.strip()
                if skill and skill not in [
                    'programming', 'framework and libraries', 'tools', 'databases',
                    'methodologies', 'soft skills'
                ]:
                    lemmatized = lemmatize_skill(skill)
                    skills.add(lemmatized)
    return sorted(skills)

skills = extract_skills_from_cv(cv_text)
print("Extracted skills from CV:", skills)