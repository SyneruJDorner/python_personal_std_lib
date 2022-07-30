class Singleton():
    '''
    A decorator that creates a singleton out of a class.
    '''

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self, *args, **kwargs):
        '''
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.
        '''
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated(*args, **kwargs)
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)