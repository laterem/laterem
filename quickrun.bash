if [[ "$OSTYPE" == "win32" ]]; then
    py -m venv venv
    source venv/Scripts/activate
    py -m pip install -r requirements.txt
    py manage.py runserver
else
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    python3 manage.py runserver
fi