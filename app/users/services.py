import logging
from datetime import datetime, date
from flask import flash
from flask.json import jsonify
from .models import User
from ..utils.utils import CustomRequestService


class UserService(CustomRequestService):
    def __init__(self, request):
        super().__init__(request)

    def fetch_all_users(self):
        try:
            return self.set_pagination(model=User)
        except Exception as e:
            self.make_500(e)

    def fetch_single_user_by_id(self, id):
        return User.query.get_or_404(id)

    def edit_user(self, id):
        try:
            user = self.fetch_single_user_by_id(id)
            name = self.form_params.get('name')
            gender = self.form_params.get('gender')
            salary = self.form_params.get('salary')
            date_of_birth = self.form_params.get('date_of_birth')
            dt_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')

            user.name = name
            user.gender = gender
            user.salary = salary
            user.date_of_birth = dt_obj

            self.commit_database()

            flash("User updated successfully!", "success")

            return user

        except Exception as e:
            self.make_500(e)

    def create_user(self):
        try:
            name = self.form_params.get('name')
            gender = self.form_params.get('gender')
            salary = self.form_params.get('salary')
            date_of_birth = self.form_params.get('date_of_birth')
            dt_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')

            new_user = User(name=name, gender=gender, salary=salary, date_of_birth=dt_obj)

            self.commit_database(new_user)

            flash('User created successfully.', 'success')

        except Exception as e:
            self.make_500(e)

    def delete_user(self, id):
        try:
            user = self.fetch_single_user_by_id(id)
            self.delete_database(user)

            flash('User deleted successfully.', 'success')

        except Exception as e:
            self.make_500(e)

    def calculate_user_age(self):
        try:
            user_id = self.form_params.get("id")
            user = User.query.get(user_id)

            if user is None:
                response = {
                    "error": f"User with id {user_id} Not found!"
                }
            else:
                age = (date.today().year - user.date_of_birth.year)
                response = {
                    "data": {
                        "age": age
                    }
                }

            return jsonify(response)

        except Exception as e:
            logging.error(e)
            return jsonify({"error": "An error occurred!"})