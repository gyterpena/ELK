# -*- coding: utf-8 -*-

import re

from csv_schema.exceptions import ImproperValueException


class BaseColumn(object):

    """Base for all column classes."""

    value_template = ''  # Schema of stored value
    improper_type_error_msg = u'Incompatible data type'
    no_blank_error_msg = u'This column can not be empty'

    _instance_counter = 0  # Counts number of instances. Needed in field ordering

    def __init__(self, **kwargs):
        self.options = kwargs
        self.blank = kwargs.get('blank', False)
        self._instance_counter = BaseColumn._instance_counter  # Override class attribute
        BaseColumn._instance_counter += 1

    def is_proper_value_format(self, raw_val):
        """Check if value has proper schema.

        :param raw_val: raw value from file
        :type raw_val: str
        :returns: True if ok, False if not
        :rtype: bool

        """
        return bool(re.match(self.value_template, raw_val))

    def convert(self, raw_val):
        """Convert raw data to Python object.

        :param raw_val: raw data
        :type raw_val: str
        :returns: Python object
        :rtype: the one you want

        """
        raise NotImplementedError

    def check_restriction(self, value):
        """Execute check of optional restriction.
        Raises ImproperValueRestrictionException when value does not meet restriction. 

        :param value: converted value
        :type value: the same as that returned by self.convert

        """
        pass

    def clean(self, raw_value):
        """Check if data piece assigned to this column is correct and return appropriate Python object.

        :param raw_value: uncleaned value
        :type raw_value: str
        :returns: cleaned value
        :rtype: object

        """
        if not raw_value:
            if self.blank:
                return raw_value
            else:
                raise ImproperValueException(self.no_blank_error_msg)
        if self.is_proper_value_format(raw_value):
            converted_value = self.convert(raw_value)
            self.check_restriction(converted_value)
            return converted_value
        else:
            raise ImproperValueException(self.improper_type_error_msg)
