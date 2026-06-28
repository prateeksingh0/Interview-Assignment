from typing import List
import math


class RetrievalMetrics:

    @staticmethod
    def recall_at_k(

        expected: List[int],

        retrieved: List[int],

    ) -> float:

        if not expected:

            return 0.0

        hits = len(

            set(expected)

            &

            set(retrieved)

        )

        return hits / len(expected)
    

    @staticmethod
    def precision_at_k(

        expected,

        retrieved,

    ):

        if not retrieved:

            return 0.0

        hits = len(

            set(expected)

            &

            set(retrieved)

        )

        return hits / len(retrieved)
    
    @staticmethod
    def mean_reciprocal_rank(
        expected: List[int],
        retrieved: List[int],
    ) -> float:

        for rank, chunk in enumerate(retrieved, start=1):

            if chunk in expected:

                return 1 / rank

        return 0.0
    

    @staticmethod
    def ndcg(
        expected: list[int],
        retrieved: list[int],
    ) -> float:

        if not expected or not retrieved:
            return 0.0

        dcg = 0.0

        for rank, chunk in enumerate(retrieved, start=1):

            if chunk in expected:

                dcg += 1 / math.log2(rank + 1)

        ideal_hits = min(
            len(expected),
            len(retrieved),
        )

        idcg = sum(
            1 / math.log2(rank + 1)
            for rank in range(
                1,
                ideal_hits + 1,
            )
        )

        if idcg == 0:
            return 0.0

        return dcg / idcg