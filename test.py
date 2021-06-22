class A(object):

    def __init__(self, q):
        print('A.__init__' + q)


class B(A):
    def __init__(self):
        print('B.__init__')

    def a(self):
        super().__init__(q="213")


k = B()
k.a()