"""other Symbol's features feature tests."""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from functools import partial
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
import os
import pytest
import symboldict as sd
Symbol = sd.Symbol
import sys

scenario = partial(scenario, '../features/other_symbol.feature')


@scenario('Attribute setting is forbidden')
def test_attribute_setting_is_forbidden():
    """Attribute setting is forbidden."""


@scenario('Call method returns symbolcontrol instance')
def test_call_method_returns_symbolcontrol_instance():
    """Call method returns symbolcontrol instance."""


@scenario('Create empty symbol')
def test_create_empty_symbol():
    """Create empty symbol."""


@scenario('Create symbol from arglist')
def test_create_symbol_from_arglist():
    """Create symbol from arglist."""


@scenario('Getvalue method raises on non existing path')
def test_getvalue_method_raises_on_non_existing_path():
    """Getvalue method raises on non existing path."""


@scenario('Getvalue method retrieves value')
def test_getvalue_method_retrieves_value():
    """Getvalue method retrieves value."""


@scenario('Hasvalue method succeeds if value does not exist')
def test_hasvalue_method_succeeds_if_value_does_not_exist():
    """Hasvalue method succeeds if value does not exist."""


@scenario('Hasvalue method succeeds if value exists')
def test_hasvalue_method_succeeds_if_value_exists():
    """Hasvalue method succeeds if value exists."""


@scenario('Symbol attribute access returns new symbol')
def test_symbol_attribute_access_returns_new_symbol():
    """Symbol attribute access returns new symbol."""


@scenario('Symbol constructor converts args to str')
def test_symbol_constructor_converts_args_to_str():
    """Symbol constructor converts args to str."""


@scenario('Symbols are hashable')
def test_symbols_are_hashable():
    """Symbols are hashable."""


@scenario('Symbols are richly ordered')
def test_symbols_are_richly_ordered():
    """Symbols are richly ordered."""


@scenario('Symbols with different path are different')
def test_symbols_with_different_path_are_different():
    """Symbols with different path are different."""


@scenario('Symbols with same path are equal')
def test_symbols_with_same_path_are_equal():
    """Symbols with same path are equal."""


@scenario('getvalue w rule dont load doesnt load')
def test_getvalue_w_rule_dont_load_doesnt_load():
    """getvalue w rule dont load doesnt load."""


@scenario('getvalue w rule each does try twice')
def test_getvalue_w_rule_each_does_try_twice():
    """getvalue w rule each does try twice."""


@scenario('getvalue w rule force reload does reload')
def test_getvalue_w_rule_force_reload_does_reload():
    """getvalue w rule force reload does reload."""


@scenario('getvalue w rule once doesnt try twice')
def test_getvalue_w_rule_once_doesnt_try_twice():
    """getvalue w rule once doesnt try twice."""


@scenario('getvalue with rule each doesnt reload')
def test_getvalue_with_rule_each_doesnt_reload():
    """getvalue with rule each doesnt reload."""


@scenario('getvalue with rule once doesnt reload')
def test_getvalue_with_rule_once_doesnt_reload():
    """getvalue with rule once doesnt reload."""


@scenario('getvalue wo rule doesnt reload')
def test_getvalue_wo_rule_doesnt_reload():
    """getvalue wo rule doesnt reload."""


@scenario('getvalue wo rule doesnt try twice')
def test_getvalue_wo_rule_doesnt_try_twice():
    """getvalue wo rule doesnt try twice."""


@scenario('hasvalue w rule dont load doesnt load')
def test_hasvalue_w_rule_dont_load_doesnt_load():
    """hasvalue w rule dont load doesnt load."""


@scenario('hasvalue w rule each does try twice')
def test_hasvalue_w_rule_each_does_try_twice():
    """hasvalue w rule each does try twice."""


@scenario('hasvalue w rule force reload does reload')
def test_hasvalue_w_rule_force_reload_does_reload():
    """hasvalue w rule force reload does reload."""


@scenario('hasvalue w rule once doesnt try twice')
def test_hasvalue_w_rule_once_doesnt_try_twice():
    """hasvalue w rule once doesnt try twice."""


@scenario('hasvalue with rule each doesnt reload')
def test_hasvalue_with_rule_each_doesnt_reload():
    """hasvalue with rule each doesnt reload."""


@scenario('hasvalue with rule once doesnt reload')
def test_hasvalue_with_rule_once_doesnt_reload():
    """hasvalue with rule once doesnt reload."""


@scenario('hasvalue wo rule doesnt reload')
def test_hasvalue_wo_rule_doesnt_reload():
    """hasvalue wo rule doesnt reload."""


@scenario('hasvalue wo rule doesnt try twice')
def test_hasvalue_wo_rule_doesnt_try_twice():
    """hasvalue wo rule doesnt try twice."""


@given('2 non trivial symbol')
@given('2 symbols with different path')
def non_trivial_symbol(self):
    """2 non trivial symbol."""
    a, b = Symbol('os.path.isfile'), Symbol('sys.executable')
    self.symbs = [a, b]
    return self.symbs

@given('2 symbols with same path')
def symbols_with_same_path(self):
    """2 symbols with same path."""
    a, b = Symbol('spam.ham.eggs'), Symbol().spam.ham.eggs
    self.symbs = [a, b]
    return self.symbs

@given('argument list of several words')
def argument_list_of_several_words(self):
    """argument list of several words."""
    self.arglist = ['eggs', 'spam', 'ham']
    return self.arglist


@given('argument list of various types')
def argument_list_of_various_types(self):
    """argument list of various types."""
    self.arglist = [1, None, 'sys.executable',
                    Symbol('spam').ham, {'a':'b'}]
    return self.arglist

@given('non trivial symbol')
@given('example symbol')
def example_symbol(self):
    """example symbol."""
    self.symb = Symbol('hello.world.from.here')
    return self.symb


@given('list of various objects among which symbol')
def list_of_various_objects_among_which_symbol(self):
    """list of various objects among which symbol."""
    self.arglist = [1, Symbol('os.path.isdir'), 
                    'sys.executable',
                    Symbol('spam').ham, {'a':'b'}]
    return self.arglist

@given('namespace')
def self():
    """namespace."""
    return type(str('Namespace'), (object,), {})()


@given('symbol ctor return value')
def symbol_ctor_return_value(self):
    """symbol ctor return value."""
    self.symb = Symbol()
    return self.symb


@given('symbol w path to Telnet')
def symbol_w_path_to_telnet(self):
    """symbol w path to Telnet."""
    self.symb = Symbol('telnetlib.Telnet')
    return self.symb


@given('symbol w path to Telnet and value')
def symbol_w_path_to_telnet_and_value(self):
    """symbol w path to Telnet and value."""
    self.symb = Symbol('telnetlib.Telnet')
    self.symb().getvalue()
    return self.symb

@given('symbol w path to spam in telnetlib')
def symbol_w_path_to_spam_in_telnetlib(self):
    """symbol w path to spam in telnetlib."""
    self.symb = Symbol('telnetlib.spam')
    return self.symb

@given('telnetlib forced out of sys modules')
def telnetlib_forced_out_of_sys_modules():
    """telnetlib forced out of sys modules."""
    sys.modules.pop('telnetlib', None)


@when('attribute ham and eggs are taken')
def attribute_ham_and_eggs_are_taken(self):
    """attribute ham and eggs are taken."""
    self.result = self.symb.ham.eggs


@when('call method is called')
def call_method_is_called(self):
    """call method is called."""
    self.result = self.symb()


@when('calling getvalue w rule once fails')
def calling_getvalue_w_rule_once_fails(self):
    """calling getvalue w rule once fails."""
    with pytest.raises(Exception):
        self.symb().getvalue(rule=sd.Rule.TRY_LOAD_ONCE)

@when('calling getvalue w rule try load each fails')
def calling_getvalue_w_rule_try_load_each_fails(self):
    """calling getvalue w rule try load each fails."""
    with pytest.raises(Exception):
        self.symb().getvalue(rule=sd.Rule.TRY_LOAD_EACH)

@when('calling getvalue wo rule fails')
def calling_getvalue_wo_rule_fails():
    """calling getvalue wo rule fails."""
    with pytest.raises(Exception):
        self.symb().getvalue()

@when('calling hasvalue w rule once returns false')
def calling_hasvalue_w_rule_once_returns_false(self):
    """calling hasvalue w rule once returns false."""
    False is self.symb().hasvalue(rule=sd.Rule.TRY_LOAD_ONCE)


@when('calling hasvalue w rule try load each returns false')
def calling_hasvalue_w_rule_try_load_each_returns_false(self):
    """calling hasvalue w rule try load each returns false."""
    False is self.symb().hasvalue(rule=sd.Rule.TRY_LOAD_EACH)

@when('calling hasvalue wo rule returns false')
def calling_hasvalue_wo_rule_returns_false(self):
    """calling hasvalue wo rule returns false."""
    False is self.symb().hasvalue()

@when('getvalue fails w rule dont load')
def getvalue_fails_w_rule_dont_load(self):
    """getvalue fails w rule dont load."""
    with pytest.raises(Exception):
        self.symb().getvalue(sd.Rule.DONT_LOAD)


@when('getvalue is called with rule force reload')
def getvalue_is_called_with_rule_force_reload(self):
    """getvalue is called with rule force reload."""
    self.result = self.symb().getvalue(sd.Rule.FORCE_RELOAD)

@when('getvalue is called with rule once')
def getvalue_is_called_with_rule_once(self):
    """getvalue is called with rule once."""
    self.result = self.symb().getvalue(sd.Rule.TRY_LOAD_ONCE)

@when('getvalue is called with rule try load each')
def getvalue_is_called_with_rule_try_load_each(self):
    """getvalue is called with rule try load each."""
    self.result = self.symb().getvalue(sd.Rule.TRY_LOAD_EACH)

@when('getvalue is called wo rule')
def getvalue_is_called_wo_rule(self):
    """getvalue is called wo rule."""
    self.result = self.symb().getvalue()


@when('getvalue method is called')
def getvalue_method_is_called(self):
    """getvalue method is called."""
    self.result = self.symb().getvalue()


@when('hasvalue called w rule dont load returns false')
def hasvalue_called_w_rule_dont_load_returns_false(self):
    """hasvalue called w rule dont load returns false."""
    False is self.symb().hasvalue(rule=sd.Rule.DONT_LOAD)


@when('hasvalue called with rule force reload returns true')
def hasvalue_called_with_rule_force_reload_returns_true(self):
    """hasvalue called with rule force reload returns true."""
    True is self.symb().hasvalue(rule=sd.Rule.FORCE_RELOAD)

@when('hasvalue called with rule once returns true')
def hasvalue_called_with_rule_once_returns_true(self):
    """hasvalue called with rule once returns true."""
    True is self.symb().hasvalue(rule=sd.Rule.TRY_LOAD_ONCE)


@when('hasvalue called with rule try load each returns true')
def hasvalue_called_with_rule_try_load_each_returns_true(self):
    """hasvalue called with rule try load each returns true."""
    True is self.symb().hasvalue(rule=sd.Rule.TRY_LOAD_EACH)

@when('hasvalue called wo rule returns true')
def hasvalue_called_wo_rule_returns_true(self):
    """hasvalue called wo rule returns true."""
    True is self.symb().hasvalue()


@when('set is created containing these symbols')
def set_is_created_containing_these_symbols(self):
    """set is created containing these symbols."""
    self.set = set(self.symbs)


@when('symbol is created from list')
def symbol_is_created_from_list(self):
    """symbol is created from list."""
    self.symb = Symbol(*self.arglist)


@then('symbol str is dot join of args converted to str')
def symbol_str_is_dot_join_of_args_converted_to_str(self):
    """symbol str is dot join of args converted to str."""
    assert str(self.symb) == ".".join(str(x) for x in self.arglist)

@when('telnetlib is removed from sys modules')
def telnetlib_is_removed_from_sys_modules():
    """telnetlib is removed from sys modules."""
    sys.modules.pop('telnetlib', None)


@then('both symbols belong to set')
def both_symbols_belong_to_set(self):
    """both symbols belong to set."""
    assert all(s in self.set for s in self.symbs)


@then('calling getvalue raises exception')
def calling_getvalue_raises_exception(self):
    """calling getvalue raises exception."""
    with pytest.raises(Exception):
        self.symb().getvalue()


@then('each object has one comparison true among lt eq gt')
def each_object_has_one_comparison_true_among_lt_eq_gt(self):
    """each object has one comparison true among lt eq gt."""
    s = self.symb
    for x in self.arglist:
        assert sum([x < s, x == s, x > s]) == 1

@then('hasvalue method returns False')
def hasvalue_method_returns_false(self):
    """hasvalue method returns False."""
    assert False == self.symb().hasvalue()


@then('hasvalue method returns True')
def hasvalue_method_returns_true(self):
    """hasvalue method returns True."""
    assert True == self.symb().hasvalue()

@then('result is a symbol instance')
def result_is_a_symbol_instance(self):
    """result is a symbol instance."""
    assert isinstance(self.symb, Symbol)

@then('result is stdlib Telnet object')
def result_is_stdlib_telnet_object(self):
    """result is stdlib Telnet object."""
    import telnetlib
    assert self.result is telnetlib.Telnet


@then('result is symbol instance')
def result_is_symbol_instance(self):
    """result is symbol instance."""
    assert isinstance(self.result, Symbol)


@then('return value is a symbolcontrol instance')
def return_value_is_a_symbolcontrol_instance(self):
    """return value is a symbolcontrol instance."""
    assert isinstance(self.result, sd.SymbolControl)


@then('setting attribute ham raises typeerror')
def setting_attribute_ham_raises_typeerror(self):
    """setting attribute ham raises typeerror."""
    with pytest.raises(TypeError):
        self.symb.ham = 'eggs'


@then('setting hidden attribute raises typeerror')
def setting_hidden_attribute_raises_typeerror(self):
    """setting hidden attribute raises typeerror."""
    self.hidden = Symbol.__slots__[0]
    with pytest.raises(TypeError):
        setattr(self.symb, self.hidden, 'eggs')

@then('symbol str is appended said attributes')
def symbol_str_is_appended_said_attributes(self):
    """symbol str is appended said attributes."""
    assert str(self.symb) + ".ham.eggs" == str(self.result)


@then('symbol str is dot join of list')
def symbol_str_is_dot_join_of_list(self):
    """symbol str is dot join of list."""
    assert str(self.symb) == '.'.join(self.arglist)


@then('symbol str is empty string')
def symbol_str_is_empty_string(self):
    """symbol str is empty string."""
    assert str(self.symb) == ''


@then('symbolcontrol path method returns str of symbol')
def symbolcontrol_path_method_returns_str_of_symbol(self):
    """symbolcontrol path method returns str of symbol."""
    assert self.result.path() == str(self.symb)


@then('symbolcontrol symbol method returns example symbol')
def symbolcontrol_symbol_method_returns_example_symbol(self):
    """symbolcontrol symbol method returns example symbol."""
    assert self.result.symbol() is self.symb


@then('telnetlib is in sys modules')
def telnetlib_is_in_sys_modules():
    """telnetlib is in sys modules."""
    assert 'telnetlib' in sys.modules


@then('telnetlib is not in sys modules')
def telnetlib_is_not_in_sys_modules():
    """telnetlib is not in sys modules."""
    assert 'telnetlib' not in sys.modules


@then('these 2 symbols are different')
def these_2_symbols_are_different(self):
    """these 2 symbols are different."""
    a, b = self.symbs
    assert a != b


@then('these 2 symbols are equal')
def these_2_symbols_are_equal(self):
    """these 2 symbols are equal."""
    a, b = self.symbs
    assert a == b


@then('value is symbol instance')
def value_is_symbol_instance(self):
    """value is symbol instance."""
    assert isinstance(self.symb, Symbol)

