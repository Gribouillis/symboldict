"""Strict and non strict symboldict feature tests."""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from functools import partial
import pytest
from pytest_bdd import (
    given,
    scenario,
    then,
    when,
)
import symboldict as sd

scenario = partial(scenario, '../features/strict.feature')


@scenario('Attributes of SymbolDict types are allowed keys in non strict symboldict')
def test_attributes_of_symboldict_types_are_allowed_keys_in_non_strict_symboldict():
    """Attributes of SymbolDict types are allowed keys in non strict symboldict."""


@scenario('Attributes of SymbolDict types are forbidden keys in strict symboldict')
def test_attributes_of_symboldict_types_are_forbidden_keys_in_strict_symboldict():
    """Attributes of SymbolDict types are forbidden keys in strict symboldict."""


@scenario('Check strictness of new symboldict')
def test_check_strictness_of_new_symboldict():
    """Check strictness of new symboldict."""


@scenario('Creating strict symboldict from dict having forbidden key raises TypeError')
def test_creating_strict_symboldict_from_dict_having_forbidden_key_raises_typeerror():
    """Creating strict symboldict from dict having forbidden key raises TypeError."""


@scenario('Creating strict symboldict from sequence having forbidden item raises TypeError')
def test_creating_strict_symboldict_from_sequence_having_forbidden_item_raises_typeerror():
    """Creating strict symboldict from sequence having forbidden item raises TypeError."""


@scenario('Forbidden key setting raise TypeError in strict symboldict')
def test_forbidden_key_setting_raise_typeerror_in_strict_symboldict(strict_symboldict):
    """Forbidden key setting raise TypeError in strict symboldict."""
    with pytest.raises(TypeError):
        strict_symboldict['update'] = 'sys.version_info'


@scenario('Setting symboldict strict raises TypeError if there is forbidden key')
def test_setting_symboldict_strict_raises_typeerror_if_there_is_forbidden_key():
    """Setting symboldict strict raises TypeError if there is forbidden key."""


@scenario('Updating strict symboldict from sequence having forbidden item raises TypeError')
def test_updating_strict_symboldict_from_sequence_having_forbidden_item_raises_typeerror():
    """Updating strict symboldict from sequence having forbidden item raises TypeError."""


@scenario('Updating strict symboldict with dict having forbidden key raises TypeError')
def test_updating_strict_symboldict_with_dict_having_forbidden_key_raises_typeerror():
    """Updating strict symboldict with dict having forbidden key raises TypeError."""


@given('dict containing forbidden key')
def dict_containing_forbidden_key():
    """dict containing forbidden key."""


@given('new <how> symboldict')
def new_how_symboldict(how):
    """new <how> symboldict."""
    if how == 'empty':
        return sd.SymbolDict()
    else:
        return sd.SymbolDict(isfile='os.path.isfile', Telnet='telnetlib.Telnet',
            conju='complex.conjugate', eggs='telnetlib.eggs')


@given('non strict symboldict')
def non_strict_symboldict():
    """non strict symboldict."""
    return sd.LaxSymbolDict()


@given('sequence of items containing forbidden key')
def sequence_of_items_containing_forbidden_key():
    """sequence of items containing forbidden key."""
    return [('strict', 'indeed'),]


@given('strict symboldict')
def strict_symboldict():
    """strict symboldict."""
    return sd.SymbolDict()


@given('symboldict containing forbidden key')
def symboldict_containing_forbidden_key():
    """symboldict containing forbidden key."""
    return sd.LaxSymbolDict(values = 'dict.values')


@then('all attributes of SymbolDict type are allowed keys in symboldict')
def all_attributes_of_symboldict_type_are_allowed_keys_in_symboldict(non_strict_symboldict):
    """all attributes of SymbolDict type are allowed keys in symboldict."""
    for key in dir(sd.SymbolDict):
        non_strict_symboldict[key] = 'sys.version_info'


@then('creating strict symboldict from dict raises TypeError')
def creating_strict_symboldict_from_dict_raises_typeerror(dict_containing_forbidden_key):
    """creating strict symboldict from dict raises TypeError."""
    with pytest.raises(TypeError):
        sd.SymbolDict(dict_containing_forbidden_key)


@then('creating strict symboldict from sequence raises TypeError')
def creating_strict_symboldict_from_sequence_raises_typeerror(
    sequence_of_items_containing_forbidden_key):
    """creating strict symboldict from sequence raises TypeError."""
    with pytest.raises(TypeError):
        sd.SymbolDict(sequence_of_items_containing_forbidden_key)


@then('every attribute of SymbolDict type is forbidden key in symboldict')
def every_attribute_of_symboldict_type_is_forbidden_key_in_symboldict(strict_symboldict):
    """every attribute of SymbolDict type is forbidden key in symboldict."""
    s = sd.Symbol('sys.executable')
    for key in dir(sd.SymbolDict):
        with pytest.raises(TypeError):
            strict_symboldict[key] = s


@then('setting symboldict item with forbidden key raises TypeError')
def setting_symboldict_item_with_forbidden_key_raises_typeerror():
    """setting symboldict item with forbidden key raises TypeError."""


@then('setting symboldict strict raises TypeError')
def setting_symboldict_strict_raises_typeerror(symboldict_containing_forbidden_key):
    """setting symboldict strict raises TypeError."""
    with pytest.raises(TypeError):
        symboldict_containing_forbidden_key.strict = True

@then('symboldict is strict')
def symboldict_is_strict(new_how_symboldict):
    """symboldict is strict."""
    assert new_how_symboldict.strict


@then('updating symboldict from sequence raises TypeError')
def updating_symboldict_from_sequence_raises_typeerror(
    strict_symboldict, sequence_of_items_containing_forbidden_key):
    """updating symboldict from sequence raises TypeError."""
    with pytest.raises(TypeError):
        strict_symboldict.update(sequence_of_items_containing_forbidden_key)


@then('updating symboldict with dict raises TypeError')
def updating_symboldict_with_dict_raises_typeerror(
    strict_symboldict, dict_containing_forbidden_key):
    """updating symboldict with dict raises TypeError."""
    with pytest.raises(TypeError):
        strict_symboldict.update(dict_containing_forbidden_key)

