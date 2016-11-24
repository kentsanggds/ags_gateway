class Userinfo(object):

    def __init__(self):
        pass

    def __getitem__(self, item):
        return {}

    def __contains__(self, item):
        return True

    def get_claims_for(self, user_id, requested_claims):
        return {}
