if [[ "$OSTYPE" == "darwin"* ]]; then
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    python3 setup.py
    python3 manage.py runserver
else
    py -m venv venv
    source venv/Scripts/activate
    py -m pip install -r requirements.txt
    py setup.py
    py manage.py runserver
fi