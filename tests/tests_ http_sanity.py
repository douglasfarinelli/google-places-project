# coding=utf-8

import peewee
import json
from unittest.mock import patch, Mock
from tornado.testing import main, AsyncHTTPTestCase
from fixtures import RESPONSE_PLACE_API


class ApiTest(AsyncHTTPTestCase):

    @patch('googleplaces.db.db',
           peewee.SqliteDatabase(':memory:'))
    def setUp(self):
        super(ApiTest, self).setUp()

    def get_app(self):
        from googleplaces.app import app
        return app

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'OK', 'results': RESPONSE_PLACE_API}))
    def test_get_method(self):
        self.http_client.fetch(self.get_url('/places/?name=Dress+&+Go'),
                               self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'OK', 'results': RESPONSE_PLACE_API}))
    def test_get_method_raises_if_query_string_name_is_none(self):
        self.http_client.fetch(self.get_url('/places/?'),
                               self.stop)
        response = self.wait()
        self.assertEqual(response.code, 400)

    def test_post_method(self):
        self.http_client.fetch(
            self.get_url('/places/'),
            self.stop,
            body=json.dumps(dict(
                place_id='foo', name='Foo',
                address='R. Foo, Bar - FO',
                latitude=-23.112, longitude=112)),
            method='POST',
        )
        response = self.wait()
        self.assertEqual(response.code, 201)

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'OK', 'results': RESPONSE_PLACE_API}))
    def test_delete_method(self):
        from googleplaces.models import Place
        new_place = Place.filter_db_or_google_api('Dress & Go').first()
        self.http_client.fetch(
            self.get_url('/places/%s/' % new_place.id),
            self.stop,
            method='DELETE'
        )
        response = self.wait()
        self.assertEqual(response.code, 204)  #: Retorna 599 ???

if __name__ == '__main__':
    main()
