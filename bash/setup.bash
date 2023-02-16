if [[ "$OSTYPE" == "darwin"* ]]; then
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    python3 manage.py clearsessions
    python3 manage.py collectstatic --noinput
    python3 manage.py makemigrations
    python3 manage.py migrate
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    python3 manage.py clearsessions
    python3 manage.py collectstatic --noinput
    python3 manage.py makemigrations
    python3 manage.py migrate
else
    py -m venv venv
    source venv/Scripts/activate
    py -m pip install -r requirements.txt
    py manage.py clearsessions
    py manage.py collectstatic --noinput
    py manage.py makemigrations
    py manage.py migrate
fi