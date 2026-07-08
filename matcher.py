from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_match_score(resume_text, jd_text):
    """
    Returns a 0-100 match score between resume and job description
    using TF-IDF vectors + cosine similarity.
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])

    # cosine_similarity returns a 2x2 matrix; [0][1] is resume-vs-jd similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return round(similarity * 100, 2)


def get_missing_keywords(resume_text, jd_text, skills_list):
    """
    Returns skills that appear in the JD but not in the resume,
    checked against a curated list of known skills/keywords.
    """
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    jd_skills = {skill for skill in skills_list if skill.lower() in jd_lower}
    resume_skills = {
        skill for skill in skills_list if skill.lower() in resume_lower}

    missing = jd_skills - resume_skills
    matched = jd_skills & resume_skills

    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
    }


def get_skill_match_score(resume_text, jd_text, skills_list):
    """
    Returns a 0-100 score based on the percentage of JD skills
    that are also found in the resume. More intuitive than raw
    TF-IDF similarity since it's grounded in actual required skills.
    """
    keywords = get_missing_keywords(resume_text, jd_text, skills_list)
    jd_skill_count = len(keywords["matched"]) + len(keywords["missing"])

    if jd_skill_count == 0:
        return 0.0

    score = (len(keywords["matched"]) / jd_skill_count) * 100
    return round(score, 2)


if __name__ == "__main__":
    # Quick manual test
    sample_resume = "Experienced in Python, SQL, and REST API development."
    sample_jd = "Looking for a candidate skilled in Python, Docker, AWS, and REST API design."
    sample_skills = ["Python", "SQL", "Docker",
                     "AWS", "REST API", "Kubernetes"]

    print("Match score:", get_match_score(sample_resume, sample_jd))
    print("Keyword breakdown:", get_missing_keywords(
        sample_resume, sample_jd, sample_skills))
