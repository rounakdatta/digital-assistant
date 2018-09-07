run:
	sudo service mongod start
	python3 app.py

data:
	python3 initDb.py