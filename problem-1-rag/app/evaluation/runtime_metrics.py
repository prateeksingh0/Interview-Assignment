class RuntimeMetrics:

    @staticmethod
    def average_similarity(chunks):

        return sum(
            chunk.distance
            for chunk in chunks
        ) / len(chunks)

    @staticmethod
    def highest_similarity(chunks):

        return max(
            chunk.distance
            for chunk in chunks
        )

    @staticmethod
    def lowest_similarity(chunks):

        return min(
            chunk.distance
            for chunk in chunks
        )

    @staticmethod
    def context_length(context):

        return len(context)

    @staticmethod
    def answer_length(answer):

        return len(answer)