# -*- coding: utf-8 -*-

from decimal import Decimal

from csv_schema.columns.base import BaseColumn
from csv_schema.exceptions import ImproperValueRestrictionException


class IntColumn(BaseColumn):

    value_template = '^(-\d)?\d*$'

    def convert(self, raw_val):
        return int(raw_val)

    def check_restriction(self, value):
        min_exclusive = self.options.get('min_exclusive', None)
        max_exclusive = self.options.get('max_exclusive', None)
        min_inclusive = self.options.get('min_inclusive', None)
        max_inclusive = self.options.get('max_inclusive', None)

        if min_inclusive is not None and min_exclusive is not None:
            raise Exception('You can specify only one of the parameters: min_inclusive or min_exclusive')
        if max_inclusive is not None and max_exclusive is not None:
            raise Exception('You can specify only one of the parameters: max_inclusive or max_exclusive')

        if min_inclusive is not None:
            if value < min_inclusive:
                raise ImproperValueRestrictionException(u'The value must not be less than {}'.format(min_inclusive))
        if min_exclusive is not None:
            if value <= min_exclusive:
                raise ImproperValueRestrictionException(u'The value can not be less than or equal {}'.format(min_exclusive))
        if max_inclusive is not None:
            if value > max_inclusive:
                raise ImproperValueRestrictionException(u'The value can not be greater than {}'.format(max_inclusive))
        if max_exclusive is not None:
            if value >= max_exclusive:
                raise ImproperValueRestrictionException(u'The value can not be greater than or equal {}'.format(max_exclusive))


class DecimalColumn(IntColumn):

    value_template = '^(-\d)?\d*\.?\d*$'

    def convert(self, raw_val):
        return Decimal(raw_val)

    def check_restriction(self, value):
        fraction_digits = self.options.get('fraction_digits', None)
        total_digits = self.options.get('total_digits', None)

        decimal_info = value.as_tuple()
        if fraction_digits is not None:
            if (decimal_info.exponent * -1) > fraction_digits:
                raise ImproperValueRestrictionException(u'The value can not be more than %d digits after the decimal point' % fraction_digits)
        if total_digits is not None:
            if len(decimal_info.digits) > total_digits:
                raise ImproperValueRestrictionException(u'The value can not be more than %d digits' % total_digits)
        return super(DecimalColumn, self).check_restriction(value)


class StringColumn(BaseColumn):

    value_template = '.*\S.*'

    def convert(self, raw_val):
        return raw_val

    def check_restriction(self, value):
        min_length = self.options.get('min_length', None)
        max_length = self.options.get('max_length', None)
        permissible_values = self.options.get('permissible_values', None)

        if min_length is not None:
            if len(value) < min_length:
                raise ImproperValueRestrictionException(u'The value can not be less than %d' % min_length)
        if max_length is not None:
            if len(value) > max_length:
                raise ImproperValueRestrictionException(u'The value can not be longer than %d' % max_length)
        if permissible_values is not None:
            if value not in permissible_values:
                raise ImproperValueRestrictionException(u'The value is not one of the acceptable')
