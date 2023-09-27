class HelloWorld:

    def __init__(self, message):
        self.message = message

    def greet(self):
        print(self.message)


if __name__ == "__main__":
    hello = HelloWorld("Hello, World!")
    hello.greet()
