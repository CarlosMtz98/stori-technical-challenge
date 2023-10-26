from app.hello_world import say_hello


class TestHelloWorld:
    def test_dummy_test(self):
        assert 1 + 1 == 2

    def test_hello_world(self):
        assert say_hello() == "Hello World!"
