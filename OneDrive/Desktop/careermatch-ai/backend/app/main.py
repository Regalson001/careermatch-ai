# main.py

import os

from dotenv import load_dotenv

from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    UploadFile
)

from fastapi.middleware.cors import CORSMiddleware

from .resume_parser import extract_resume
from .matcher import analyze
from .rewriter import improve_bullets


load_dotenv()


app = FastAPI(

    title="CareerMatch AI API",

    version="1.0.0",

    description=(
        "Stateless resume and job description "
        "matching API"
    )

)


origin_setting = os.getenv(
    "FRONTEND_ORIGIN",
    "*"
)

origins = (
    ["*"]
    if origin_setting == "*"
    else [
        origin.strip()
        for origin in origin_setting.split(",")
    ]
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=False,

    allow_methods=["GET", "POST"],

    allow_headers=["*"]

)


@app.get("/api/health")
def health():

    return {

        "status": "ok",

        "service": "careermatch-ai"

    }


@app.post("/api/analyze")
async def analyze_resume(

    resume: UploadFile = File(...),

    job_description: str = Form(...)

):

    job_description = job_description.strip()

    if len(job_description) < 50:

        raise HTTPException(

            status_code=422,

            detail=(
                "Please provide a job description "
                "of at least 50 characters."
            )

        )

    if len(job_description) > 30000:

        raise HTTPException(

            status_code=413,

            detail="Job description is too long."

        )

    resume_text, filename = await extract_resume(
        resume
    )

    result = analyze(

        resume_text,

        job_description,

        filename

    )

    result.bullet_suggestions = await improve_bullets(

        resume_text,

        job_description,

        result.bullet_suggestions

    )

    return result
