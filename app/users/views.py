from flask import render_template, request, flash, url_for
from werkzeug.utils import redirect
from . import users as users_blueprint
from .services import UserService
from .forms import AddUser


@users_blueprint.route('/', methods=['GET'])
def all_users():
    """
    List all Users
    """
    service = UserService(request)
    users = service.fetch_all_users()

    return render_template('users.html', users=users, title="Users")


@users_blueprint.route('/user/<int:id>', methods=['GET', 'POST'])
def view_user(id):
    """
        A route that allows claim officer fillout a form for a particular user
    """
    service = UserService(request)
    user_data = service.fetch_single_user_by_id(id)

    return render_template('user_data.html', user_data=user_data)


@users_blueprint.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    """
        A route for editing a user record
    """
    form = AddUser()
    service = UserService(request)
    user_data = service.fetch_single_user_by_id(id)

    if request.method == 'POST':
        if form.validate_on_submit():
            service = UserService(request)
            _ = service.edit_user(id)

            return redirect(url_for('users.edit_user', id=id))
        else:
            flash("Something went wrong!", "warning")
            return render_template('edit_user.html', user_data=user_data, form=form)

    return render_template('edit_user.html', user_data=user_data, form=form)


@users_blueprint.route('/add', methods=['GET', 'POST'])
def add_user():
    """
        A route for adding users
    """
    form = AddUser()
    service = UserService(request)

    if request.method == 'POST':
        if form.validate_on_submit():
            _ = service.create_user()
            return redirect(url_for('users.all_users'))

        else:
            flash('You entered and invalid form data', 'danger')

        return render_template('create_user.html', form=form)
    else:
        return render_template('create_user.html', form=form)


@users_blueprint.route('/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """
        A route for deleting a user
    """
    service = UserService(request)
    _ = service.delete_user(id)

    return redirect(url_for('users.all_users'))


@users_blueprint.route('/age', methods=['POST'])
def user_age():
    """
        A route to get a user's birthdate and calculate his age
    """
    if request.method == "POST":
        service = UserService(request)
        return service.calculate_user_age()
