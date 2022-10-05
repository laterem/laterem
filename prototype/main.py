from tasks import *

t1 = NumberComparison()
t1.generate()
t2 = AnswerMatching()
t2.configure(['китай',])
t3 = BasicProblemSolving()
t3.generate()
t4 = NumberNotationConvertation()
t4.generate()

print(t1.render())
print(t2.render())
print(t3.render())
print(t4.render())