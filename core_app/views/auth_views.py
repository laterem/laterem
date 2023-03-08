from core_app.views.views_commons import *
from django.contrib.auth import authenticate, login, logout


def logout_view(request):
    logout(request)
    return redirect("/")

def login_view(request):
    # <Костыль>
    DEBUG_assure_admin()
    # </Костыль>
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next"))
        else:
            return HttpResponse(
                "<h1>Такого аккаунта не существует! или данные некорректные</h1>"
            )
    else:
        form = LoginForm()
        return render(
            request, "login.html", render_args(additional={"title": "Вход в аккаунт", "form": form})
        )