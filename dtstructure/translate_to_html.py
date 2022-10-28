from context_objects import LEFT_MENU_CODE, WORK_DIR

def make_html(inp):
    output = ['<ul>', '</ul>']
    pointer = 1
    for el in inp.keys():
        if type(inp[el]) == type(dict()):
            output.insert(pointer, '<li>' + el + make_html(inp[el]) + '</li>')
            pointer += 1
        else:
            output.insert(pointer, '<li>' + el + '<ul>')
            pointer += 1
            output.insert(pointer, '</ul></li>')
            for elel in inp[el]:
                element = elel[elel.find('/', elel.find('/') + 1) + 1:elel.rfind('.')]
                output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace('/', '.') + '">' + element[element.rfind('/') + 1:] + '</a></li>')
                pointer += 1
            pointer += 1
    return ''.join(output)

def translate_to_html():
    LEFT_MENU_CODE.value = make_html(WORK_DIR)
