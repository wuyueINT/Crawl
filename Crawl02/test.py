class Testclass:

    def __init__(self, a):
        self.a = a

    def method1(self, a):
        yield from self.method2(2)
        yield a

    def method2(self, a):
        yield a


if __name__ == "__main__":

    tc = Testclass(0)
    for n in tc.method1(1):
        print(n)


