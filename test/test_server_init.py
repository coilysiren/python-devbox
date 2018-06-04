import subprocess
import requests
import time
import os
import signal

PORT = 5005
SERVER_START_TIMEOUT = 10


def test_server_init():
    _start_server_process()
    response = _await_server_response()
    assert response.status_code == 200
    assert response.content.decode('utf-8') == 'pong'
    _kill_server_processes()


def _start_server_process():
    try:
        requests.get(f'http://localhost:{PORT}/ping')
        _kill_server_processes()
    except requests.exceptions.ConnectionError:
        return subprocess.Popen(['heroku', 'local',  '-p', f'{PORT}'])


def _kill_server_processes():
    pids = subprocess.run(
        "ps | grep 'gunicorn src' | sed 's/ .*//'", shell=True, stdout=subprocess.PIPE)
    for pid in filter(None, pids.stdout.decode('utf-8').split('\n')):
        try:
            os.kill(int(pid), signal.SIGTERM)
        except ProcessLookupError:
            pass


def _await_server_response():
    timeout = time.time() + SERVER_START_TIMEOUT
    while time.time() < timeout:
        try:
            return requests.get(f'http://localhost:{PORT}/ping')
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    else:
        raise Exception(
            f'Could not connect to server within {SERVER_START_TIMEOUT} seconds')
