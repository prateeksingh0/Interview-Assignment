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
        expected_chunk_numbers=[5, 6],
        expected_answer="""
The candidate has built three major projects: AI Resume Analyzer & Job Match Platform, AI Interview Preparation Platform, and AI-Powered OWASP Top 10 Vulnerability Scanner.
""",
    ),

    EvaluationSample(
        question="Where did the candidate complete their internship?",
        expected_chunk_numbers=[3],
        expected_answer="""
The candidate completed their internship at Uplyift in Delhi.
""",
    ),

    EvaluationSample(
        question="What degree is the candidate pursuing?",
        expected_chunk_numbers=[2],
        expected_answer="""
B.Tech – Computer Science & Engineering (AI & ML)
""",
    ),

    EvaluationSample(
        question="What is the candidate's CGPA?",
        expected_chunk_numbers=[2, 3],
        expected_answer="""
The candidate's CGPA is 8.43.
""",
    ),

    EvaluationSample(
        question="What frontend technologies are listed?",
        expected_chunk_numbers=[8],
        expected_answer="""
The frontend technologies include React.js, HTML, and CSS.
""",
    ),

    EvaluationSample(
        question="What backend technologies are listed?",
        expected_chunk_numbers=[8],
        expected_answer="""
The backend technologies include Node.js, Express.js, Django, FastAPI, REST APIs, Prisma ORM, JWT Authentication, and Ollama for local LLM integration.
""",
    ),

    EvaluationSample(
        question="Which databases are mentioned?",
        expected_chunk_numbers=[8],
        expected_answer="""
The databases mentioned are PostgreSQL and MySQL.
""",
    ),

    EvaluationSample(
        question="Which DevOps tools are mentioned?",
        expected_chunk_numbers=[8],
        expected_answer="""
Docker
Git
""",
    ),

    EvaluationSample(
        question="Which AI and machine learning technologies are mentioned?",
        expected_chunk_numbers=[8],
        expected_answer="""
LLMs
RAG Pipelines
PPO / RL
PyTorch
Scikit-learn
Pandas
NumPy
""",
    ),

    EvaluationSample(
        question="Which security tools are listed?",
        expected_chunk_numbers=[8],
        expected_answer="""
Burp Suite
Metasploit
Nmap
OWASP ZAP
Scapy
Kali Linux
""",
    ),

    EvaluationSample(
        question="Summarize the candidate's internship experience.",
        expected_chunk_numbers=[2,3,4],
        expected_answer="""
Worked as a Full-Stack Developer Intern at Uplyift building Shopify CMS, GenAI pipelines, React UI, FastAPI backend, and Shopify integrations.
""",
    ),

    EvaluationSample(
        question="Summarize the AI Resume Analyzer project.",
        expected_chunk_numbers=[4,5],
        expected_answer="""
Built a full-stack AI Resume Analyzer with React, Node.js, PostgreSQL, Prisma, JWT, Ollama, resume parsing and ATS scoring.
""",
    ),

    EvaluationSample(
        question="Does the candidate have experience with local LLMs?",
        expected_chunk_numbers=[5,6,8],
        expected_answer="""
Yes. The projects integrate Ollama for local LLM inference.
""",
    ),

    EvaluationSample(
        question="Tell me if this resume is suitable for a React.js developer role.",
        expected_chunk_numbers=[2,3,4,5,8],
        expected_answer="""
Based on the available evidence, the candidate appears well suited for a React.js Developer role due to experience with React.js in professional work, multiple full-stack projects, and listed frontend skills.
""",
    ),

    EvaluationSample(
        question="What cloud platforms has the candidate worked with?",
        expected_chunk_numbers=[],
        expected_answer="""
I don't have enough information from the provided documents.
""",
    ),
]