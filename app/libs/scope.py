
class Scope(object):
    allow_api = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))

class UserScope(Scope):
    allow_api = ['v1.get_user','v1.delete_user','v1.search','v1.detail']

class AdminScope(Scope):
    allow_api = ['v1.super_get_user']

    def __init__(self):
        self + UserScope()

def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    print(scope)
    if endpoint in scope.allow_api:
        return True
    else:
        return False