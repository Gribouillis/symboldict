#!/usr/bin/env python
# -*-coding: utf8-*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
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

def test_symbol_ctor_accepts_several_args(sd):
    s = sd.Symbol('spam', 'ham', 'eggs')
    assert isinstance(s, sd.Symbol)
    assert str(s) == 'spam.ham.eggs'
    
def test_symbol_ctor_accepts_empty_arglist(sd):
    s = sd.Symbol()
    assert isinstance(s, sd.Symbol)
    assert str(s) == ''
    
def test_symbol_ctor_converts_args_to_str(sd):
    s = sd.Symbol(None, dir)
    assert str(s) == 'None.<built-in function dir>'
    
def test_dot_overload_creates_new_symbol(sd):
    s = sd.Symbol('spam').ham
    assert str(s) == 'spam.ham'
    s = s.eggs
    assert isinstance(s, sd.Symbol)
    assert str(s) == 'spam.ham.eggs'
    
def test_cannot_set_attribute_on_symbol(sd):
    s = sd.Symbol('').eggs.ham
    with pytest.raises(TypeError):
        s.eggs = 'eggs'
    with pytest.raises(TypeError):
        s._path = 'eggs'

def test_symbol_to_string_conversion_return_symbol_path(sd):
    s = sd.Symbol('').spam.ham
    assert str(s) == s().path()

def test_symbol_equality_operator(sd):
    s = sd.Symbol('Spam.Ham.Eggs')
    t = sd.Symbol().Spam.Ham.Eggs
    assert s == t
    assert s != 'Spam.Ham.Eggs'
    assert s != sd.Symbol('Eggs')

def test_symbol_total_ordering(sd):
    def ok(a, b):
        return sum([a < b, a == b, a > b]) == 1
    s, t = sd.Symbol('Spam'), sd.Symbol('Eggs')
    assert ok(s, t)
    assert ok(s, 1)
    assert ok(s, None)
    assert ok(s, ['spam', 'ham'])
    
def test_symbol_is_hashable_type(sd):
    s = sd.Symbol('eggs').ham.spam.eggs
    t = s.eggs
    hash(s)
    f = set([s, 1])
    assert s in f
    e = set([1, 2, s, None, t, ('spam', 'ham')])
    assert s in e
    assert t in e
    
def test_list_with_symbols_is_sortable(sd):
     # could be removed, mixed comparison is not python3-ish
    s = sd.Symbol('eggs').ham.spam.eggs
    t = s.eggs
    L = sorted([1, 2, s, t, 3])
    assert s in L
    assert t in L
    
def test_symbol_getvalue_retrieves_value(sd):
    from telnetlib import Telnet
    assert sd.Symbol('telnetlib.Telnet')().getvalue() is Telnet
    with pytest.raises(Exception):
        sd.Symbol('telnetlib.spam')().getvalue()
        
def test_symbol_hasvalue_checks_value(sd):
    assert sd.Symbol('socket.socket')().hasvalue() == True
    assert sd.Symbol('socket.spam')().hasvalue() == False

def test_symbol_call_method_return_value(sd):
    s = sd.Symbol('spam.ham')
    c = s()
    assert isinstance(c, sd.SymbolControl)
    assert c.symbol() is s
    assert c.path() == str(s)

def test_symbol_root_instance_exists(sd):
    assert sd.symbol == sd.Symbol('')

# getvalue() and rule

def test_rule_getvalue_dont_load(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    with pytest.raises(Exception):
        s().getvalue(rule=sd.Rule.DONT_LOAD)
    assert s().hasvalue(rule=sd.Rule.DONT_LOAD) == False
    assert 'telnetlib' not in sys.modules
    
def test_rule_getvalue_force_reload(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    assert s().getvalue(rule=sd.Rule.FORCE_RELOAD) is not None
    del sys.modules['telnetlib']  # must be key
    assert s().getvalue(rule=sd.Rule.FORCE_RELOAD) is not None
    del sys.modules['telnetlib']  # must be key

def test_rule_getvalue_try_load_each(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Spam')
    with pytest.raises(Exception):
        s().getvalue(rule=sd.Rule.TRY_LOAD_EACH)
    del sys.modules['telnetlib']  # must be key
    with pytest.raises(Exception):
        s().getvalue(rule=sd.Rule.TRY_LOAD_EACH)
    del sys.modules['telnetlib']  # must be key
    s = sd.Symbol('telnetlib.Telnet')
    assert s().getvalue(rule=sd.Rule.TRY_LOAD_EACH) is not None
    del sys.modules['telnetlib']  # must be key
    assert s().getvalue(rule=sd.Rule.TRY_LOAD_EACH) is not None
    assert 'telnetlib' not in sys.modules  # must be key

def test_rule_getvalue_try_load_once(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Spam')
    with pytest.raises(Exception):
        s().getvalue(rule=sd.Rule.TRY_LOAD_ONCE)
    del sys.modules['telnetlib']  # must be key
    with pytest.raises(Exception):
        s().getvalue(rule=sd.Rule.TRY_LOAD_ONCE)
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    assert s().getvalue(rule=sd.Rule.TRY_LOAD_ONCE) is not None
    del sys.modules['telnetlib']  # must be key
    assert s().getvalue(rule=sd.Rule.TRY_LOAD_ONCE) is not None
    assert 'telnetlib' not in sys.modules

def test_rule_getvalue_try_load_norule_is_once(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Spam')
    with pytest.raises(Exception):
        s().getvalue()
    del sys.modules['telnetlib']  # must be key
    with pytest.raises(Exception):
        s().getvalue()
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    assert s().getvalue() is not None
    del sys.modules['telnetlib']  # must be key
    assert s().getvalue() is not None
    assert 'telnetlib' not in sys.modules

# hasvalue() and rule


def test_rule_hasvalue_dont_load(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    assert s().hasvalue(rule=sd.Rule.DONT_LOAD) is False
    assert 'telnetlib' not in sys.modules
    
def test_rule_hasvalue_force_reload(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    assert s().hasvalue(rule=sd.Rule.FORCE_RELOAD) is True
    del sys.modules['telnetlib']  # must be key
    assert s().hasvalue(rule=sd.Rule.FORCE_RELOAD) is True
    del sys.modules['telnetlib']  # must be key

def test_rule_hasvalue_try_load_each(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Spam')
    assert  s().hasvalue(rule=sd.Rule.TRY_LOAD_EACH) is False
    del sys.modules['telnetlib']  # must be key
    assert s().hasvalue(rule=sd.Rule.TRY_LOAD_EACH) is False
    del sys.modules['telnetlib']  # must be key
    s = sd.Symbol('telnetlib.Telnet')
    assert s().hasvalue(rule=sd.Rule.TRY_LOAD_EACH) is True
    del sys.modules['telnetlib']  # must be key
    assert s().hasvalue(rule=sd.Rule.TRY_LOAD_EACH) is True
    assert 'telnetlib' not in sys.modules  # must be key

def test_rule_hasvalue_try_load_once(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Spam')
    assert s().hasvalue(rule=sd.Rule.TRY_LOAD_ONCE) is False
    del sys.modules['telnetlib']  # must be key
    assert s().hasvalue(rule=sd.Rule.TRY_LOAD_ONCE) is False
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    assert s().hasvalue(rule=sd.Rule.TRY_LOAD_ONCE) is True
    del sys.modules['telnetlib']  # must be key
    assert s().hasvalue(rule=sd.Rule.TRY_LOAD_ONCE) is True
    assert 'telnetlib' not in sys.modules

def test_rule_hasvalue_try_load_norule_is_once(sd, notelnetlib):
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Spam')
    assert s().hasvalue() is False
    del sys.modules['telnetlib']  # must be key
    assert s().hasvalue() is False
    assert 'telnetlib' not in sys.modules
    s = sd.Symbol('telnetlib.Telnet')
    assert s().hasvalue() is True
    del sys.modules['telnetlib']  # must be key
    assert s().hasvalue() is True
    assert 'telnetlib' not in sys.modules
