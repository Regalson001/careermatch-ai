# test_matcher.py

from app.matcher import analyze, extract_skills


def test_extract_skills():

    found = extract_skills(
        "We need Python, FastAPI, Docker and PostgreSQL experience."
    )

    assert "Python" in found

    assert "FastAPI" in found

    assert "Docker" in found

    assert "PostgreSQL" in found


def test_match_score_and_gaps():

    resume = (
        "Python developer with FastAPI and Docker experience. "
        "Built REST APIs."
    )

    job = (
        "Required: Python and FastAPI. "
        "Must have AWS and Docker. "
        "Experience with PostgreSQL."
    )

    result = analyze(
        resume,
        job,
        "resume.txt"
    )

    assert result.match_score > 0

    assert "Python" in result.matched_skills

    assert "AWS" in result.missing_skills

    assert 0 <= result.match_score <= 100


def test_no_detected_job_skills():

    result = analyze(

        "My resume text is long enough to be processed.",

        "A role requiring excellent communication and leadership experience.",

        "cv.txt"

    )

    assert result.match_score == 0
