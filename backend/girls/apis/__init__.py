# -*- coding: utf-8 -*-

from flask_restplus import Api
from .ns_girl import ns_girl

api = Api(title="DataHub",
          version='1.0',
          description='All funny things are here',
          doc='/doc/')

api.add_namespace(ns_girl)
