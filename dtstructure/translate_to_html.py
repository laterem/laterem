from dtstructure.fileutils import rdir_to_tree

def update_global_dict(container: dict, value):
    container.clear()
    for k, v in value.items():
        container[k] = v

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
                element = elel[elel.find('\\', elel.find('\\') + 1) + 1:elel.rfind('.')]
                output.insert(pointer, '<li><a href="' + 'http://localhost:8000/works/' + element.replace('\\', '.') + '">' + element[element.rfind('\\') + 1:] + '</a></li>')
                pointer += 1
            pointer += 1
    return ''.join(output)

def translate_to_html():
    work_dir = dict()
    update_global_dict(work_dir, rdir_to_tree('dtm\\works'))
    print('Works directory snapshot:', work_dir)

    with open('core_app/templates/menu.html', 'w', encoding='UTF-8') as f:
        f.write(make_html(work_dir))
