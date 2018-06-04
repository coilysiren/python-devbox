watch:
	pytest-watch \
		--onpass "osascript -e 'display notification \"All tests passed!\" with title \"Passed\" ' " \
    --onfail "osascript -e 'display notification \"Tests failed XXX\" with title \"Failed\" ' "
