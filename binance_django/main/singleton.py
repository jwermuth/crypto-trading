class Singleton(type):
    """See https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python?answertab=active#tab-top"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
