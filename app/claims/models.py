from datetime import datetime
from app import database
from app.models import BaseModel


class HMOProvider(BaseModel):
    __tablename__ = "hmo_providers"

    name = database.Column(database.String(100), nullable=False, index=True)

    def __repr__(self):
        return f"<HMOProvider: {self.name}>"


class Claim(BaseModel):
    __tablename__ = 'claim'

    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    diagnosis = database.Column(database.String(1000))
    # hmo = database.Column(database.String(4))
    hmo_provider_id = database.Column(database.Integer, database.ForeignKey("hmo_providers.id"), nullable=False)
    age = database.Column(database.Integer, nullable=True)
    # total_cost = database.Column(database.Integer)
    # final_cost = database.Column(database.Integer)
    services = database.relationship('Service', backref='claim', lazy=True)

    def __repr__(self):
        return f"<Claim: {self.user_id}::{self.hmo_provider_id}>"

    def get_total_cost(self):
        total_cost = database.session.query(database.func.sum(Service.cost_of_service)).filter(
            Service.claim_id == self.id).scalar()
        return total_cost if total_cost else 0


class Service(BaseModel):
    __tablename__ = 'service'

    claim_id = database.Column(database.Integer, database.ForeignKey('claim.id'), nullable=False)
    service_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    name = database.Column(database.String(100), nullable=False, comment="Name of specific service.")
    type_ = database.Column(database.String(50), nullable=False, comment="Options are Hematology, Microbiology, "
                                                                         "Chemical, Pathology, Histopathology and "
                                                                         "Immunology.")
    provider_name = database.Column(database.String(100), nullable=False, comment="Full name of doctor who ordered "
                                                                                  "the test.")
    source = database.Column(database.String(100), nullable=False, comment="Name of Hospital where doctor works.")
    cost_of_service = database.Column(database.Integer)

    def __repr__(self):
        return f"<Service: {self.claim_id}::{self.type_}::{self.cost_of_service}>"
