from context_objects import SEPARATOR
from os import listdir
from os.path import isfile

# Цветовая палитра сайта
COLORS = {
    'GREEN': '#befb61', #'#00ff43'
    'LIGHT_BLUE': '#60a3f8',
    'ABRICOT_DARK': '#ee754a',  #'#f17a54'
    'ABRICOT_LIGHT': '#ee8f6d' #'#ffa573'
} 

def init():
    srcdir = 'core_app' + SEPARATOR + 'static_templates'
    dstdir = 'core_app' + SEPARATOR + 'static'

    def render(filename):
        with open(srcdir + SEPARATOR + filename, mode='r') as srcfile:
            with open(dstdir + SEPARATOR + filename, mode='w') as dstfile:
                for line in srcfile:
                    for key, value in COLORS.items():
                        line = line.replace('{% ' + key + ' %}', value)
                    dstfile.write(line)
    ld = listdir(srcdir)
    for file in ld:
        if isfile(srcdir + SEPARATOR + file):
            render(file)
