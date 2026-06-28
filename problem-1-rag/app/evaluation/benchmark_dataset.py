from dataclasses import dataclass
from typing import List


@dataclass
class EvaluationSample:

    question: str

    expected_chunk_numbers: List[int]

    expected_answer: str


EVALUATION_DATASET = [

    EvaluationSample(

        question="What projects has the candidate built?",

        expected_chunk_numbers=[
            5,
            6,
        ],

        expected_answer="""
AI Resume Analyzer & Job Match Platform
AI Interview Preparation Platform
AI-Powered OWASP Top 10 Vulnerability Scanner
""",
    ),

    EvaluationSample(

        question="What technologies are listed in the candidate's skills?",

        expected_chunk_numbers=[
            8,
        ],

        expected_answer="""
Node.js
React
Django
FastAPI
PostgreSQL
Docker
Git
PyTorch
Scikit-learn
""",
    ),

    EvaluationSample(

        question="Where did the candidate complete their internship?",

        expected_chunk_numbers=[
            3,
        ],

        expected_answer="""
Uplyift
Delhi
""",
    ),

]