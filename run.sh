export $(cat ./.env | xargs)
gunicorn main:app -b 0.0.0.0:5000 --reload