dev:
	pytest-watch

focus:
	pytest-watch -- -m focus

run:
	FLASK_ENV=development FLASK_APP=src/python/server flask run --port 3000

reset-db:
	python -c 'from src import db, app; db.drop_all(app=app)'
	python -c 'from src import db, app; db.create_all(app=app)'
