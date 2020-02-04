class LinguisticVar:
    def __init__(self, membership_funcs, name):
        self._membership_funcs = membership_funcs
        self._name = name

    @property
    def membership_funcs(self):
        return self._membership_funcs
