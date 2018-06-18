dev:
	pytest-watch

focus:
	pytest-watch -- -m focus

__dev-old:
	npx concurrently \
		-k -n angular,flask \
		-c red,green \
			"make __dev-angular" \
			"make __dev-flask"

__dev-angular:
	npx ng serve --port 4200

__dev-flask:
	FLASK_ENV=development FLASK_APP=src/python/server flask run --port 3000
