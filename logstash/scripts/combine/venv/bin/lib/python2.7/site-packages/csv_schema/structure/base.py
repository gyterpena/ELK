# -*- coding: utf-8 -*-


from csv_schema.columns.base import BaseColumn
from csv_schema.exceptions import (
    ImproperValueException,
    ImproperValueRestrictionException,
)
from csv_schema.structure.set import Cs


class BaseCsvStructureMeta(type):

    """BaseCsvStructure metaclass."""

    def __new__(cls, name, bases, attrs):
        """Dodaje liste z posortowanymi w kolejnosci definicji polami"""
        tmp_list = [(name, obj._instance_counter) for name, obj in attrs.items() if isinstance(obj, BaseColumn)]
        tmp_list.sort(key=lambda t: t[1])
        attrs['column_order'] = [t[0] for t in tmp_list]
        return super(BaseCsvStructureMeta, cls).__new__(cls, name, bases, attrs)


class BaseCsvStructure(object):

    """Base for classes that describe line structure in CSV file."""

    __metaclass__ = BaseCsvStructureMeta

    class Rules(object):  # Inner class used for containing schema rules
        pass

    def __init__(self, data, line_no):
        """

        :param data: data from CSV file
        :type data: list
        :param line_no: number of current line in CSV file
        :type line_no: int

        """
        self._raw_data = data
        self.errors = []
        self.line_no = line_no
        self.no_of_column = len(self.column_order)

    def _prepare_data(self):
        """Check types and data restrictions for each column.
        Add self.columns that contains bond between column name and its value.
        """
        self.columns = {}

        for index, raw_val in enumerate(self._raw_data):
            column_obj = getattr(self, self.column_order[index])
            try:
                self.columns[self.column_order[index]] = column_obj.clean(raw_val)
            except (ImproperValueException, ImproperValueRestrictionException) as e:
                self.errors.append(u'Line %d, column %d: %s' % (self.line_no, index, e.message))

    def _extract_rules(self):
        """Search self.Rules for defined schema rules.

        :returns: extracted rules objects
        :rtype: list

        """
        rules = []
        for _, probable_cs in vars(self.Rules).items():
            if isinstance(probable_cs, Cs):
                rules.append(probable_cs)
        return rules

    def _handel_rule(self, rule):
        """Execute single rule and handle it result.

        :param rule: rule described by Cs objects
        :type rule: csv_schema.structure.set.Cs

        """
        if not rule(self.columns):
            self.errors.append(u'Line %d: %s' % (self.line_no, rule.error_msg))

    def check(self):
        """Check data dependencies.
        Method does not return anything, it only adds errors messages to self.errors.
        """
        for rule in self._extract_rules():
            self._handel_rule(rule)

    def is_valid(self):
        """Check if data in schema are correct.

        :returns: check result
        :rtype: bool

        """
        if self.no_of_column != len(self._raw_data):
            self.errors.append(u'Line %d: Wrong number of columns (%d). The correct number is %d.' %
                               (self.line_no, len(self._raw_data), self.no_of_column))
            return False
        self._prepare_data()
        if not self.errors:
            self.check()
        return not bool(self.errors)
