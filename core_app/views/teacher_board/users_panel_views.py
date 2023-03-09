from core_app.views.views_commons import *

@permission_required("can_manage_users")
def users_panel(request):
    general_POST_handling(request)
    if request.method == "POST":
        if "newuser" in request.POST:
            form = NewUser(request.POST)
            if form.is_valid():
                test = LateremUser.objects.filter(
                    email=form.cleaned_data["email"]
                )
                if test:
                    # Пользователь с такой почтой уже есть,
                    # надо(!!!!!!) как-то оповестить
                    pass
                else:
                    User.create(email=form.cleaned_data["email"],
                                password=form.cleaned_data["password"],
                                first_name=form.cleaned_data["first_name"],
                                last_name=form.cleaned_data["second_name"])
        elif "submit_import_users" in request.POST:
            # Импорт из файла
            import_file = request.FILES.get("import_file")
            import_file = read_text_file(import_file)
            if import_file:
                try:
                    header = True 
                    for line in import_file:
                        line = line.decode().strip()
                        if header:
                            keys = line.split(';')
                            header = False
                            # print(keys)
                            if set(keys) != {'email', 'password', 'first_name', 'last_name'}:
                                # Таблица неполная, оповестить пользователя
                                break
                            continue
                        args = line.split(';')
                        if len(args) != 4:
                            # Таблица некорректная, оповестить пользователя
                            break
                        # Добавить проверку корректности данных
                        User.create(**dict(zip(keys, args)))
                except UnicodeDecodeError:
                    pass # Отправлен странный файл, оповестить пользователя
        else:
            flag = False
            for signal in request.POST:
                if signal.startswith("delete:"):
                    email = signal[len("delete:"):]
                    try:
                        user = LateremUser.objects.get(email=email)
                    except LateremUser.DoesNotExist:
                        continue
                    user.delete()
                    flag = True
                    break
                elif signal.startswith("edit:"):
                    email = signal.lstrip("edit:")
                    try:
                        user = LateremUser.objects.get(email=email)
                    except LateremUser.DoesNotExist:
                        continue
                    email = request.POST.get("user_email")
                    first_name = request.POST.get("user_name")
                    last_name = request.POST.get("user_lastname")
                    print(email, first_name, last_name)
                    print(request.POST)

                    if email and first_name and last_name:
                        user.email = email
                        user.first_name = first_name
                        user.last_name = last_name

                    # if request.POST.get('user_password'):
                    #   user.password = request.POST.get('user_password')
                        user.save()
    form = NewUser()
    return render(
        request,
        "teacher_panel/user_panel.html",
        render_args(
            meta_all_users_available=True,
            request=request,
            additional={"newuserform": form,
                        "title": "Управление учениками"},
        ),
    )
