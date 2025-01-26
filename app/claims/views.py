from flask import render_template, request, url_for, flash
from werkzeug.utils import redirect

from . import claims as claims_blueprint
from .services import ClaimService


@claims_blueprint.route('', methods=['GET'])
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
        _ = service.create_claim()
        return redirect(url_for('claims.claims'))

    else:
        context_data = service.claims_context()
        return render_template('create_claim.html', data=context_data)


@claims_blueprint.route('view_claim/<int:id>', methods=['GET'])
def view_claim(id):
    """
        A route to view a claim
    """
    service = ClaimService(request)

    claim = service.fetch_claim_by_id(id)

    return render_template('claim_data.html', claim=claim)


@claims_blueprint.route('edit_claim/<int:id>', methods=['GET', 'POST'])
def edit_claim(id):
    """
        A route to edit a claim
    """
    service = ClaimService(request)
    if request.method == "POST":
        _ = service.edit_claim(id)
        flash("Claim updated successfully.", "success")
        return redirect(url_for("claims.view_claim", id=id))

    else:
        claim = service.fetch_claim_by_id(id)
        context_data = service.claims_context()

        return render_template('edit_claim.html', data=context_data, claim=claim)


@claims_blueprint.route('delete_claim/<int:id>', methods=['POST'])
def delete_claim(id):
    """
        Route to delete a claim
    """
    service = ClaimService(request)
    service.delete_claim(id)

    flash('Claim deleted successfully.', 'success')

    return redirect(url_for("claims.claims"))


@claims_blueprint.route('add_claim_service/<int:id>', methods=['POST', 'GET'])
def add_claim_service(id):
    """
        id: <Claim.id>
        Route to add a new service to claim
    """
    service = ClaimService(request)
    if request.method == 'POST':
        _ = service.add_claim_service(id)

        flash("Service added successfully", 'success')
        return redirect(url_for("claims.view_claim", id=id))

    else:
        return render_template("add_claim_service.html", claim_id=id)

@claims_blueprint.route('edit_claim_service/<int:id>', methods=['POST', 'GET'])
def edit_claim_service(id):
    service = ClaimService(request)
    claim_service = service.fetch_service_by_id(id)

    if request.method == 'POST':
        claim = service.edit_claim_service(id)

        flash("Service updated successfully.", "success")
        return redirect(url_for("claims.view_claim", id=claim.id))
    else:
        return render_template('edit_claim_service.html', service=claim_service)

@claims_blueprint.route('delete_claim_service/<int:id>', methods=["POST"])
def delete_claim_service(id):
    """
        Route to delete a service
    """
    service = ClaimService(request)
    claim = service.delete_service_by_id(id)

    flash('Service deleted successfully.', 'success')

    return redirect(url_for("claims.view_claim", id=claim.id))