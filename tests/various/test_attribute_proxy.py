"""Attribute proxy in SymbolDict feature tests."""
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

scenario = partial(scenario, '../features/attribute_proxy.feature')


@scenario('Clearing symboldict deletes attribute proxies')
def test_clearing_symboldict_deletes_attribute_proxies():
    """Clearing symboldict deletes attribute proxies."""


@scenario('Deleting item in symboldict deletes attribute proxy')
def test_deleting_item_in_symboldict_deletes_attribute_proxy():
    """Deleting item in symboldict deletes attribute proxy."""


@scenario('Setting item in symboldict deletes attribute proxy')
def test_setting_item_in_symboldict_deletes_attribute_proxy():
    """Setting item in symboldict deletes attribute proxy."""


@scenario('Successful symbol access in symboldict installs attribute proxy',
          example_converters=dict(method=str))
def test_successful_symbol_access_in_symboldict_installs_attribute_proxy():
    """Successful symbol access in symboldict installs attribute proxy."""


@scenario('Updating symboldict deletes corresponding attribute proxies')
def test_updating_symboldict_deletes_corresponding_attribute_proxies():
    """Updating symboldict deletes corresponding attribute proxies."""

