# -*- coding: utf-8 -*-

import unittest

from csv_schema.structure.base import BaseCsvStructure
from csv_schema.structure.set import Cs
from csv_schema.columns import (
    IntColumn,
    DecimalColumn,
    StringColumn,
)


class CsTest(unittest.TestCase):

    """Column set tests."""

    def test_at_least_one_rule(self):
        tmp = Cs('a')|Cs('b')

        self.assertEqual(tmp({'a': '', 'b':''}), False)
        self.assertEqual(tmp({'a': 'TEST', 'b':''}), True)
        self.assertEqual(tmp({'a': '', 'b':'TEST'}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'TEST'}), True)

    def test_only_one_rule(self):
        tmp = Cs('a')^Cs('b')

        self.assertEqual(tmp({'a': '', 'b':''}), False)
        self.assertEqual(tmp({'a': 'TEST', 'b':''}), True)
        self.assertEqual(tmp({'a': '', 'b':'TEST'}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'TEST'}), False)

    def test_mixed_rules(self):
        tmp = Cs('a')|Cs('b')^Cs('c')

        self.assertEqual(tmp({'a': '', 'b':'', 'c': ''}), False)
        self.assertEqual(tmp({'a': 'TEST', 'b':'', 'c': ''}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'TEST', 'c': ''}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'TEST', 'c': 'TEST'}), True)
        self.assertEqual(tmp({'a': '', 'b':'TEST', 'c': 'TEST'}), False)
        self.assertEqual(tmp({'a': '', 'b':'', 'c': 'TEST'}), True)
        self.assertEqual(tmp({'a': '', 'b':'TEST', 'c': ''}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'', 'c': 'TEST'}), True)

    def test_diffrent_operators_order_mixed_rules(self):
        tmp = (Cs('a')|Cs('b'))^Cs('c')

        self.assertEqual(tmp({'a': '', 'b':'', 'c': ''}), False)
        self.assertEqual(tmp({'a': 'TEST', 'b':'', 'c': ''}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'TEST', 'c': ''}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'TEST', 'c': 'TEST'}), False)
        self.assertEqual(tmp({'a': '', 'b':'TEST', 'c': 'TEST'}), False)
        self.assertEqual(tmp({'a': '', 'b':'', 'c': 'TEST'}), True)
        self.assertEqual(tmp({'a': '', 'b':'TEST', 'c': ''}), True)
        self.assertEqual(tmp({'a': 'TEST', 'b':'', 'c': 'TEST'}), False)

    def test_expected_values_logic(self):
        tmp = Cs('a', b='TEST')

        self.assertEqual(tmp({'a': '', 'b':''}), True)
        self.assertEqual(tmp({'a': 'A', 'b':''}), False)
        self.assertEqual(tmp({'a': '', 'b':'TEST'}), False)
        self.assertEqual(tmp({'a': 'A', 'b':'TEST'}), True)

    def test_expected_values_with_operator(self):
        tmp = Cs('a', a='OK')|Cs('b')

        self.assertEqual(tmp({'a': '', 'b':''}), True)
        self.assertEqual(tmp({'a': 'OK', 'b':''}), True)
        self.assertEqual(tmp({'a': 'NOT OK', 'b':''}), False)
        self.assertEqual(tmp({'a': '', 'b':'TEST'}), True)
        self.assertEqual(tmp({'a': 'OK', 'b':'TEST'}), True)
        self.assertEqual(tmp({'a': 'NOT OK', 'b':'TEST'}), True)

    def test_multiple_columns(self):
        tmp = Cs('a', 'b', 'c')

        self.assertEqual(tmp({'a': '', 'b': '', 'c': ''}), False)
        self.assertEqual(tmp({'a': '', 'b': 'OK', 'c': ''}), False)
        self.assertEqual(tmp({'a': '', 'b': '', 'c': 'OK'}), False)
        self.assertEqual(tmp({'a': 'OK', 'b': '', 'c': ''}), False)
        self.assertEqual(tmp({'a': 'OK', 'b': 'OK', 'c': ''}), False)
        self.assertEqual(tmp({'a': 'OK', 'b': 'OK', 'c': 'OK'}), True)

    def test_complex_execution_order(self):
        tmp = Cs('e')|((Cs('a')|Cs('b'))^Cs('d'))|Cs('c')
        tmp_exe_order = ' '.join([str(obj) for obj in tmp.exe_order])
        self.assertEqual(tmp_exe_order, "('e',) ('a',) ('b',) | ('d',) ^ | ('c',) |")


class BasicUseCaseTest(unittest.TestCase):

    class TestCsvStructure(BaseCsvStructure):

        no_of_things = IntColumn()
        no_of_other_things = IntColumn(blank=True, min_inclusive=100, max_exclusive=300)
        frequency = DecimalColumn(total_digits=3, fraction_digits=2)

    def test_full_data_set(self):
        csv_structure = self.TestCsvStructure(['100', '132', '2.1'], 6)
        self.assertEqual(csv_structure.is_valid(), True)

    def test_required_only_data_set(self):
        csv_structure = self.TestCsvStructure(['100', '', '1.23'], 6)
        self.assertEqual(csv_structure.is_valid(), True)

    def test_wrong_data_set(self):
        csv_structure = self.TestCsvStructure(['100', 'LOL', '123.12'], 6)
        self.assertEqual(csv_structure.is_valid(), False)

    def test_wrong_value_range(self):
        csv_structure = self.TestCsvStructure(['3', '300', '1.321'], 6)
        self.assertEqual(csv_structure.is_valid(), False)
        self.assertEqual(len(csv_structure.errors), 2)


class BasicStringUseTestCase(unittest.TestCase):

    class TestStringCsvStructure(BaseCsvStructure):

        name = StringColumn(blank=True)
        last_name = StringColumn(min_length=3, max_length=30)
        is_programer = StringColumn(permissible_values=['yes', 'no'])

    def test_full_data_set(self):
        csv_structure = self.TestStringCsvStructure(['Han', 'Solo', 'no'], 6)
        self.assertEqual(csv_structure.is_valid(), True)

    def test_required_only_data_set(self):
        csv_structure = self.TestStringCsvStructure(['', 'Solo', 'no'], 6)
        self.assertEqual(csv_structure.is_valid(), True)

    def test_wrong_data_set(self):
        csv_structure = self.TestStringCsvStructure(['Han', ' ', 'shot first'], 6)
        self.assertEqual(csv_structure.is_valid(), False)
        self.assertEqual(len(csv_structure.errors), 2)


class CsUseTestCase(unittest.TestCase):

    class TestCsvStructure(BaseCsvStructure):

        a = StringColumn(blank=True)
        b = IntColumn(blank=True)
        c = DecimalColumn(blank=True)

        class Rules(object):
            rule_1 = (Cs('a')|Cs('b')).error('A or B')
            rule_2 = Cs('c', b=87)

    def test_good_data(self):
        csv_structure = self.TestCsvStructure(['A', '', ''], 1)
        self.assertEqual(csv_structure.is_valid(), True)

    def test_rule_breaking_data(self):
        csv_structure = self.TestCsvStructure(['', '87', ''], 1)
        self.assertEqual(csv_structure.is_valid(), False)
        self.assertEqual(len(csv_structure.errors), 1)

    def test_custom_rule_error_msg(self):
        csv_structure = self.TestCsvStructure(['', '', ''], 1)
        self.assertEqual(csv_structure.is_valid(), False)
        self.assertEqual(len(csv_structure.errors), 1)
        self.assertEqual(csv_structure.errors[0], 'Line 1: A or B')

if __name__ == '__main__':
    unittest.main()
