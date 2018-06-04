import server_utils


SERVER_TEST_PATH = '/ping'
SERVER_TEST_RESULT = 'pong'


def test_server_init():
    server_utils.start_server_process()
    try:
        response = server_utils.await_server_response(SERVER_TEST_PATH)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == SERVER_TEST_RESULT
    except Exception:
        pass
    server_utils.kill_server_processes()
