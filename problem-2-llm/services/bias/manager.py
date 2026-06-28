from services.bias.position import PositionBiasDetector
from services.bias.verbosity import VerbosityBiasDetector
from services.bias.self_enhancement import SelfEnhancementBiasDetector
from services.bias.sycophancy import SycophancyBiasDetector
from services.bias.clustering import ScoreClusteringDetector


class BiasManager:

    def __init__(self):
        self.position = PositionBiasDetector()
        self.verbosity = VerbosityBiasDetector()
        self.self_enhancement = SelfEnhancementBiasDetector()
        self.sycophancy = SycophancyBiasDetector()
        self.clustering = ScoreClusteringDetector()

    def run(self, evaluations):

        return {
            "position_bias": self.position.evaluate_suite(evaluations).model_dump(),

            "verbosity_bias": self.verbosity.evaluate_suite(evaluations).model_dump(),

            "self_enhancement_bias": self.self_enhancement.evaluate_suite(evaluations).model_dump(),

            "sycophancy_bias": self.sycophancy.evaluate_suite(evaluations).model_dump(),

            "score_clustering": self.clustering.evaluate_suite(evaluations).model_dump(),
        }