def main():
    return 20


def test_main():
    assert main() == 20


def test_main_failing():
    assert main() == 10
