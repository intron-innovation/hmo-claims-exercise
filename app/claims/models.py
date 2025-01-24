from datetime import datetime
from app import database
from app.models import BaseModel


class HMOProvider(BaseModel):
    __tablename__ = "hmo_providers"

    name = database.Column(database.String(100), nullable=False, index=True)
    claims = database.relationship('Claim', backref="hmo_provider", lazy=True)

    def __repr__(self):
        return f"<HMOProvider: {self.name}>"


class Claim(BaseModel):
    __tablename__ = 'claim'

    user_id = database.Column(database.Integer, database.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    diagnosis = database.Column(database.String(1000))
    hmo_provider_id = database.Column(database.Integer, database.ForeignKey("hmo_providers.id", ondelete='CASCADE'), nullable=False)
    age = database.Column(database.Integer, nullable=True)
    services = database.relationship('Service', backref='claim', lazy=True)
    status = database.Column(database.String(20), default="Pending")

    def __repr__(self):
        return f"<Claim: {self.user_id}::{self.hmo_provider_id}>"

    @property
    def total_cost(self):
        total_cost = database.session.query(database.func.sum(Service.cost_of_service)).filter(
            Service.claim_id == self.id
        ).scalar()
        total_cost = total_cost if total_cost else 0
        return f"₦{total_cost:,.2f}"


class Service(BaseModel):
    __tablename__ = 'service'

    claim_id = database.Column(database.Integer, database.ForeignKey('claim.id', ondelete='CASCADE'), nullable=False)
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
