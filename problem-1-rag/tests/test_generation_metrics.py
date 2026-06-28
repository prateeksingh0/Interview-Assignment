from app.evaluation.generation_metrics import GenerationMetrics


def test_faithfulness():

    score = GenerationMetrics.faithfulness(

        "React Node Docker",

        "React Node Docker PostgreSQL",

    )

    assert score == 1.0


def test_answer_relevance():

    score = GenerationMetrics.answer_relevance(

        "What projects",

        "The projects are...",

    )

    assert score > 0


def test_context_precision():

    score = GenerationMetrics.context_precision(

        "React Node",

        "React Node PostgreSQL",

    )

    assert 0 < score < 1