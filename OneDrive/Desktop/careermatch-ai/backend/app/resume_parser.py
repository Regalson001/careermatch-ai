# resume_parser.py

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader
from fastapi import HTTPException, UploadFile


MAX_BYTES = 5 * 1024 * 1024


async def extract_resume(file: UploadFile) -> tuple[str, str]:

    filename = file.filename or "resume"

    suffix = Path(filename).suffix.lower()

    if suffix not in {".pdf", ".txt"}:
        raise HTTPException(
            status_code=415,
            detail="Upload a PDF or TXT resume."
        )

    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty."
        )

    if len(data) > MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Resume exceeds the 5 MB upload limit."
        )

    try:

        if suffix == ".pdf":

            reader = PdfReader(BytesIO(data))

            if reader.is_encrypted:
                raise HTTPException(
                    status_code=400,
                    detail="Password-protected PDFs are not supported."
                )

            text = "\n".join(
                page.extract_text() or ""
                for page in reader.pages
            )

        else:

            text = data.decode("utf-8-sig")

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Could not read this file. Check that it is a valid PDF or TXT file."
        )

    text = text.strip()

    if len(text) < 30:

        raise HTTPException(
            status_code=422,
            detail="Not enough readable text was found. Scanned PDFs require OCR."
        )

    return text[:100000], filename
