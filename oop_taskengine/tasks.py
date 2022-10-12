from abc import ABCMeta, abstractmethod
from typing import List, Set
from random import randint, choice

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


class AnswerMatching(Task):
    def configure(self, correct_answers: List[str], description: str) -> None:
        self.correct_answers = correct_answers
        self.description = description
    
    def render(self) -> str:
        return self.description

    def generate(self) -> None:
        return NotImplemented
    
    def test(self, answer: str) -> int:
        return answer.strip() in self.correct_answers


class NumberNotationConvertation(Task):
    def configure(self, source: int, source_base: int, destination_base: int) -> None:
        self.source = source
        self.source_base = source_base
        self.destination_base = destination_base
    
    def render(self) -> str:
        from custommath import int2str
        return f"{int2str(self.source, self.source_base)} по основанию {self.source_base} = ___ по основанию {self.destination_base}"
    
    def test(self, answer: str) -> int:
        try:
            return int(answer, self.destination_base) == self.source
        except ValueError as e:
            return 0
    
    def generate(self, a:int=0, b:int=2**9, bases:Set[int]={2, 10, 16}) -> None:
        self.source = randint(a, b)
        tmp0 = len(bases)
        tmp1 = randint(0, tmp0-1)
        tmp2 = list(bases)
        self.source_base = tmp2[tmp1]
        del tmp2[tmp1]
        self.destination_base = choice(tmp2)


class NumberComparison(Task):
    def configure(self, a: int, a_base: int, b: int, b_base: int) -> None:
        self.a = a
        self.a_base = a_base
        self.b = b
        self.b_base = b_base
    
    def test(self, answer: str) -> int:
        answer = answer.strip()
        if answer == '>':
            return self.a > self.b
        elif answer == '=':
            return self.a == self.b
        elif answer == '<':
            return self.a < self.b
        return 0
    
    def render(self) -> str:
        from custommath import int2str
        return f"{int2str(self.a, self.a_base)} по основанию {self.a_base} ___ чем {int2str(self.b, self.b_base)} по основанию {self.b_base}"
    
    def generate(self, a:int=0, b:int=2**9, bases:Set[int]={2, 10, 16}) -> None:
        bases = list(bases)
        self.a = randint(a, b)
        self.b = randint(a, b)
        tmp0 = randint(0, len(bases) - 1)
        self.a_base = bases[tmp0]
        if self.a == self.b:
            del bases[tmp0]
        self.b_base = choice(bases)


class BasicProblemSolving(Task):
    Minus = object()
    Plus = object()
    def configure(self, a : int, b : int, op,
                  a_base : int, b_base : int, sol_base : int) -> None:
        self.a = a
        self.b = b
        self.op = op
        self.a_base = a_base
        self.b_base = b_base
        self.sol_base = sol_base
    
    def generate(self, a:int=0, b:int=2**9, bases:Set[int]={2, 10, 16}) -> None:
        self.a = randint(a, b)
        self.b = randint(a, b)
        self.op = choice((BasicProblemSolving.Minus, BasicProblemSolving.Plus))
        bases = list(bases)
        self.a_base = choice(bases)
        self.b_base = choice(bases)
        self.sol_base = choice(bases)
    
    def test(self, answer: str) -> int:
        try:
            answer = int(answer, self.sol_base)
        except ValueError as e:
            return 0
        if self.op == BasicProblemSolving.Minus:
            return answer == (self.a - self.b)
        elif self.op == BasicProblemSolving.Plus:
            return answer == (self.a + self.b)
    
    def render(self) -> str:
        from custommath import int2str
        return f"{int2str(self.a, self.a_base)} по основанию {self.a_base} {'+' if self.op == BasicProblemSolving.Plus else '-'} {int2str(self.b, self.b_base)} по основанию {self.b_base} = ___ по основанию {self.sol_base}"
