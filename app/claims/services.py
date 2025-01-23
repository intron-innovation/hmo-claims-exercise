from app.claims.models import Claim, HMOProvider
from app.users.models import User
from app.utils.utils import CustomRequestService


class ClaimService(CustomRequestService):
    def __init__(self, request):
        super().__init__(request)

    def fetch_all_claims(self):
        try:
            return self.set_pagination(model=Claim)
        except Exception as e:
            self.make_500(e)

    def claims_context(self):
        users = User.query.all()[:20]
        hmo_providers = HMOProvider.query.with_entities(HMOProvider.name).all()

        return {
            "users": users,
            "hmo_providers": hmo_providers
        }
