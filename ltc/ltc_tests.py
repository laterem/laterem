from ltc_builtins import *
from ltc_compiler import *
from ltc_core import *

class TestFailed(Exception):
    pass

def test(name):
    def wrapper(function):
        def new():
            print(f'[ ] <Test {name}>' + '\t' + 'Starting...')
            try:
                function()
            except TestFailed as e:
                print(f'[!] <Test {name}>' + '\t' + 'Test failed! ' + str(e))
            except Exception as e:
                print(f'[!] <Test {name}>' + '\t' + 'Runtime error occured: ' + type(e).__name__ + ': ' + str(e))
            else:
                print(f'[ ] <Test {name}>' + '\t' + 'Test passed successfully!')
        return new
    return wrapper

@test('1 Basic')
def test1():
    string = '''
a = 5
input?Equal(a)'''

    ltcc = LTCCompiler()

    ltc = ltcc.compile(string)
    ltc.execute()
    
    if not ltc.check({'input': 5}):
        raise TestFailed('5')
    
    if not ltc.check({'input': '5'}):
        raise TestFailed("'5'")
    
    if ltc.check({'input': 10}):
        raise TestFailed("10")
    
    if ltc.check({'input': "chunky"}):
        raise TestFailed("chunky")

@test('2 Functions')
def test2():
    string = '''
a = Rand10(-20, 20)
b = Rand10(-20, 20)
input?Equal(Sum(a, b))'''

    ltcc = LTCCompiler()

    ltc = ltcc.compile(string)
    ltc.execute()
    
    a, b = ltc.field_table['a'], ltc.field_table['b']

    if not ltc.check({'input': a + b}):
        raise TestFailed()

@test('3 Shortcuts')
def test3():
    string = '''
a = Rand10(-20, 20)
b = Rand10(-20, 20)
input?Sum(a, b)'''

    ltcc = LTCCompiler()

    ltc = ltcc.compile(string)
    ltc.execute()
    
    a, b = ltc.field_table['a'], ltc.field_table['b']

    if not ltc.check({'input': a + b}):
        raise TestFailed()

@test('4 Lists')
def test4():
    string = '''
a = [0, 1, 2, 3, 4, "[I'm no list, capiche?]", Reverse(['But', 'I', 'am!'])]
input?Reverse(a)'''

    ltcc = LTCCompiler()

    ltc = ltcc.compile(string)
    ltc.execute()
    
    if not ltc.field_table['a'] == [0, 1, 2, 3, 4, "[I'm no list, capiche?]", reversed(['But', 'I', 'am!'])]:
        raise TestFailed('list is ' + str(ltc.field_table['a']))

    input = reversed([0, 1, 2, 3, 4, "[I'm no list, capiche?]", reversed(['But', 'I', 'am!'])])

    if not ltc.check({'input': input}):
        raise TestFailed()

@test('5 Forbidders 1')
def test5():
    string = '''
a = Rand10(0, 10)
\\a?Equal(5)'''

    ltcc = LTCCompiler()
    
    for i in range(10000):
        ltc = ltcc.compile(string)
        ltc.execute()
        if ltc.field_table['a'] == 5:
            raise TestFailed('a == 5')
    

@test('6 Forbidders 2')
def test6():
    ltcc = LTCCompiler()
    
    string = '''
a = 21
b = Sum(a, a)

\\b?NotEqual(42)'''

    ltcc = LTCCompiler()

    ltc = ltcc.compile(string)
    ltc.execute()
    
    for i in range(10000):
        if ltc.field_table['b'] != '42':
            raise TestFailed('b != 42')

@test('7 Tricky typing')
def test7():
    ltcc = LTCCompiler()
    string = '''
a = 7
b = 3.5
c = Multiply(b, 2)
d = Sum(b, b)
e = Sum(Sum(b, b), Sum(a, a))

f = Multiply(c, 11)
g = GenerateLine(2, a)

inputa?Equal(c)
inputc?Equal(d)
inpute?Equal(21)
inputg?Equal(f)
'''
    ltc = ltcc.compile(string)
    ltc.execute()
    ft = ltc.field_table
    if not ltc.check({'inputa': ft['a'],
                      'inputc': ft['c'],
                      'inpute': ft['e'],
                      'inputg': ft['g'],
                      }):
        raise TestFailed(str(ft) + ' (must be )')


if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()

