from context_objects import SEPARATOR, HASH_FUNCTION
from os import listdir
from os.path import isfile

# Цветовая палитра сайта
COLORS = {
    'GREEN': '#befb61', #'#00ff43'
    'LIGHT_BLUE': '#60a3f8',
    'ABRICOT_DARK': '#ee754a',  #'#f17a54'
    'ABRICOT_LIGHT': '#ee8f6d', #'#ffa573'
    'GRAY': '#000a19'
} 


def render_static_templates(srcdir, dstdir):
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


def assure_authtxt(path):
    if not isfile(path):
        with open(path, mode='w') as file: pass
        print('\n')
        print('|\t Внимание!')
        print('|\t По адресу ' + path + ' не обнаружен файл данных авторизации пользователей')
        print('|\t Файл ' + path + ' был создан с нуля.')
        print('|\t Для работы сайта необходимо завести ADMIN пользователя и указать его данные в вышеуказанном файле.')
        print('|\t Пожалуйста, введите пароль, который будет использоваться для входа в аккаунт ADMIN пользователя:')
        #password = HASH_FUNCTION(input('|\t >>'))
        password = input('|\t >>')
        with open(path, mode='w') as file:
            file.write('ADMIN@ADMIN.ADMIN' + '\\' + str(password))
        print('|\t Спасибо! Пароль был внесён в файл данных авторизации пользователей ' + path)
        print('|\t Запуск сайта возобновлён')
        print('\n')
    else:
        print('\n')
        print('|\t Запуск сайта с базой пользователей ' + path)
        print('\n')

#def register_authtxt(path):
#    from django.contrib.auth.models import User
#    with open(path, mode='r') as file:
#        for line in file:
#            email, hashed_password = line.split('\\')
#            User.objects.create(email=email,
#                                password=int(hashed_password))

def init():
    render_static_templates('core_app' + SEPARATOR + 'static_templates', 
                            'core_app' + SEPARATOR + 'static')
    assure_authtxt('data' + SEPARATOR + 'userdata' + SEPARATOR + 'auth.txt')



if __name__ == '__main__':
    init()

#def post_run_setup():
#    register_authtxt('data' + SEPARATOR + 'userdata' + SEPARATOR + 'auth.txt')