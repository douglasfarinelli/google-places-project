# coding=utf=8

import json
from tornado.web import RequestHandler
from googleplaces.models import Place
from googleplaces.exceptions import InvalidJSONError, InvalidRequestError, PlaceDoesNotExistError


class ApiJSONView(RequestHandler):
    """View base para lidar com as solicitações do tipo
    json."""

    @property
    def data(self):
        try:
            return json.loads(self.request.body.decode())
        except ValueError:
            raise InvalidJSONError()

    def send_json(self, data, status_code=None):
        self.set_status(status_code=status_code or 200)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(data))

    def write_error(self, status_code, **kwargs):
        json_error = {'code': status_code, 'message': self._reason}
        if 'exc_info' in kwargs:
            exc = kwargs.get('exc_info')[1]
            if hasattr(exc, 'log_message'):
                json_error['log_message'] = exc.log_message
        self.send_json(json_error, status_code=int(status_code))


class PlacesView(ApiJSONView):
    """View para lidar com o recurso /places/.

    Retorna, cadastra e deleta locais específicos a Api Google Places.
    """

    def get(self):
        name = self.get_query_argument('name', None)
        if name is None:
            raise InvalidRequestError()
        query = Place.filter_db_or_google_api(name)
        self.send_json([m.as_dict() for m in query])

    def post(self):
        place = Place(**self.data)
        errors = place.validates()
        if errors:
            self.send_json(errors, status_code=400)
        else:
            place.save()
            self.send_json(place.as_dict(), status_code=201)

    def delete(self, pk=None):
        try:
            place = Place.get(id=pk)
        except Place.DoesNotExist:
            raise PlaceDoesNotExistError()
        else:
            place.delete()
            self.send_json('', status_code=204)
