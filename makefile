dev:
	pytest-watch

focus:
	pytest-watch -- -m focus

run:
	FLASK_ENV=development FLASK_APP=src/python/server flask run --port 3000
