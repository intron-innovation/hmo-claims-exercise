from flask import render_template, request

from . import claims as claims_blueprint
from .models import Claim
from .services import ClaimService
from ..users.models import User


@claims_blueprint.route('claim', methods=['GET'])
def claims():
    """
    List all Claims
    """
    service = ClaimService(request)
    all_claims = service.fetch_all_claims()
    return render_template('claims.html', claims=all_claims, title="Claims")


@claims_blueprint.route('create_claim', methods=['GET', 'POST'])
def create_claim():
    """
        A route for a claim officer to make/create a claim
    """

    service = ClaimService(request)

    if request.method == 'POST':
        # Get the form field values for claim model insertion

        user = request.form.get('user')
        diagnosis = request.form.get('diagnosis')
        hmo = request.form.get('hmo')

        total_cost = request.form.get('total_cost')
        service_charge = request.form.get('service_charge')
        final_cost = request.form.get('final_cost')

        user = User.query.filter_by(name=user).first()
        new_claim = Claim(user_id=user.id, diagnosis=diagnosis, hmo=hmo, service_charge=service_charge,
                          total_cost=total_cost, final_cost=final_cost)
        database.session.add(new_claim)
        database.session.commit()

        # Get the form field values for service model insertion
        service_name = request.form.getlist('service_name')
        service_type = request.form.getlist('type')
        provider_name = request.form.getlist('provider_name')
        source = request.form.getlist('source')
        cost_of_service = request.form.getlist('cost_of_service')

        dates = request.form.getlist('service_date')

        # Formate dates
        service_date = []
        for d in dates:
            service_date.append(datetime.strptime(d, '%Y-%m-%d'))
        print("Anthony", service_date)

        # Get the above claim as foreign key for services
        claim = Claim.query.filter().last()

        # Loop to enter possible list of services
        for i in range(len(service_name)):
            new_service = Service(claim_id=claim.id, service_date=service_date[i], service_name=service_name[i],
                                  type=service_type[i], provider_name=provider_name[i], source=source[i],
                                  cost_of_service=cost_of_service[i])
            database.session.add(new_service)
            database.session.commit()

        flash('Claim created successfully.', 'success')
        return redirect(url_for('home.claim'))
    else:
        context_data = service.claims_context()
        return render_template('create_claim.html', data=context_data)
#
