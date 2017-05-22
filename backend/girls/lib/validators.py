# -*- coding: utf-8 -*-


def page_validator(value):
    value = int(value)
    if isinstance(value, int) and value > 0:
        return value
    raise ValueError("Invalid page: %s" % value)


def per_page_validator(value):
    value = int(value)
    if isinstance(value, int) and 0 < value <= 20:
        return value
    raise ValueError("Invalid per_page: %s" % value)
