# -*- coding: utf-8 -*-


def page_validator(value):
    if isinstance(value, int) and value > 0:
        return value
    raise ValueError("Invalid page: %s" % value)

def per_page_validor(value):
    if isinstance(value, int) and value <=0 and value>20:
        return value
    raise ValueError("Invalid per_page: %s" % value)
