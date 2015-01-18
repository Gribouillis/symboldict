#!/usr/bin/env python
# -*-coding: utf8-*-
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
import symboldict as sd

@given('non empty symboldict having existing symbol path')
def sd_with_existing_path():
    """non empty symboldict having existing symbol path."""
    return sd.SymbolDict(isfile='os.path.isfile')


@given('non empty symboldict with existing attribute proxy')
def sd_with_existing_proxy():
    """non empty symboldict with existing attribute proxy."""
    d = sd.SymbolDict(isfile='os.path.isfile')
    d.isfile
    return d

@given('non empty symboldict with several attribute proxies')
def sd_with_several_proxies():
    """non empty symboldict with several attribute proxies."""
    d = sd.SymbolDict(
        a='os.path.isfile', b='sys.executable',
        c='sys.platform', d='sys.modules')
    (d.a, d.b, d.c) # creates the proxies
    return d

@when('the path is accessed through symboldict <method>')
def the_path_is_accessed_through_symboldict_method(
    sd_with_existing_path, method):
    """the path is accessed through symboldict <method>."""
    if method == 'attribute':
        sd_with_existing_path.isfile
    elif method == 'getvalue':
        sd_with_existing_path.getvalue('isfile')
    elif method == 'hasvalue':
        sd_with_existing_path.hasvalue('isfile')
    else:
        raise ValueError('Invalid method value in test')


@when('this key is deleted from symboldict')
def this_key_is_deleted_from_symboldict(sd_with_existing_proxy):
    """this key is deleted from symboldict."""
    del sd_with_existing_proxy['isfile']


@when('this key is reset to symbol')
def this_key_is_reset_to_symbol(sd_with_existing_proxy):
    """this key is reset to symbol."""
    #print("KEY RESET (when)")
    sd_with_existing_proxy['isfile'] = sd.Symbol('sys.version_info')


@when('this symboldict is cleared')
def this_symboldict_is_cleared(sd_with_several_proxies):
    """this symboldict is cleared."""
    sd_with_several_proxies.clear()


@when('this symboldict is updated from <what>')
def this_symboldict_is_updated_from_what(sd_with_several_proxies, what):
    """this symboldict is updated from <what>."""
    d = dict(b='os.path.isdir', c='sys.prefix')
    if what == 'dict':
        sd_with_several_proxies.update(d)
    elif what == 'sequence':
        sd_with_several_proxies.update(list(d.items()))
    elif what == 'kwargs':
        sd_with_several_proxies.update(**d)
    else:
        raise RuntimeError('Invalid choice in test')

@then('Examples vertical:')
def examples_vertical():
    """Examples vertical:."""


@then('all attribute proxies are deleted from symboldict')
def all_attribute_proxies_are_deleted_from_symboldict(sd_with_several_proxies):
    """all attribute proxies are deleted from symboldict."""
    len(sd_with_several_proxies.__dict__) == 0

@then('attribute proxy is deleted from symboldict')
def attribute_proxy_is_deleted_from_symboldict(
    sd_with_existing_proxy):
    """attribute proxy is deleted from symboldict."""
    assert 'isfile' not in sd_with_existing_proxy.__dict__


@then('corresponding attribute proxies are deleted from symboldict')
def corresponding_attribute_proxies_are_deleted_from_symboldict():
    """corresponding attribute proxies are deleted from symboldict."""
    assert all(x not in sd_with_existing_path.__dict__ for x in ('b', 'c'))


@then('the symboldict instance has given key and value in its dict')
def the_symboldict_instance_has_given_key_and_value_in_its_dict(
    sd_with_existing_path):
    """the symboldict instance has given key and value in its dict."""
    d = sd_with_existing_path.__dict__
    assert 'isfile' in d
    assert d['isfile'] is os.path.isfile

@then('| method | attribute | getvalue | hasvalue |')
def _method__attribute__getvalue__hasvalue_():
    """| method | attribute | getvalue | hasvalue |."""
