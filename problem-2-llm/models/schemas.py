from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class TestCase(BaseModel):
    id: int
    input: str
    system_prompt: str
    expected_output: Optional[str] = None
    criteria: Optional[List[str]] = None


class CriterionScore(BaseModel):
    name: str

    score_a: float = Field(..., ge=0, le=10)
    score_b: float = Field(..., ge=0, le=10)

    winner: Literal["A", "B", "Tie"]

    rationale: str


class JudgeVerdict(BaseModel):
    winner: Literal["A", "B", "Tie"]

    overall_score_a: float = Field(..., ge=0, le=10)
    overall_score_b: float = Field(..., ge=0, le=10)

    criteria: list[CriterionScore]

    overall_rationale: str

class JudgeCall(BaseModel):
    prompt: str
    raw_response: str

    judge_model: str

    timestamp: datetime = Field(default_factory=datetime.now)

class EvaluationResult(BaseModel):
    test_case: TestCase

    answer_a: str
    answer_b: str

    verdict: JudgeVerdict

    judge_call: JudgeCall

class PositionBiasResult(BaseModel):
    original_winner: str
    reversed_winner: str

    consistent: bool

    flip_rate: float

class PositionBiasReport(BaseModel):
    total_cases: int

    consistent_cases: int

    flipped_cases: int

    flip_rate: float

    results: list[PositionBiasResult]


class VerbosityBiasResult(BaseModel):
    winner: str

    answer_a_length: int
    answer_b_length: int

    longer_answer: str

    preferred_longer_answer: bool

    length_difference: int
    length_ratio: float


class VerbosityBiasReport(BaseModel):
    total_cases: int

    longer_answer_wins: int

    verbosity_bias_rate: float

    results: list[VerbosityBiasResult]


class SelfEnhancementBiasResult(BaseModel):
    generator_model: str

    judge_model: str

    generator_family: str

    judge_family: str

    same_family: bool

    risk: str


class SelfEnhancementBiasReport(BaseModel):
    total_cases: int

    same_family_cases: int

    risk: str

    results: list[SelfEnhancementBiasResult]


class SycophancyBiasResult(BaseModel):
    winner: str

    confident_wrong_answer: str

    fooled: bool


class SycophancyBiasReport(BaseModel):
    total_cases: int

    fooled_cases: int

    sycophancy_rate: float

    results: list[SycophancyBiasResult]


class ScoreClusteringResult(BaseModel):
    mean: float

    median: float

    minimum: float

    maximum: float

    variance: float

    standard_deviation: float

    clustered: bool


class ScoreClusteringReport(BaseModel):
    total_cases: int

    result: ScoreClusteringResult


class JudgeValidationResult(BaseModel):
    winners: list[str]

    consistent_runs: int

    total_runs: int

    consistency_rate: float

    stable: bool


class JudgeValidationReport(BaseModel):
    total_cases: int

    average_consistency: float

    stable_cases: int

    results: list[JudgeValidationResult]