# -*- coding: utf-8 -*-

"""Modul containing utility used in describing simple dependencies between columns."""

__all__ = ['Cs']


class _Rule(object):

    """Basic rule object."""

    def check(self, caller_eval_result, arg_eval_result):
        """Execute rule check. 

        :param caller_eval_result: first argument of the operator 
        :type caller_eval_result: bool
        :param arg_eval_result: second argument of the operator 
        :type arg_eval_result: bool
        :returns: check result
        :rtype: bool

        """
        raise NotImplementedError


class _AtLeastOneRule(_Rule):

    """Rule that demands at least one Cs filled properly."""

    def __str__(self):
        return '|'

    def check(self, caller_eval_result, arg_eval_result):
        return caller_eval_result or arg_eval_result


class _OnlyOneRule(_Rule):

    """Rule that demands only one Cs filled properly."""

    def __str__(self):
        return '^'

    def check(self, caller_eval_result, arg_eval_result):
        return caller_eval_result ^ arg_eval_result


class Cs(object):

    """Column set."""

    def __init__(self, *args, **kwargs):
        self.exe_order = []
        self.columns_in_set = args
        self.expected_values = kwargs
        self.error_msg = u'Values does not meet validation rules'

    def __str__(self):
        return str(self.columns_in_set)

    def __call__(self, col_data):
        return self._call_exe_order(col_data) if self.exe_order else self.estimate(col_data)

    def _call_exe_order(self, col_data):
        """Do stored expression.

        :param col_data: cleaned data assigned to each column
        :type col_data: dict
        :returns: expression result
        :rtype: bool

        """
        exe_stack = []
        for obj in self.exe_order:
            if isinstance(obj, _Rule):
                self._perform_operation(obj, exe_stack, col_data)
            else:
                exe_stack.append(obj)
        return exe_stack[0]

    def __or__(self, other_cs):
        self._set_operation(_AtLeastOneRule(), other_cs)
        return self

    def __xor__(self, other_cs):
        self._set_operation(_OnlyOneRule(), other_cs)
        return self

    def _update_exe_order(self, order_obj, op_obj):
        """Update internal execution order.

        :param order_obj: can by other execution list or single object
        :type order_obj: list or csv_schema.structure.set.Cs

        """
        if type(order_obj) is list:
            self.exe_order.extend(order_obj)
        else:
            self.exe_order.append(order_obj)
        self.exe_order.append(op_obj)

    def _set_operation(self, op_obj, other_cs):
        """Add new element to execution order.

        :param op_obj: rule operator
        :type ob_obj: csv_schema.structure.set._Rule
        :param other_cs: operator attribute
        :type other_cs: csv_schema.structure.set.Cs

        """
        order_obj = other_cs.exe_order if other_cs.exe_order else other_cs
        if not self.exe_order:
            self.exe_order.append(self)
        self._update_exe_order(order_obj, op_obj)

    def _perform_operation(self, op_obj, exe_stack, col_data):
        """Perform operation and append result to execution stack.

        :param op_obj: rule operator
        :type op_obj: csv_schema.structure.set._Rule
        :param exe_stack: current execution stack
        :type exe_stack: list
        :param col_data: cleaned data assigned to each column
        :type col_data: dict

        """
        value = lambda e, d: e.estimate(d) if isinstance(e, self.__class__) else e

        second_arg = value(exe_stack.pop(), col_data)
        first_arg = value(exe_stack.pop(), col_data)
        exe_stack.append(op_obj.check(first_arg, second_arg))

    def _check_expected_values(self, col_data):
        """Look into columns data and check if they have proper values.

        :param col_data: cleaned data assigned to each column
        :type col_data: dict
        :returns: True if all values are equal, False if at least one is wrong
        :rtype: bool

        """
        for key, value in self.expected_values.items():
            if col_data[key] != value:
                return False
        return True

    def _check_if_set_filled(self, col_data):
        """Check if all columns in set are filled.

        :param col_data: cleaned data assigned to each column
        :type col_data: dict
        :returns: True if all columns are filled, False if atleast one is not
        :rtype: bool

        """
        for col_name in self.columns_in_set:
            if col_data[col_name] in ['', u'', None]:
                return False
        return True

    def estimate(self, col_data):
        """Compute value of this column set.

        :param col_data: cleaned data assigned to each column
        :type col_data: dict
        :returns: True if all columns are filled and have proper values, False if not
        :rtype: bool

        """
        if self.expected_values:
            if self._check_expected_values(col_data):
                return self._check_if_set_filled(col_data)
            else:
                return not self._check_if_set_filled(col_data)
        else:
            return self._check_if_set_filled(col_data)

    def error(self, error_msg):
        """Override default error message.

        :param error_msg: new error message
        :type error_msg: basestring
        :returns: self, method is chainable
        :rtype: 

        """
        self.error_msg = error_msg
        return self
