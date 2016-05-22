# coding=utf-8

import peewee
import peewee_validates
import logging
from json import loads
from googleplaces.db import db
from googleplaces.exceptions import (
    PlaceDoesNotExistError, InvalidRequestError,
    OverQueryLimitError, RequestDeniedError
)

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

LOGGER = logging.getLogger('googleplaces.ops')
LOGGER.setLevel(logging.DEBUG)
GOOGLE_PLACE_API_KEY = 'AIzaSyBvStMyLJ9WxFIdJJ7J-GQx6wAm0E-MLRA'


class GooglePlaceApi:
    """Classe para lidar com a google api."""

    BASE_URL = 'https://maps.googleapis.com/maps/api'
    PLACE_URL = BASE_URL + '/place'
    TEXT_SEARCH_API_URL = 'textsearch/json'

    RESPONSE_STATUS_OK = 'OK'
    RESPONSE_STATUS_ZERO_RESULTS = 'ZERO_RESULTS'
    RESPONSE_STATUS_INVALID_REQUEST = 'INVALID_REQUEST'
    RESPONSE_STATUS_OVER_QUERY_LIMIT = 'OVER_QUERY_LIMIT'
    RESPONSE_STATUS_REQUEST_DENIED = 'REQUEST_DENIED'

    def __init__(self, api_key):
        """
        :param api_key:
            É a chave de autenticação na Google Api.
            Para gerar uma acesse: https://console.developers.google.com/apis/credentials.
        """
        self._api_key = api_key

    def fetch_search(self, query):
        url = (
            '{0.PLACE_URL}/'
            '{0.TEXT_SEARCH_API_URL}'
            '?{query}'.format(self, query=query)
        )
        LOGGER.debug('googleplaces.api: sent request %s' % url)
        with urlopen(url) as response:
            return loads(
                response.read().decode(response.info().get_param('charset') or 'utf-8')
            )


    def get_place(self, name):
        """Efetua uma busca na api do tipo 'textsearch'.

        :param name:
            É o nome do local a ser pesquisado.
        :raises:
            InvalidRequestError, OverQueryLimitError, RequestDeniedError,
            PlaceDoesNotExistError.
        :return:
            Retorna uma lista de locais.
        """
        json = self.fetch_search(urlencode(dict(key=self._api_key, query=name)))

        if json['status'] == self.RESPONSE_STATUS_INVALID_REQUEST:
            raise InvalidRequestError()

        elif json['status'] == self.RESPONSE_STATUS_OVER_QUERY_LIMIT:
            raise OverQueryLimitError()

        elif json['status'] == self.RESPONSE_STATUS_REQUEST_DENIED:
            raise RequestDeniedError()

        elif json['status'] == self.RESPONSE_STATUS_ZERO_RESULTS:
            raise PlaceDoesNotExistError()

        return [dict(address=place.get('formatted_address'),
                     name=place.get('name'),
                     place_id=place.get('id'),
                     latitude=place.get('geometry').get('location').get('lat'),
                     longitude=place.get('geometry').get('location').get('lng'))
                for place in json.get('results')]


google_api = GooglePlaceApi(api_key=GOOGLE_PLACE_API_KEY)


class Model(peewee.Model):
    """Model base."""

    class Meta:

        database = db

    def as_dict(self):
        """Retorna um dicionário com o nome e o valor do campo de acordo
        com a instância."""
        return {field_name: getattr(self, field_name)
                for field_name in self._meta.fields}


class Place(Model):
    """Model com regras e métodos extras de gerenciamento
    do recurso /places/."""

    place_id = peewee.TextField(
        index=True, unique=True, verbose_name='Google Place ID',
    )
    name = peewee.TextField(
        verbose_name='Place Name',
    )
    address = peewee.TextField(
        verbose_name='Full Address',
    )
    latitude = peewee.FloatField(
        verbose_name='Latitude',
    )
    longitude = peewee.FloatField(
        verbose_name='Longitude',
    )

    def validates(self):
        """Válida todos os campos da model. Se houver erros, retorna um
        dicionário com a chave representando o nome do campo e o valor
        com o erro encontrado, de acordo com os valores da instância.

        :return:
            Retorna um dicionário.
        """
        try:
            validator = peewee_validates.ModelValidator(self)
            validator.validate(data=self.as_dict())
            return validator.errors
        except peewee.IntegrityError:
            return {'place_id': 'is already'}

    @classmethod
    def filter_db_or_google_api(cls, name):
        """Efetua a busca no banco e caso não exista nenhuma informação
        com o termo pesquisado, busca da google api, cadastra no banco
        e retorna a queryset.

        :param name:
            É o nome do local a ser pesquisado.
        :return:
            Retorna uma queryset.
        """
        if not cls.filter(name__like=name).exists():
            with db.transaction():
                query = cls.insert_many([
                    p for p in google_api.get_place(name)
                ]).upsert(upsert=True)
                for q in query.sql():
                    LOGGER.debug(q)
                query.execute()
        query = cls.filter(name__like=name)
        LOGGER.debug(query.sql())
        return query


if not Place.table_exists():
    for q in Place.sqlall():
        LOGGER.debug(q)
    Place.create_table()

