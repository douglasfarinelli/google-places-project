# coding=utf-8

import peewee
import unittest
from unittest.mock import patch, Mock
from fixtures import RESPONSE_PLACE_API


class PlaceModelTest(unittest.TestCase):

    @patch('googleplaces.models.GooglePlaceApi.fetch_search',
           Mock(return_value={'status': 'OK', 'results': RESPONSE_PLACE_API}))
    @patch('googleplaces.db.db', peewee.SqliteDatabase(':memory:'))
    def test_method_filter_db_or_google_api_returns_correct(self):
        from googleplaces.models import Place
        query = Place.filter_db_or_google_api('Dress & Go')
        self.assertTrue(query)

    @patch('googleplaces.db.db', peewee.SqliteDatabase(':memory:'))
    def test_validates_has_errors(self):
        from googleplaces.models import Place
        place = Place()
        self.assertTrue(place.validates())

    @patch('googleplaces.db.db', peewee.SqliteDatabase(':memory:'))
    def test_validates_returns_correct(self):
        from googleplaces.models import Place
        place = Place(
            place_id='foo', name='Foo',
            address='R. Foo, Bar - FO',
            latitude=-23.112, longitude=112
        )
        self.assertFalse(place.validates())


if __name__ == '__main__':
    unittest.main()
