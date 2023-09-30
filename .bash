python -m pip install -r requirements.txt
flask db init 
flask db migrate
flask db upgrade
python server.py