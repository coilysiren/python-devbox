dev:
	npx concurrently \
		-k -n angular,flask \
		-c red,green \
			"make __dev-angular" \
			"make __dev-flask"

__dev-angular:
	npx ng serve --port 4200

__dev-flask:
	FLASK_APP=src/python/server flask run --port 3000
