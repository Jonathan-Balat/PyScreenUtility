
class ModDict(dict):

    """ WIP """

    def __init__(self, seq=None, **kwargs):
        super(ModDict, self).__init__(seq=seq, **kwargs)

    def add_if_none(self, key, value):
        if key not in self:
            self[key] = value