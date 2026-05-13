from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def send(self, payload: dict) -> dict:
        pass