from abc import ABCMeta, abstractmethod

class Task():
    __metaclass__ = ABCMeta

    @abstractmethod
    def render(self) -> str:
        ...

    @abstractmethod
    def configure(self, *args) -> None:
        ...

    @abstractmethod
    def generate(self) -> None:
        ...
    
    @abstractmethod
    def test(self, *args) -> int:
        ...