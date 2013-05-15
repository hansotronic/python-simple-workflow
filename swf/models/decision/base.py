#! -*- coding:utf-8 -*-

# Copyright (c) 2013, Theo Crevon
# Copyright (c) 2013, Greg Leclercq
#
# See the file LICENSE for copying permission.

from functools import wraps

from swf.utils import decapitalize


def decision_action(fn):
    """Ensures the decorated method class instance is bootstraped
    with decision type, attributes_key, and body"""
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        self._fill_from_action(fn.__name__)
        return fn(self, *args, **kwargs)
    return wrapper


class Decision(dict):
    """Base decision message wrapper

    subclasses dictionary and provides attributes and methods
    to build a suitable Decision message that Amazon service will
    understand.

    It is meant to be subclassed, and does not intend to be intstantiated
    by itself.
    """
    _attributes_key_suffix = 'DecisionAttributes'
    _base_type = None

    def __init__(self):
        super(Decision, self).__init__()

    def _fill_from_action(self, action):
        self.type = action.capitalize() + self._base_type
        self.attributes_key = decapitalize(self.type + self._attributes_key_suffix)

        self['decisionType'] = self.type
        self[self.attributes_key] = {}

    def update_attributes(self, data):
        """Updates Decision instance attributes_key dictionary
        with provided data which values is not None"""
        if not hasattr(self, 'attributes_key'):
            raise AttributeError("Can't update unset attributes_key"
                                 "decision attritute")

        for key, value in data.iteritems():
            if value:
                self[self.attributes_key].update({key: value})