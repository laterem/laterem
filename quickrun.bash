source bash/setup.bash
if [[ "$OSTYPE" == "darwin"* ]]; then
    python3 manage.py runserver
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    python3 manage.py runserver
else
    py manage.py runserver
fi