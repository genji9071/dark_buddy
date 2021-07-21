import time

l = {}


class state():
    def __init__(self, initial_function):
        self.initial_function = initial_function
        if callable(self.initial_function):
            l[initial_function.__name__] = {'function': self.initial_function,
                                            'result': self.initial_function.__call__()}

    def set(self, element):
        self.initial_function = element
        for f in l:
            l[f] = {'function': l[f]['function'], 'result': l[f]['function'].__call__()}

    def get(self):
        if callable(self.initial_function):
            return l[self.initial_function.__name__]['result']
        else:
            return str(self.initial_function)


x = state(0)

x.set(0)

print('first x ' + x.get())


def do_y():
    time.sleep(1)
    return str(int(x.get()) + 1)


y = state(do_y)


def do_z():
    return str([x.get(), y.get(), int(x.get()) + int(y.get())])


z = state(do_z)

x.set(1)

print('second x ' + x.get())
print('second y ' + y.get())
print('second z ' + z.get())

x.set(10)

print('third x ' + x.get())
print('third y ' + y.get())
print('third z ' + z.get())
