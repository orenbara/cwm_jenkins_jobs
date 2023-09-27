class HelloWorld:

    def __init__(self, message):
        self.message = message

    def greet(self):
        return self.message


def test_hello_world():
    hello = HelloWorld("Hello, World!")
    assert hello.greet() == "Hello, World!"