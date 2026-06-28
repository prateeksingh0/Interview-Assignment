from abc import ABC, abstractmethod


class BiasDetector(ABC):
    """Base class for all bias detectors."""

    @abstractmethod
    def run(self):
        """Run the bias experiment."""
        pass