# -*- coding: utf-8 -*-




class RemoveGirlTag(object):
    def __call__(self, values):
        return list(
            map(lambda v: v.strip().replace('Tags:', '').strip().split(' ,') if isinstance(v, str) else v,
                values)
        )


class Strip(object):
    def __call__(self, values):
        result = []
        for value in values:
            if value:
                if isinstance(value, str):
                    result.append(value.strip())
                else:
                    result.append(value)
        return result


class FormatMonthYear(object):
    def __call__(self, values):
        return list(
            map(lambda v: v.replace('\xa0', '-'),
                values)
        )
