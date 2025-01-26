from datetime import datetime

from flask import flash

from app.claims.models import Claim, HMOProvider, Service
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
        hmo_providers = HMOProvider.query.all()

        return {
            "users": users,
            "hmo_providers": hmo_providers
        }

    def create_services(self, services):
        service_to_db = []

        for service in services:
            service = Service(**service)
            service_to_db.append(service)

        self.commit_database(service_to_db)

    def create_claim(self):
        user = self.form_params.get('user')
        diagnosis = self.form_params.get('diagnosis')
        hmo = self.form_params.get('hmo_provider')
        age = self.form_params.get('age')

        claim = Claim(user_id=user, diagnosis=diagnosis, hmo_provider_id=hmo, age=age)
        _ = self.commit_database(claim)

        # Get the form field values for service model insertion
        service_names = self.form_params.getlist('service_name')
        service_types = self.form_params.getlist('claim_type')
        provider_names = self.form_params.getlist('provider_name')
        sources = self.form_params.getlist('source')
        costs_of_services = self.form_params.getlist('cost_of_service')

        dates = self.form_params.getlist('service_date')
        service_dates = []

        for date in dates:
            service_dates.append(datetime.strptime(date, "%Y-%m-%d"))

        services = []

        for i in range(len(service_names)):
            services.append({
                "claim_id": claim.id,
                "service_date": service_dates[i],
                "name": service_names[i],
                "type_": service_types[i],
                "provider_name": provider_names[i],
                "source": sources[i],
                "cost_of_service": costs_of_services[i]
            })

        # Create Services for the Claim
        self.create_services(services)

        flash("Claim created successfully.", "success")

        return claim

    def fetch_claim_by_id(self, id):
        return Claim.query.get_or_404(id)

    def delete_services_for_claim(self, claim):
        for service in claim.services:
            self.delete_database(service)

    def fetch_service_by_id(self, id):
        return Service.query.get_or_404(id)

    def delete_service_by_id(self, id):
        claim_service = self.fetch_service_by_id(id)

        claim = claim_service.claim
        self.delete_database(claim_service)

        return claim

    def add_claim_service(self, id):
        claim = self.fetch_claim_by_id(id)
        try:
            name = self.form_params.get("name")
            type_ = self.form_params.get("claim_type")
            provider_name = self.form_params.get("provider_name")
            source = self.form_params.get("source")
            date = self.form_params.get("service_date")
            service_date = datetime.strptime(date, "%Y-%m-%d")
            cost_of_service = self.form_params.get("cost_of_service")

            new_claim_service = Service(claim_id=claim.id, name=name, type_=type_, provider_name=provider_name, source=source,
                    service_date=service_date, cost_of_service=cost_of_service)

            self.commit_database(new_claim_service)

        except Exception as e:
            self.make_500(e)


    def edit_claim_service(self, id):
        service = self.fetch_service_by_id(id)
        try:
            name = self.form_params.get("name") or service.name
            type_ = self.form_params.get("claim_type") or service.type_
            provider_name = self.form_params.get("provider_name") or service.provider_name
            source = self.form_params.get("source") or service.source
            date = self.form_params.get("service_date") or service.service_date
            service_date = datetime.strptime(date, "%Y-%m-%d")
            cost_of_service = self.form_params.get("cost_of_service") or service.cost_of_service

            service.name = name
            service.type_ = type_
            service.provider_name = provider_name
            service.service_date = service_date
            service.source = source
            service.cost_of_service = cost_of_service

            self.commit_database()

            return service.claim

        except Exception as e:
            self.make_500(e)

    def delete_claim(self, id):
        claim = self.fetch_claim_by_id(id)
        try:
            self.delete_services_for_claim(claim)

            self.delete_database(claim)

        except Exception as e:
            self.make_500(e)

    def edit_claim(self, id):
        from app.users.services import UserService

        claim = self.fetch_claim_by_id(id)
        user_id = self.form_params.get("user")

        user_service = UserService(self.request)
        user = user_service.fetch_single_user_by_id(user_id)

        try:
            diagnosis = self.form_params.get("diagnosis")
            hmo_provider = self.form_params.get("hmo_provider")
            age = self.form_params.get("age")

            claim.diagnosis = diagnosis
            claim.hmo_provider_id = hmo_provider
            claim.age = age
            claim.user = user

            self.commit_database()
        except Exception as e:
            self.make_500(e)

    def delete_claims_for_user(self, user):
        claims = user.claims

        for claim in claims:
            self.delete_claim(claim.id)
