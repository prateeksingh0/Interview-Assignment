from app.evaluation.retrieval_metrics import RetrievalMetrics


def test_recall():

    score = RetrievalMetrics.recall_at_k(

        [5, 6],

        [5, 6, 4],

    )

    assert score == 1.0


def test_precision():

    score = RetrievalMetrics.precision_at_k(

        [5, 6],

        [5, 6, 4],

    )

    assert score == 2 / 3


def test_mrr_first():

    score = RetrievalMetrics.mean_reciprocal_rank(

        [5, 6],

        [5, 3, 2],

    )

    assert score == 1.0


def test_mrr_second():

    score = RetrievalMetrics.mean_reciprocal_rank(

        [5, 6],

        [3, 5, 2],

    )

    assert score == 0.5


def test_mrr_none():

    score = RetrievalMetrics.mean_reciprocal_rank(

        [5, 6],

        [1, 2, 3],

    )

    assert score == 0.0

def test_ndcg_perfect():

    score = RetrievalMetrics.ndcg(
        [5, 6],
        [5, 6],
    )

    assert score == 1.0


def test_ndcg_partial():

    score = RetrievalMetrics.ndcg(
        [5, 6],
        [3, 5],
    )

    assert 0 < score < 1


def test_ndcg_none():

    score = RetrievalMetrics.ndcg(
        [5, 6],
        [1, 2],
    )

    assert score == 0.0