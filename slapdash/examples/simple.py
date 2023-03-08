import slapdash


class Simple:
    a = 0.0
    b = 1
    c = "test"
    d = False

    def test(self):
        self.a += 0.1
        self.b += 1
        self.c += '!'
        self.d = not self.d


if __name__ == '__main__':
    simple = Simple()
    slapdash.run(simple)
