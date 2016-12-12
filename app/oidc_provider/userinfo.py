class Userinfo(dict):

    def get_claims_for(self, user_id, requested_claims):

        claims = {}
        userinfo = self.get(user_id)

        if userinfo:

            for claim, spec in requested_claims.items():

                if claim in userinfo:
                    claims[claim] = userinfo[claim]

        return claims
