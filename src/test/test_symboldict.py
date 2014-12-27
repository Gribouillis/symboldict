#!/usr/bin/env python
# -*-coding: utf8-*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import pytest
import sys

__doc__ = '''
'''

@pytest.fixture(scope='session')
def sd():
    import symboldict
    return symboldict

@pytest.fixture(scope="function")
def notelnetlib(request):
    mod = sys.modules.get('telnetlib', None)
    if mod is not None:
        del sys.modules['telnetlib']
    def fin():
        if mod is not None:
            sys.modules['telnetlib'] = mod
    request.addfinalizer(fin)

@pytest.fixture(scope='function')
def sye(sd):
    return sd.SymbolDict(isfile='os.path.isfile', Telnet='telnetlib.Telnet',
                       conju='complex.conjugate', eggs='telnetlib.eggs')
    
def test_empty_ctor_symboldict(sd):
    sy = sd.SymbolDict()
    assert isinstance(sy, sd.SymbolDict)
    assert len(sy) == 0
    assert not sy
    
def test_ctor_mapping_arg_symboldict(sd):
    D = dict(isfile='os.path.isfile', Telnet='telnetlib.Telnet', conju='complex.conjugate')
    sy = sd.SymbolDict(D)
    assert isinstance(sy, sd.SymbolDict)
    assert len(sy) == 3
    assert set(sy.keys()) == set(D.keys())

def test_ctor_iterable_arg_symboldict(sd):
    L = [('isfile', 'os.path.isfile'), ('Telnet', 'telnetlib.Telnet'), ('conju', 'complex.conjugate')]
    sy = sd.SymbolDict(L)
    assert isinstance(sy, sd.SymbolDict)
    assert len(sy) == 3
    assert set(x[0] for x in L) == set(sy.keys())

def test_ctor_kwargs_symboldict(sd):
    sy = sd.SymbolDict(isfile='os.path.isfile', Telnet='telnetlib.Telnet', conju='complex.conjugate')
    assert isinstance(sy, sd.SymbolDict)
    assert len(sy) == 3
    assert set(sy.keys()) == set(['isfile', 'Telnet', 'conju'])
    
def test_symboldict_subclasses_dict(sd):
    assert issubclass(sd.SymbolDict, dict)
    sy = sd.SymbolDict()
    assert isinstance(sy, dict)

def test_dot_overload_symboldict(sd, sye):
    assert sye.conju is complex.conjugate
    assert sye.isfile is os.path.isfile
    with pytest.raises(Exception):
        sye.eggs

def test_getvalue_fetches_value_symboldict(sd, sye):
    assert sye().getvalue('conju') is complex.conjugate
    assert sye().getvalue('isfile') is os.path.isfile
    with pytest.raises(Exception):
        sye().getvalue('eggs')

def test_hasvalue_checks_value_symboldict(sd, sye):
    assert sye().hasvalue('conju') is True
    assert sye().hasvalue('isfile') is True
    assert sye().hasvalue('eggs') is False

def test_call_symboldict_return_value(sd, sye):
    assert isinstance(sye(), sd.SymbolDictControl)
    assert sye().symboldict() is sye

def test_symboldict_setdefault_method(sd, sye):
    assert sye.setdefault('conju', 'os.path') == sd.Symbol('complex.conjugate')
    assert sye.setdefault('spam', 'os.path') == sd.Symbol('os.path')
    assert 'spam' in sye

def test_update_symboldict(sd):
    sy = sd.SymbolDict()
    E1 = [('u', 'uu'), ('v', 'vv')]
    E2 = dict(w='ww', x='xx')
    sy.update(E1, y='yy')
    Symbol = sd.Symbol
    assert set(sy.items()) == set([('u', Symbol('uu')), ('v', Symbol('vv')), ('y', Symbol('yy'))])
    sy.update(E2, z='zz')
    assert set(sy.items()) == set([('u', Symbol('uu')), ('v', Symbol('vv')), ('y', Symbol('yy')),
                                   ('w', Symbol('ww')), ('x', Symbol('xx')), ('z', Symbol('zz'))])


# getvalue() and rule

def test_rule_getvalue_dont_load(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    with pytest.raises(Exception):
        sye().getvalue('Telnet', rule=sd.Rule.DONT_LOAD)
    assert 'telnetlib' not in sys.modules
    
def test_rule_getvalue_force_reload(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    assert sye().getvalue('Telnet', rule=sd.Rule.FORCE_RELOAD) is not None
    del sys.modules['telnetlib']  # must be key
    assert sye().getvalue('Telnet', rule=sd.Rule.FORCE_RELOAD) is not None
    del sys.modules['telnetlib']  # must be key

def test_rule_getvalue_try_load_each(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    with pytest.raises(Exception):
        sye().getvalue('eggs', rule=sd.Rule.TRY_LOAD_EACH)
    del sys.modules['telnetlib']  # must be key
    with pytest.raises(Exception):
        sye().getvalue('eggs', rule=sd.Rule.TRY_LOAD_EACH)
    del sys.modules['telnetlib']  # must be key
    assert sye().getvalue('Telnet', rule=sd.Rule.TRY_LOAD_EACH) is not None
    del sys.modules['telnetlib']  # must be key
    assert sye().getvalue('Telnet', rule=sd.Rule.TRY_LOAD_EACH) is not None
    assert 'telnetlib' not in sys.modules  # must be key

def test_rule_getvalue_try_load_once(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    with pytest.raises(Exception):
        sye().getvalue('eggs', rule=sd.Rule.TRY_LOAD_ONCE)
    del sys.modules['telnetlib']  # must be key
    with pytest.raises(Exception):
        sye().getvalue('eggs', rule=sd.Rule.TRY_LOAD_ONCE)
    assert 'telnetlib' not in sys.modules
    assert sye().getvalue('Telnet', rule=sd.Rule.TRY_LOAD_ONCE) is not None
    del sys.modules['telnetlib']  # must be key
    assert sye().getvalue('Telnet', rule=sd.Rule.TRY_LOAD_ONCE) is not None
    assert 'telnetlib' not in sys.modules

def test_rule_getvalue_try_load_norule_is_once(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    with pytest.raises(Exception):
        sye().getvalue('eggs')
    del sys.modules['telnetlib']  # must be key
    with pytest.raises(Exception):
        sye().getvalue('eggs')
    assert 'telnetlib' not in sys.modules
    assert sye().getvalue('Telnet') is not None
    del sys.modules['telnetlib']  # must be key
    assert sye().getvalue('Telnet') is not None
    assert 'telnetlib' not in sys.modules

# hasvalue() and rule


def test_rule_hasvalue_dont_load(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    assert sye().hasvalue('Telnet', rule=sd.Rule.DONT_LOAD) is False
    assert 'telnetlib' not in sys.modules
    
def test_rule_hasvalue_force_reload(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    assert sye().hasvalue('Telnet', rule=sd.Rule.FORCE_RELOAD) is True
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('Telnet', rule=sd.Rule.FORCE_RELOAD) is True
    del sys.modules['telnetlib']  # must be key

def test_rule_hasvalue_try_load_each(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    assert  sye().hasvalue('eggs', rule=sd.Rule.TRY_LOAD_EACH) is False
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('eggs', rule=sd.Rule.TRY_LOAD_EACH) is False
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('Telnet', rule=sd.Rule.TRY_LOAD_EACH) is True
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('Telnet', rule=sd.Rule.TRY_LOAD_EACH) is True
    assert 'telnetlib' not in sys.modules  # must be key

def test_rule_hasvalue_try_load_once(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    assert sye().hasvalue('eggs', rule=sd.Rule.TRY_LOAD_ONCE) is False
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('eggs', rule=sd.Rule.TRY_LOAD_ONCE) is False
    assert 'telnetlib' not in sys.modules
    assert sye().hasvalue('Telnet', rule=sd.Rule.TRY_LOAD_ONCE) is True
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('Telnet', rule=sd.Rule.TRY_LOAD_ONCE) is True
    assert 'telnetlib' not in sys.modules

def test_rule_hasvalue_try_load_norule_is_once(sd, notelnetlib, sye):
    assert 'telnetlib' not in sys.modules
    assert sye().hasvalue('eggs') is False
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('eggs') is False
    assert 'telnetlib' not in sys.modules
    assert sye().hasvalue('Telnet') is True
    del sys.modules['telnetlib']  # must be key
    assert sye().hasvalue('Telnet') is True
    assert 'telnetlib' not in sys.modules
