server: server.py
	FLASK_APP=server.py flask run --port=80

run: main.py
	python main.py