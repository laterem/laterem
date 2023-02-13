from dbapi.tasks import Verdicts
from context_objects import SEPARATOR, WORKS

def init_personal_tree(tree):
    ret = dict()
    for el in list(tree.keys()):
        if type(tree[el]) == type(dict()):
            # Ситуация на узле
            ret[el] = init_personal_tree(tree[el])
        else:
            # Ситуация последнего узла
            ret[el] = dict()
            for i in tree[el]:
                #  i - имя работы
                ret[el][i] = Verdicts.NO_ANSWER
    return ret

def set_work_verdict(answers):
    if answers[Verdicts.NO_ANSWER] == 0:
        if (answers[Verdicts.WRONG_ANSWER] == answers[Verdicts.PARTIALLY_SOLVED] == 0):
            return Verdicts.OK
    elif (answers[Verdicts.OK] > 0) or (answers[Verdicts.SENT] > 0) or (answers[Verdicts.PARTIALLY_SOLVED] > 0):
        return Verdicts.PARTIALLY_SOLVED
    else:
        return Verdicts.NO_ANSWER

def merge_tree(tree1, tree2, user):
    # tree1 - WORKDIR или его ветка; tree2 - Дерево ученика; ret - результат
    ret = dict()
    if type(tree1) != type(dict()):
        # Обработка листьев (работ)
        for k in tree1:
            # k - имя работы
            # answers - словарь. ключ - вердикт; значение - сколько задач с таким вердиктом в работе
            answers = {Verdicts.NO_ANSWER: 0,
                Verdicts.OK: 0,
                Verdicts.PARTIALLY_SOLVED: 0,
                Verdicts.SENT: 0,
                Verdicts.WRONG_ANSWER: 0
            }

            work_name_for_WORKS = k[11:k.rfind('.')].replace(SEPARATOR, '.')
            work_name_for_user = k[11:k.rfind('.')]

            for t in WORKS[work_name_for_WORKS][0]:
                if user.get_task_verdict(work_name_for_user, t):
                    answers[user.get_task_verdict(work_name_for_user, t)] += 1
                else:
                    answers[Verdicts.NO_ANSWER] += 1

            # Функция, определяющая вердикт работы от количества вердиктов по задачам
            ret[k] = set_work_verdict(answers)
    else:
        for k in list(tree1.keys()):
            if k in list(tree2.keys()):
                ret[k] = merge_tree(tree1[k], tree2[k], user)
            else:
                ret[k] = init_personal_tree(tree1)
    return ret

def set_work_verdict(answers):
    if answers[Verdicts.NO_ANSWER] == 0:
        if (answers[Verdicts.WRONG_ANSWER] == answers[Verdicts.PARTIALLY_SOLVED] == 0):
            return Verdicts.OK
    elif (answers[Verdicts.OK] > 0) or (answers[Verdicts.SENT] > 0) or (answers[Verdicts.PARTIALLY_SOLVED] > 0):
        return Verdicts.PARTIALLY_SOLVED
    else:
        return Verdicts.NO_ANSWER

def _submenu(inp, deep=0):
    if deep == 0:
        output = ['<ul id="myUL">', '</ul>']
    else:
        output = ['<ul class="nested">', '</ul>']
    pointer = 1
    for el in inp.keys():
        # print('§§§§§§')
        # print(deep)
        # print(inp[el])
        # print(list(inp[el].items())[0])
        # print()
        if type(list(inp[el].values())[0]) == type(dict()):
            output.insert(pointer, '<li><span class="caret">' + el + '</span>' + _submenu(inp[el], deep=deep + 1) + '</li>')
            pointer += 1
        else:
            output.insert(pointer, '<li><span class="caret">' + el + '</span><ul class="nested">')
            pointer += 1
            output.insert(pointer, '</ul></li>')
            for elel in inp[el].keys():
                element = elel[elel.find(SEPARATOR, elel.find(SEPARATOR) + 1) + 1:elel.rfind('.')]
                if inp[el][elel] == Verdicts.NO_ANSWER:
                    output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '" id="no-answer_work">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                else:
                    # Оперделение состояния задания
                    if inp[el][elel] == Verdicts.OK:
                        output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '" id="correct_work">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                    elif inp[el][elel] == Verdicts.WRONG_ANSWER:
                        output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '" id="wrong_work">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                    else:
                        output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace(SEPARATOR, '.') + '" id="unchecked_work">' + element[element.rfind(SEPARATOR) + 1:] + '</a></li>')
                pointer += 1
            pointer += 1
    return ''.join(output)


class NestingDictWrapper(dict):
    def __init__(self, source):
        self.dict = source
        self.wrapper = {}

    def __getitem__(self, key):
        # print('>>>', key, self.dict, self.wrapper, key in self.dict)

        if key not in self.dict:
            self.dict[key] = {}
            self.wrapper[key] = NestingDictWrapper(self.dict[key])
            return self.wrapper[key]
        elif key in self.wrapper:
            return self.wrapper[key]
        else:
            return self.dict[key]
    
    def __setitem__(self, key, value):
        self.dict[key] = value
        self.wrapper[key] = value

from os import listdir
from os.path import join
# Построение объекта вложенного словаря по директории (рекурсия, произвольная вложенность)
def rdir_to_tree(sourcepath, layers=-1):
    dirlist = listdir(sourcepath)
    if dirlist:
        if layers == 0 or (layers < 0 and dirlist[0].endswith('.json')): # Костыль, но учителю нужно постараться чтобы его заабузить
            return sorted([join(sourcepath, path) for path in dirlist if path.endswith('.json')])
        else:
            output = {}
            for key in dirlist:
                output[key] = rdir_to_tree(join(sourcepath, key), layers-1)
            return output
    else:
        return []

LateremCategoryCategory = None
Category = None
def tree(self, accesible_for=None):
    children = self.categories()
    ret = {}
    for child in children:
        if child.__dbmodel__ == LateremCategoryCategory:
            result = child.tree(accesible_for)
        else:
            result = child.works(accesible_for)
        if result:
            ret[child.name] = result
    return ret

@staticmethod
def global_tree(accesible_for=None):
    roots = Category.roots()
    ret = {}
    for child in roots:
        if child.__dbmodel__ == LateremCategoryCategory:
            result = child.tree(accesible_for)
        else:
            result = child.works(accesible_for)
        if result:
            ret[child.name] = result
    return ret