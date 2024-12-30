from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self):
        """Perform validation and return the result."""
        pass
