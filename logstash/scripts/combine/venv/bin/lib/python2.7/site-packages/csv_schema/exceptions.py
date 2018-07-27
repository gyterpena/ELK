# -*- coding: utf-8 -*-

"""Module containing exceptions used in csv_schema."""

class ImproperValueException(Exception):

    """Exception thrown when value has unacceptable format."""

    pass


class ImproperValueRestrictionException(Exception):

    """Exception thrown when value does not satisfy column restrictions."""

    pass
