if [[ "$OSTYPE" == "darwin"* ]]; then
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    python3 manage.py clearsessions
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver
else
    py -m venv venv
    source venv/Scripts/activate
    py -m pip install -r requirements.txt
    py manage.py clearsessions
    py manage.py makemigrations
    py manage.py migrate
    py manage.py runserver
fi