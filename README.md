AI-powered resume and job description matching platform.

CareerMatch AI analyzes resumes against job descriptions,
extracts required skills, identifies missing qualifications,
calculates a transparent alignment score, and generates
tailored resume bullet-point suggestions.

## Features

- PDF and TXT resume uploads
- Job description analysis
- Resume text extraction
- Technical skill extraction
- Matched skill identification
- Missing skill identification
- Weighted match scoring
- Resume optimization suggestions
- Optional LLM integration
- Structured API responses
- Stateless request processing

## Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- Pydantic
- pypdf

### AI
- Natural Language Processing
- Keyword matching
- OpenAI API integration

### Testing
- pytest

### Deployment
- Docker
- GitHub

## Project Structure

careermatch-ai/

├── backend/

│   ├── app/

│   │   ├── main.py

│   │   ├── schemas.py

│   │   ├── matcher.py

│   │   ├── resume_parser.py

│   │   └── rewriter.py

│   ├── tests/

│   │   └── test_matcher.py

│   ├── requirements.txt

│   └── Dockerfile

├── frontend/

│   ├── index.html

│   ├── styles.css

│   └── app.js

├── README.md

├── .gitignore

└── docker-compose.yml

## Installation

### Backend

Create a virtual environment:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Start the API:

uvicorn app.main:app --reload --port 8000

### Frontend

Open frontend/index.html using
the VS Code Live Server extension.

## API Documentation

http://localhost:8000/docs

## API Endpoints

GET /api/health

POST /api/analyze

## How It Works

1. Upload your resume.
2. Paste a job description.
3. Extract resume text.
4. Identify required job skills.
5. Compare resume skills.
6. Calculate the alignment score.
7. Identify potential skill gaps.
8. Generate improvement suggestions.

## Important Notes

The match score is a keyword-based alignment
indicator, not a hiring prediction.

Review all AI-generated suggestions before
using them in your resume.

## Author

Stephen Oyugi

GitHub:
https://github.com/Regalson001
