from werkzeug.exceptions import abort
import logging
from app import database


class BaseService:
    def __init__(self, request):
        self.request = request
        self.filter_params = self.request.args
        self.form_params = self.request.form


class PaginationService(BaseService):

    def __init__(self, request):
        super().__init__(request=request)
        self.page = self.filter_params.get("page", 1, type=int)
        self.per_page = self.filter_params.get("per_page", 10, type=int)

    def set_pagination(self, model):
        result = model.query.paginate(page=self.page, per_page=self.per_page)

        return result


class CustomRequestService(PaginationService):
    def __init__(self, request):
        super().__init__(request=request)

    def database_session_commit(self):
        database.session.commit()

    def commit_database(self, model_object=None):
        if model_object:
            if not isinstance(model_object, list):
                model_object = [model_object]

            for model_obj in model_object:
                database.session.add(model_obj)

        self.database_session_commit()

        return True

    def delete_database(self, model_object):
        if model_object:
            if not isinstance(model_object, list):
                model_object = [model_object]

            for model_obj in model_object:
                database.session.delete(model_obj)

        self.database_session_commit()

        return True

    def make_500(self, e):
        logging.error(msg=e)
        abort(500)