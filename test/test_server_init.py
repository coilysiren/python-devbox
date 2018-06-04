import subprocess
import requests
import time

PORT = 5001
SERVER_START_TIME = 3
SERVER_TIMEOUT_TIME = 60


def test_server_init(capsys):
    proc = subprocess.Popen(f'heroku local -p {PORT}', shell=True)
    response = _await_server_response(capsys)
    assert response.status_code == 200
    assert response.content.decode('utf-8') == 'pong'
    proc.kill()


def _await_server_response(capsys):
    timeout = time.time() + SERVER_START_TIME + SERVER_TIMEOUT_TIME
    while time.time() < timeout:
        try:
            response = requests.get(f'http://localhost:{PORT}/ping')
            break
        except requests.exceptions.ConnectionError:
            with capsys.disabled():
                print(f'\n{timeout - time.time()} until timeout\n')
            time.sleep(1)
    else:
        raise f'Could not connect to server within {SERVER_TIMEOUT_TIME} seconds'
    return response
