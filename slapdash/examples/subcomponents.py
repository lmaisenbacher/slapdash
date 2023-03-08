import slapdash


class SubComponent1:
    cool_a = False
    string_b = "test"
    int_c = 1
    float_d = 0.0


class SubComponent2:
    float_a = 0.0
    int_b = 1
    string_c = "test"
    cool_d = False


class Subcomponent3:
    float_a = 0.0
    int_b = 1
    string_c = "test"
    cool_d = False
    sub2 = SubComponent2()
    sub4 = SubComponent1()


class Channel:
    voltage: float = 0.0
    current: float = 0.0


class TopComponent:
    float_1 = 0.0
    string_2 = 'test'
    bool_3 = False

    def __init__(self):
        self.sub1 = SubComponent1()
        self.channels = [Channel() for i in range(4)]
        self.sub3 = Subcomponent3()


if __name__ == '__main__':
    top = TopComponent()
    slapdash.run(top)
