"""other SymbolDict's features feature tests."""
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
import sys

scenario = partial(scenario, '../features/other_symboldict.feature')


@scenario('Empty symboldict creation')
def test_empty_symboldict_creation():
    """Empty symboldict creation."""


@scenario('Getvalue try load each rule does load')
def test_getvalue_try_load_each_rule_does_load():
    """Getvalue try load each rule does load."""


@scenario('Getvalue try load each rule does not reload')
def test_getvalue_try_load_each_rule_does_not_reload():
    """Getvalue try load each rule does not reload."""


@scenario('Getvalue try load each rule tries after failure')
def test_getvalue_try_load_each_rule_tries_after_failure():
    """Getvalue try load each rule tries after failure."""


@scenario('Getvalue try load once rule does not reload')
def test_getvalue_try_load_once_rule_does_not_reload():
    """Getvalue try load once rule does not reload."""


@scenario('Getvalue try load once rule tries only once')
def test_getvalue_try_load_once_rule_tries_only_once():
    """Getvalue try load once rule tries only once."""


@scenario('Getvalue w dont load rule does not import module')
def test_getvalue_w_dont_load_rule_does_not_import_module():
    """Getvalue w dont load rule does not import module."""


@scenario('Getvalue w force reload rule refetches value')
def test_getvalue_w_force_reload_rule_refetches_value():
    """Getvalue w force reload rule refetches value."""


@scenario('Getvalue wo rule does not reload')
def test_getvalue_wo_rule_does_not_reload():
    """Getvalue wo rule does not reload."""


@scenario('Getvalue wo rule tries only once')
def test_getvalue_wo_rule_tries_only_once():
    """Getvalue wo rule tries only once."""


@scenario('Hasvalue try load each rule does load')
def test_hasvalue_try_load_each_rule_does_load():
    """Hasvalue try load each rule does load."""


@scenario('Hasvalue try load each rule does not reload')
def test_hasvalue_try_load_each_rule_does_not_reload():
    """Hasvalue try load each rule does not reload."""


@scenario('Hasvalue try load each rule tries after failure')
def test_hasvalue_try_load_each_rule_tries_after_failure():
    """Hasvalue try load each rule tries after failure."""


@scenario('Hasvalue try load once rule does not reload')
def test_hasvalue_try_load_once_rule_does_not_reload():
    """Hasvalue try load once rule does not reload."""


@scenario('Hasvalue try load once rule tries only once')
def test_hasvalue_try_load_once_rule_tries_only_once():
    """Hasvalue try load once rule tries only once."""


@scenario('Hasvalue w dont load rule does not import module')
def test_hasvalue_w_dont_load_rule_does_not_import_module():
    """Hasvalue w dont load rule does not import module."""


@scenario('Hasvalue w force reload rule refetches value')
def test_hasvalue_w_force_reload_rule_refetches_value():
    """Hasvalue w force reload rule refetches value."""


@scenario('Hasvalue wo rule does not reload')
def test_hasvalue_wo_rule_does_not_reload():
    """Hasvalue wo rule does not reload."""


@scenario('Hasvalue wo rule tries only once')
def test_hasvalue_wo_rule_tries_only_once():
    """Hasvalue wo rule tries only once."""


@scenario('Setdefault with existing key')
def test_setdefault_with_existing_key():
    """Setdefault with existing key."""


@scenario('Setdefault with non existing key')
def test_setdefault_with_non_existing_key():
    """Setdefault with non existing key."""


@scenario('Symboldict checks existing values')
def test_symboldict_checks_existing_values():
    """Symboldict checks existing values."""


@scenario('Symboldict checks non existing values')
def test_symboldict_checks_non_existing_values():
    """Symboldict checks non existing values."""


@scenario('Symboldict creation')
def test_symboldict_creation():
    """Symboldict creation."""


@scenario('Symboldict fetches existing values')
def test_symboldict_fetches_existing_values():
    """Symboldict fetches existing values."""


@scenario('Symboldict reports non existing values')
def test_symboldict_reports_non_existing_values():
    """Symboldict reports non existing values."""


@scenario('Update method works and converts to symbol')
def test_update_method_works_and_converts_to_symbol():
    """Update method works and converts to symbol."""


@given('empty symboldict')
def empty_symboldict(self):
    """empty symboldict."""
    self.dic = sd.SymbolDict()
    return self

@given('example sd')
@given('non empty sd')
def example_sd():
    """example sd."""
    return sd.SymbolDict(
        isfile='os.path.isfile',
        whatisthis='sys.module',
        newyork='new.york.city',
        )


@given('list of 2 pairs key value')
def list_of_2_pairs_key_value(self):
    """list of 2 pairs key value."""
    self.pairs = [('u', 'uu'), ('v', 'vv')]
    return self.pairs


@given('list of 3 pairs key value')
def list_of_3_pairs_key_value(self):
    """list of 3 pairs key value."""
    self.pairs = [
            ('aa', 'abracadabra'),
            ('bb', 'bycicle.wheel'),
            ('cc', 'common.creative')]
    return self.pairs

@given('namespace')
def self():
    """self."""
    return type(str('Namespace'), (object,), {})()



@given('sd pointing to Telnet')
def sd_pointing_to_telnet():
    """sd pointing to Telnet."""
    return sd.SymbolDict(
        gnu='emacs',
        Telnet='telnetlib.Telnet',
        linux='free',
        )

@given('sd pointing to Telnet with value')
def sd_pointing_to_telnet_with_value():
    """sd pointing to Telnet with value."""
    s = sd_pointing_to_telnet()
    s.Telnet
    return s

@given('sd pointing to Telnet without value')
def sd_pointing_to_telnet_without_value():
    """sd pointing to Telnet without value."""
    s = sd_pointing_to_telnet()
    return s

@given('sd pointing to bad eggs symbol in telnetlib')
@given('sd pointing to non existing symbols')
def sd_w_bad_eggs_symbol(self):
    """sd pointing to bad eggs symbol in telnetlib."""
    self.dic = sd.SymbolDict(
        gnu='richard',
        eggs='telnetlib.eggs',
        linux='linus',
        )
    return self.dic


@given('sd pointing to stdlib symbols')
def sd_pointing_to_stdlib_symbols(self):
    """sd pointing to stdlib symbols."""
    self.dic = sd.SymbolDict(
        version='sys.version_info',
        executable='sys.executable',
        )
    self.symbols = ('version', 'executable')
    return self.dic

@given('telnetlib forced out sys modules')
def telnetlib_forced_out_sys_modules():
    """telnetlib forced out sys modules."""
    sys.modules.pop('telnetlib', None)


@when('getvalue rule dont load fails')
def getvalue_rule_dont_load_fails(sd_pointing_to_telnet):
    """getvalue rule dont load fails."""
    with pytest.raises(sd.VoidValueError):
        sd_pointing_to_telnet.getvalue(
            'Telnet', sd.Rule.DONT_LOAD)


@when('getvalue rule force reload is called')
def getvalue_rule_force_reload_is_called(
    sd_pointing_to_telnet_with_value):
    """getvalue rule force reload is called."""
    sd_pointing_to_telnet_with_value.getvalue(
        'Telnet', sd.Rule.FORCE_RELOAD)
    

@when('getvalue rule try load each fails')
def getvalue_rule_try_load_each_fails(
    sd_w_bad_eggs_symbol):
    """getvalue rule try load each fails."""
    with pytest.raises(Exception):
        sd_w_bad_eggs_symbol.getvalue(
            'eggs', sd.Rule.TRY_LOAD_EACH)


@when('getvalue rule try load each is called')
def getvalue_rule_try_load_each_is_called(
    sd_pointing_to_telnet_with_value):
    """getvalue rule try load each is called."""
    sd_pointing_to_telnet_with_value.getvalue(
        'Telnet', sd.Rule.TRY_LOAD_EACH)


@when('getvalue rule try load each is called 2')
def getvalue_rule_try_load_each_is_called_2(
    sd_pointing_to_telnet_without_value):
    """getvalue rule try load each is called."""
    sd_pointing_to_telnet_without_value.getvalue(
        'Telnet', sd.Rule.TRY_LOAD_EACH)
    

@when('getvalue rule try load once fails')
def getvalue_rule_try_load_once_fails(
    sd_w_bad_eggs_symbol):
    """getvalue rule try load once fails."""
    with pytest.raises(Exception):
        sd_w_bad_eggs_symbol.getvalue(
            'eggs', sd.Rule.TRY_LOAD_ONCE)

@when('getvalue rule try load once is called')
def getvalue_rule_try_load_once_is_called(
    sd_pointing_to_telnet_with_value):
    """getvalue rule try load once is called."""
    sd_pointing_to_telnet_with_value.getvalue(
        'Telnet', sd.Rule.TRY_LOAD_ONCE)

@when('getvalue wo rule fails')
def getvalue_wo_rule_fails(
    sd_w_bad_eggs_symbol):
    """getvalue wo rule fails."""
    with pytest.raises(Exception):
        sd_w_bad_eggs_symbol.getvalue('eggs')

@when('getvalue wo rule is called')
def getvalue_wo_rule_is_called(
    sd_pointing_to_telnet_with_value):
    """getvalue wo rule is called."""
    sd_pointing_to_telnet_with_value.getvalue('Telnet')

@when('hasvalue rule dont load is called')
def hasvalue_rule_dont_load_is_called(
    sd_pointing_to_telnet):
    """hasvalue rule dont load is called."""
    sd_pointing_to_telnet.hasvalue(
        'Telnet', sd.Rule.DONT_LOAD)

@when('hasvalue rule force reload is called')
def hasvalue_rule_force_reload_is_called(
    sd_pointing_to_telnet_with_value):
    """hasvalue rule force reload is called."""
    sd_pointing_to_telnet_with_value.getvalue(
        'Telnet', sd.Rule.FORCE_RELOAD)

@when('hasvalue rule try load each is called 3')
def hasvalue_rule_try_load_each_is_called_3(
    sd_w_bad_eggs_symbol):
    """hasvalue rule try load each is called 3."""
    sd_w_bad_eggs_symbol.hasvalue(
        'eggs', sd.Rule.TRY_LOAD_EACH)

@when('hasvalue rule try load each is called')
def hasvalue_rule_try_load_each_is_called(
    sd_pointing_to_telnet_with_value):
    """hasvalue rule try load each is called."""
    sd_pointing_to_telnet_with_value.hasvalue(
        'Telnet', sd.Rule.TRY_LOAD_EACH)

@when('hasvalue rule try load each is called 2')
def hasvalue_rule_try_load_each_is_called(
    sd_pointing_to_telnet_without_value):
    """hasvalue rule try load each is called."""
    sd_pointing_to_telnet_without_value.hasvalue(
        'Telnet', sd.Rule.TRY_LOAD_EACH)

@when('hasvalue rule try load once is called 3')
def hasvalue_rule_try_load_once_is_called_3(
    sd_w_bad_eggs_symbol):
    """hasvalue rule try load once is called 3."""
    sd_w_bad_eggs_symbol.hasvalue(
        'eggs', sd.Rule.TRY_LOAD_ONCE)

@when('hasvalue rule try load once is called')
def hasvalue_rule_try_load_once_is_called(
    sd_pointing_to_telnet_with_value):
    """hasvalue rule try load once is called."""
    sd_pointing_to_telnet_with_value.hasvalue(
        'eggs', sd.Rule.TRY_LOAD_ONCE)

@when('hasvalue wo rule is called 3')
def hasvalue_wo_rule_is_called_3(
    sd_w_bad_eggs_symbol):
    """hasvalue wo rule is called 3."""
    sd_w_bad_eggs_symbol.hasvalue('eggs')

@when('hasvalue wo rule is called')
def hasvalue_wo_rule_is_called(
    sd_pointing_to_telnet_with_value):
    """hasvalue wo rule is called."""
    sd_pointing_to_telnet_with_value.hasvalue(
        'Telnet')
    

@when('sd is updated with <method>')
def sd_is_updated_with_method(self, example_sd, method):
    """sd is updated with <method>."""
    if method == 'dict':
        example_sd.update(dict(self.pairs))
    elif method == 'sequence':
        example_sd.update(self.pairs)
    elif method == 'kwargs':
        example_sd.update(**dict(self.pairs))
    else:
        raise RuntimeError('Invalid <method> in test')


@when('setdefault is called on existing key')
def setdefault_is_called_on_existing_key(self, example_sd):
    """setdefault is called on existing key."""
    self.result = example_sd.setdefault('newyork', None)


@when('setdefault is called on non existing key')
def setdefault_is_called_on_non_existing_key(self, example_sd):
    """setdefault is called on non existing key."""
    self.pair = ('nonexisting', 'non.existing')
    self.result = example_sd.setdefault(*self.pair)

@when('symboldict is created by <method>')
def symboldict_is_created_by_method(self, method):
    """symboldict is created by <method>."""
    if method == 'dict':
        self.dic = sd.SymbolDict(dict(self.pairs))
    elif method == 'sequence':
        self.dic = sd.SymbolDict(self.pairs)
    elif method == 'kwargs':
        self.dic = sd.SymbolDict(**dict(self.pairs))
    else:
        raise RuntimeError('Bad <method> in test')


@when('telnetlib is removed from sys modules')
def telnetlib_is_removed_from_sys_modules():
    """telnetlib is removed from sys modules."""
    del sys.modules['telnetlib']


@when('these symbols are accessed by <method>')
def these_symbols_are_accessed_by_method(self, method):
    """these symbols are accessed by <method>."""
    self.result = res = {}
    if method == 'attribute':
        res['version'] = self.dic.version
        res['executable'] = self.dic.executable
    elif method == 'getvalue':
        res['version'] = self.dic.getvalue('version')
        res['executable'] = self.dic.getvalue('executable')
    else:
        raise RuntimeError(('Bad <method>', method, 'in test'))


@then('accessing by <method> raises exception')
def accessing_by_method_raises_exception(self, method):
    """accessing by <method> raises exception."""
    dic = self.dic
    if method == 'attribute':
        with pytest.raises(Exception):
            dic.eggs
    elif method == 'getvalue':
        with pytest.raises(Exception):
            dic.getvalue('eggs')
    else:
        raise RuntimeError(('Bad <method>', method, 'in test'))


@then('all values are symbol instances')
def all_values_are_symbol_instances(self):
    """all values are symbol instances."""
    assert all(isinstance(v, sd.Symbol)
               for v in self.dic.values())


@then('existing value is returned')
def existing_value_is_returned(self, example_sd):
    """existing value is returned."""
    self.result is example_sd['newyork']


@then('hasvalue returns false for these symbols')
def hasvalue_returns_false_for_these_symbols(self):
    """hasvalue returns false for these symbols."""
    assert self.dic.hasvalue('eggs') is False


@then('hasvalue returns true for these symbols')
def hasvalue_returns_true_for_these_symbols(self):
    """hasvalue returns true for these symbols."""
    assert self.dic.hasvalue('version') is True
    assert self.dic.hasvalue('executable') is True


@then('key is inserted in sd')
def key_is_inserted_in_sd(self, example_sd):
    """key is inserted in sd."""
    k, v = self.pair
    assert k in example_sd


@then('keys are inserted in sd')
def keys_are_inserted_in_sd(self, example_sd):
    """keys are inserted in sd."""
    for k, v in self.pairs:
        assert k in example_sd


@then('sd boolean value is False')
def sd_boolean_value_is_false(self):
    """sd boolean value is False."""
    assert bool(self.dic) is False


@then('sd has length 0')
def sd_has_length_0(self):
    """sd has length 0."""
    assert len(self.dic) == 0


@then('sd is dict instance')
def sd_is_dict_instance(self):
    """sd is dict instance."""
    assert isinstance(self.dic, dict)


@then('stdlib values are properly fetched')
def stdlib_values_are_properly_fetched(self):
    """stdlib values are properly fetched."""
    from sys import version_info, executable
    assert self.result['version'] is version_info
    assert self.result['executable'] is executable


@then('symboldict has length 3')
def symboldict_has_length_3(self):
    """symboldict has length 3."""
    assert len(self.dic) == 3


@then('symboldict has required keys')
def symboldict_has_required_keys(self):
    """symboldict has required keys."""
    assert all(k in self.dic for (k, v) in self.pairs)


@then('telnetlib is in sys modules')
def telnetlib_is_in_sys_modules():
    """telnetlib is in sys modules."""
    assert 'telnetlib' in sys.modules


@then('telnetlib is not in sys modules')
def telnetlib_is_not_in_sys_modules():
    """telnetlib is not in sys modules."""
    assert 'telnetlib' not in sys.modules

@then('value is default converted to symbol')
def value_is_default_converted_to_symbol(self, example_sd):
    """value is default converted to symbol."""
    k, v = self.pair
    assert example_sd[k] == sd.Symbol(v)


@then('values are converted to symbol')
def values_are_converted_to_symbol(self, example_sd):
    """values are converted to symbol."""
    for k, v in self.pairs:
        assert example_sd[k] == sd.Symbol(v)
