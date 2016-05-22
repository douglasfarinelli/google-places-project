# coding=utf-8

import peewee
import unittest
from unittest.mock import patch, Mock
from googleplaces.exceptions import (
    PlaceDoesNotExistError, OverQueryLimitError,
    RequestDeniedError, InvalidRequestError
)

from fixtures import DUMMY_KEY, RESPONSE_PLACE_API


class GooglePlaceApiTest(unittest.TestCase):

    @patch('googleplaces.db.db', peewee.SqliteDatabase(':memory:'))
    def setUp(self):
        from googleplaces.models import GooglePlaceApi
        self.google_api = GooglePlaceApi(DUMMY_KEY)

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'ZERO_RESULTS'}))
    def test_raises_doesnotexist_error(self):
        with self.assertRaises(PlaceDoesNotExistError):
            self.google_api.get_place('Foo')

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'OVER_QUERY_LIMIT'}))
    def test_raises_over_limit_error(self):
        with self.assertRaises(OverQueryLimitError):
            self.google_api.get_place('Foo')

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'REQUEST_DENIED'}))
    def test_raises_request_denied_error(self):
        with self.assertRaises(RequestDeniedError):
            self.google_api.get_place('Foo')

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'INVALID_REQUEST'}))
    def test_raises_invalid_request_error(self):
        with self.assertRaises(InvalidRequestError):
            self.google_api.get_place('Foo')

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'OK', 'results': RESPONSE_PLACE_API}))
    def test_returns_correct(self):
        places = self.google_api.get_place('Dress & Go')
        self.assertIsInstance(places, list)
        self.assertDictEqual(places[0], {
            'address': 'R. Santa Justina, 352 - Vila Olimpia, São Paulo - SP, 04545-041, Brazil',
            'latitude': -23.5949846,
            'longitude': -46.6764696,
            'name': 'Dress & Go',
            'place_id': 'e89f32a7476e28fc4481caf9a2c116e896645eb8'
        })

if __name__ == '__main__':
    unittest.main()
