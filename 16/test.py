class A:
    @classmethod
    def a(cls):
        print(cls)


class B(A):
    pass


B.a()
