# -*- coding: utf-8 -*-

from girls.config import prod
from girls.core.main import app_factory

app = app_factory(prod)
