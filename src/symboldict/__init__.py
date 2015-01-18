# -*-coding: utf8-*-
"""symboldict module
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import functools
from importlib import import_module
import sys
from .version import __version__
import warnings

def deprecated(func):
    '''This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.
    
    ref:
        https://wiki.python.org/moin/PythonDecoratorLibrary#Generating_Deprecation_Warnings
    '''
    @functools.wraps
    def new_func(*args, **kwargs):
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    return new_func

class VoidValueError(ValueError): pass

if sys.version_info < (3, 4):
    Enum = object
    _isrule = (0, 1, 2, 3).__contains__
else:
    from enum import Enum
    _isrule = lambda x: isinstance(x, Rule)

class Rule(Enum):
    """Enumerated rules for :meth:`SymbolControl.getvalue()`.
    
    The available values are
    
    Attributes:
        Rule.DONT_LOAD
        Rule.TRY_LOAD_ONCE
        Rule.TRY_LOAD_EACH
        Rule.FORCE_RELOAD
    """
    DONT_LOAD = 0
    TRY_LOAD_ONCE = 1
    TRY_LOAD_EACH = 2
    FORCE_RELOAD = 3
    
_DONT = Rule.DONT_LOAD
_EACH = Rule.TRY_LOAD_EACH
_FORCE = Rule.FORCE_RELOAD
_ONCE = Rule.TRY_LOAD_ONCE

_DOT = str('.')

class Symbol(object):
    """Symbol(*parts) -> new Symbol instance
    
    Args:
        parts(convertibles to str): A sequence of :class:`str` or objects
            convertible to :class:`str`. These strings are joined by :code:`'.'` to
            create the instance's path.
    
    Example:
        >>> Symbol('spam.ham', 'eggs')
        Symbol('spam.ham.eggs')
        >>> Symbol()
        Symbol('')
        >>> Symbol(None, 12)
        Symbol('None.12')
    
    This is the type of objects used as values in :class:`SymbolDict`
    instances. Their role is mainly to wrap a dot-separated path to a python
    object, which may exist or not, with a convenient interface.
    
    Example:
        >>> Symbol('os.path.isfile')
        >>> Symbol('telnetlib.Telnet')
        >>> Symbol('complex.conjugate')
    
    Defining an instance does *not* trigger an attempt to retrieve the
    indicated python object by importing modules or accessing attributes.
    This is the role of the :meth:`SymbolControl.getvalue` or
    :meth:`SymbolDict.__getattr__` methods.
    """
    __slots__ = ("_path", "_has", "_val")

    def __init__(self, *parts):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        parts = [str(x) for x in parts]
        s = _DOT.join(x for x in parts if x)
        _storpath(self, s)
        _storhas(self, False)
        _storval(self, False) # no failed load

    def __getattribute__(self, attr):
        """Overridden attribute access creates a new :class:`Symbol`.
        
        Args:
            attr(str): new path element
            
        Example:
            >>> Symbol('spam').eggs
            Symbol('spam.eggs')
        """
        return Symbol(Symbol._path.__get__(self), attr)

    def __call__(self):
        """Calling a :class:`Symbol` instance wraps it into a :class:`SymbolControl` object.
        
        Returns:
            SymbolControl: a lightweight object wrapping the :class:`Symbol`.
            
        This allows to bypass the overloading of the dot operator to
        access some methods.
        
        Example:
            >>> s = Symbol('os.path.isfile')
            >>> s().getvalue()
            <function isfile at ...>
            
        """
        return SymbolControl(self)

    def __setattr__(self, attr, value):
        """Attribute setting is disabled for :class:`Symbol` instances.
        
        Raises:
            TypeError: this exception is always raised.
            
        Example:
            >>> s = Symbol('spam')
            >>> s.ham = 'eggs'
            Traceback ...
            TypeError: Attribute setting is disabled for Symbol instances

        """
        raise TypeError('Attribute setting is disabled for Symbol instances')

    def __str__(self):
        """Converting a :class:`Symbol` to :class:`str` returns the wrapped path.
        
        Returns:
            str: the string stored in the Symbol instance.
        
        Example:
            >>> s = Symbol('spam.ham').eggs
            >>> s
            Symbol('spam.ham.eggs')
            >>> str(s)
            'spam.ham.eggs'
        """
        return _readpath(self)
        
        
    def __repr__(self):
        return "Symbol({})".format(repr(_readpath(self)))
    
    def __eq__(self, other):
        """Equality relation with another instance.
        
        A :class:`Symbol` :code:`x` is equal to a python object :code:`y` if
        they have the same type and the same path.
        
        Example:
            >>> x = Symbol('spam.ham')
            >>> y = Symbol('spam.ham')
            >>> x == y
            True
            >>> x == 'spam.ham'
            False
            
        The relations :code:`!=, <, >, <=, >=` are defined as well.
        """
        return (_cid(self) == _cid(other)) and (_readpath(self) == _readpath(other))
    def __ne__(self, other):
        return not (self == other)
    def __le__(self, other):
        return not (self > other)
    def __lt__(self, other):
        return (_cid(self) < _cid(other)) or (
            (_cid(self) == _cid(other)) and (_readpath(self) < _readpath(other)))
    def __ge__(self, other):
        return not (self < other)
    def __gt__(self, other):
        return (_cid(self) > _cid(other)) or (
            (_cid(self) == _cid(other)) and (_readpath(self) > _readpath(other)))
    def __hash__(self):
        """Computes a hash value for the Symbol instance.
        
        Returns:
            int: the instance's hash value
            
        :class:`Symbol` instances are hashable objects which
        can be used as dictionary keys or as set elements.
        
        Example:
            >>> S = set([Symbol('spam.ham'), Symbol('eggs')])
            >>> Symbol('eggs') in S
            True

        """
        return hash((_cid(self), _readpath(self)))

_readpath = Symbol._path.__get__
_storpath = Symbol._path.__set__
_readhas = Symbol._has.__get__
_storhas = Symbol._has.__set__
_readval = Symbol._val.__get__
_storval = Symbol._val.__set__

def _cid(obj):
    return id(type(obj)) # cannot use .__class__

symbol = Symbol()
"""An instance of :class:`Symbol` with empty path.

Used to build other Symbols by the means of attribute access.

Example:
    >>> symbol.spam.ham
    Symbol('spam.ham')
"""

def _getvalue(symb, rule):
    """Attempts to return the python object referenced symbolically by this instance.
    
    Args:
        rule(Rule): a rule specifying how to obtain the object's value.
        
    Returns:
        any: a python object referenced by this instance,
            if such a value can be found.
    
    Raises:
        Exception
            met while trying to
            obtain the value when it does not exist.
    
    see :meth:`SymbolControl.getvalue()` for description.
    """
    #    must fetch ?
    #            void    value    failed
    #    ONCE    ?        Rtn       Exc
    #    EACH    ?        Rtn       ?
    #    DONT    Exc      Rtn       Exc
    #    RELO    ?        ?         ?
    if _readhas(symb):
        if rule is _ONCE:
            return _readval(symb)
        elif rule is _DONT or rule is _EACH:
            return _readval(symb)
        # else fetch
    elif (rule is _ONCE and _readval(symb)) or (rule is _DONT):
        raise VoidValueError
    # else fetch
    # fetch starts here
    if not _isrule(rule): # check only when load is needed
        raise TypeError(('Need symboldict.Rule,', type(rule), 'found'))
    try:
        #... procedure -> v
        # we try to load
        L = _readpath(symb).split('.')
        acc = L[0]
        try:
            # may raise ValueError if s is empty string
            v = import_module(acc)
        except ImportError:
            # this section may raise AttributeError for example
            if acc in __builtins__:
                v = __builtins__[acc]
            else:
                raise
            for attr in L[1:]:
                v = getattr(v, attr)
        else:
            for attr in L[1:]:
                acc = acc + _DOT + attr
                try:
                    v = getattr(v, attr)
                except AttributeError:
                    v = import_module(acc)
    except Exception:
        _storhas(symb, False)
        _storval(symb, True) # FETCH FAILED
        raise
    else:
        _storhas(symb, True)
        _storval(symb, v)
        return v

class SymbolControl(object):
    """SymbolControl(symb) -> new SymbolControl instance
    
    Args:
        symb(Symbol): a symbol referenced by the SymbolControl object
        
    This is a class of lightweight wrappers around :class:`Symbol` instances
    used to bypass the overriding of the dot operator in this class.
    SymbolControl objects are returned by the :meth:`Symbol.__call__()`
    method. Their main purpose is to hold methods to manipulate Symbols.
    
    Example:
        >>> s = Symbol('os.path.isfile')
        >>> s()
        <symboldict.SymbolControl object ...>
        >>> s().hasvalue()
        True
        >>> s().path()
        'os.path.isfile'
        >>> s().getvalue()
        <function isfile ...>

    """
    __slots__ = ('__symb',)

    def __init__(self, symb):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        self.__symb = symb

    def hasvalue(self, rule=Rule.TRY_LOAD_ONCE):
        """Returns a boolean indicating if a value is available for the python object referenced symbolically by this instance.
        
        Args:
            rule(Rule): a rule specifying how to obtain the object's value.
                It defaults to ``Rule.TRY_LOAD_ONCE``.
                
        Returns:
            bool: a boolean indicating if a value is available for this instance.

        This method returns True if the corresponding call to :meth:`getvalue()`
        would succeed, and returns False if the call to :meth:`getvalue()` would
        fail. In any case, it does not raise an exception.
        
        The rule argument has the same meaning as in :meth:`Symbol.getvalue()`.
        
        Example:
            >>> a = Symbol('wave.Error')
            >>> a().hasvalue()
            True
            >>> b = Symbol('spam.ham')
            >>> b().hasvalue()
            False
        """
        try:
            _getvalue(self.__symb, rule)
        except Exception:
            return False
        else:
            return True

    def getvalue(self, rule=Rule.TRY_LOAD_ONCE):
        """Attempts to return the python object referenced symbolically by this instance.
        
        Args:
            rule(Rule): a rule specifying how to obtain the object's value.
                It defaults to ``Rule.TRY_LOAD_ONCE``.
            
        Returns:
            any: a python object referenced by this instance,
                if such a value can be found.
        
        Raises:
            Exception
                met while trying to
                obtain the value when it does not exist.
        
        This method tries to obtain a value by importing modules and taking
        attributes according to the dotted path of the contained :class:`Symbol`
        instance. In this path, the word before the first dot can be the
        name of an importable module or that of a builtin python object
        in the `__builtins__` dictionnary.
        
        If the object can not be  found, an exception is raised.
        
        Example:
            >>> a = Symbol('wave.Error')
            >>> a().getvalue()
            <class 'wave.Error'>
            
        The `rule` parameter can be used to specify the policy
        with respect to value search. The possible values are
        
        - ``Rule.TRY_LOAD_ONCE`` (default rule) The value
            is searched once and stored in the ``Symbol`` instance. Subsequent
            calls to ``getvalue()`` return the same value without trying
            to reload the symbol. If the first search fails, subsequent
            calls will fail without attempting to search the value.
            This rule handles most lazy import cases because symbol values
            in imported modules usually don't vary. For example there is
            no need to search the symbol ``Symbol('telnetlib.Telnet')``
            more than once. This is a per-instance policy, which means that
            a different instance with the same path will trigger a second search.
            
        - ``Rule.DONT_LOAD`` With this rule, there is no attempt to get
            the symbol's value through imports or attribute accesses. It
            means that the call will succeed only if a value was previously
            found by a call to ``getvalue()`` or ``hasvalue()`` with a different
            rule.
            
        - ``Rule.FORCE_RELOAD`` With this rule, an attempt is made to load
            the symbol through imports and attribute access. It can be used
            to handle cases where a variable changes in an imported module.
            There is no attempt to reload imported modules.
            
        - ``Rule.TRY_LOAD_EACH`` With this rule, an attempt is made to load
            the symbol's value only if the previous attempts failed
            to obtain a value.
        
        """
        return _getvalue(self.__symb, rule)
    
    def path(self):
        """Returns the path of the referenced :class:`Symbol` instance.
        
        Example:
            >>> s = Symbol('socket.socket')
            >>> s().path()
            'socket.socket'
        """
        return _readpath(self.__symb)
    
    def symbol(self):
        """Returns the referenced :class:`Symbol` instance.
        
        Example:
            >>> s = Symbol('socket.socket')
            >>> s().symbol() is s
            True
        """
        return self.__symb
    
_dictga = dict.__getitem__

class BaseSymbolDict(dict):
    __slots__ = ('_strict',)
    
    def __new__(cls, *args, **kwargs):
        instance = dict.__new__(cls)
        return instance
    
    def __init__(self, *args, **kwargs):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        dict.__init__(self)
        self._strict = True
        self.update(dict(*args, **kwargs))

class SymbolDict(BaseSymbolDict):
    """SymbolDict() -> new empty SymbolDict
    SymbolDict(mapping) -> new SymbolDict initiliazed from a mapping object's
        (key, value) pairs. The values are converted to Symbol instances.
    SymbolDict(iterable) -> new SymbolDict initialized as if via::
        d = SymbolDict()
        for k, v in iterable:
            d[k] = Symbol(v)
    SymbolDict(**kwargs) -> new SymbolDict initialized with the name=value pairs
        in the keyword argument list.  For example:  SymbolDict(one='spam.eggs', two='os').
        The values are converted to Symbol instances.
        
    SymbolDict is a subclass of :class:`dict`, which means that the usual
    dict methods (clear, copy, get, items, keys, pop, popitem, setdefault,
    update, values) apply. The main differences are
    
    - The dictionary values are :class:`Symbol` instances.
    - Attribute access is overridden to obtain the symbols values,
        see :meth:`SymbolDict.__getattr__()`.
    
    Example:
        >>> from symboldict import symbol, SymbolDict
        >>> sy = SymbolDict(
        ...     isfile=symbol.os.path.isfile,
        ...     Telnet=symbol.telnetlib.Telnet,
        ...     conju=symbol.complex.conjugate,
        ...     eggs=symbol.spam.eggs,
        ... )
        >>> sy['isfile']
        Symbol('os.path.isfile')
        >>> sy['eggs']
        Symbol('spam.eggs')
        >>> sy['Parser'] = Symbol('argparse.ArgumentParser')
        >>> 'Telnet' in sy
        True
        >>> sy.isfile
        <function isfile ...'>
        >>> sy.Telnet
        <class 'telnetlib.Telnet ...'>
        >>> sy.conju
        <method 'conjugate' of 'complex' objects>
        >>> sy.eggs
        Traceback ...
        ImportError: No module named spam
        >>> sy.hasvalue('isfile')
        True
        >>> sy.getvalue('Parser')
        <class 'argparse.ArgumentParser'>
        
    """

    @property
    def strict(self):
        return self._strict
    
    @strict.setter
    def strict(self, value):
        value = bool(value)
        if value and (not self._strict) and any(key in self for key in _reserved):
            raise TypeError('Invalid key for strict SymbolDict')
        self._strict = value
    
    def update(self, *args, **kwargs):
        """sy.update([E, ]**F) -> None. Update SymbolDict ``sy`` from dict/iterable E and F.
        - If E is present and has a .keys() method, then does: ``for k in E: sy[k] = Symbol(E[k])``
        - If E is present and lacks a .keys() method, then does: ``for k, v in E: sy[k] = Symbol(v)``
        - In either case, this is followed by: ``for k in F: sy[k] = Symbol(F[k])``
        
        The only difference with :meth:`dict.update()` is that values are converted
        to :class:`Symbol` instances.
        """
        d = dict()
        d.update(*args, **kwargs)
        if self.strict:
            if len(d) < len(_reserved):
                b = any(k in _reserved for k in d.keys())
            else:
                b = any(k in d for k in _reserved)
            if b:
                raise TypeError('Invalid key for strict SymbolDict')
        dict.update(self, [(k, Symbol(v)) for (k, v) in d.items()])
        
        
    def __setitem__(self, k, v):
        """Like :meth:`dict.__setitem__()` but converts value to :class:`Symbol`"""
        if self._strict and k in _reserved:
            raise TypeError(("Invalid key for strict SymbolDict", k))
        dict.__setitem__(self, k, v if isinstance(v, Symbol) else Symbol(v))
        self.__dict__.pop(k, None)
        
        
    def __delitem__(self, k):
        dict.__delitem__(self, k)
        self.__dict__.pop(k, None)
    
    
    def setdefault(self, k, v):
        """Like :meth:`dict.setdefault()` but converts value to :class:`Symbol`"""
        return dict.setdefault(self, k, Symbol(v))
    
    
    def __getattr__(self, attr):
        """Identical to ``self().getvalue(attr)`` but raises AttributeError if attr is not a dictionary key.
        
        Example:
            >>> sy = SymbolDict(isfile='os.path.isfile')
            >>> sy.isfile
            <function isfile at ...>
        """
        try:
            symb = _dictga(self, attr)
        except KeyError:
            raise AttributeError(attr)
        else:
            value = _readval(symb) if _readhas(symb) else _getvalue(symb, _ONCE)
            if attr not in _reserved:
                self.__dict__[attr] = value
            return value
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, dict.__repr__(self))


    def getvalue(self, key, rule=Rule.TRY_LOAD_ONCE):
        """Attempts to return the python object referenced symbolically by the Symbol under the given key.
        
        Args:
            key(hashable): one of the dictionary keys of the wrapped SymbolDict instance.
            rule(Rule): a rule specifying how to obtain the object's value.
                It defaults to ``Rule.TRY_LOAD_ONCE``.
            
        Returns:
            any: a python object referenced by this instance,
                if such a value can be found.
        
        Raises:
            Exception
                met while trying to
                obtain the value when it does not exist.
                Also raises KeyError if the key is missing in this SymbolDict.
        
        This method tries to obtain a value by importing modules and taking
        attributes according to the dotted path of the :class:`Symbol`
        instance ``self[key]``. In this path, the word
        before the first dot can be the
        name of an importable module or that of a builtin python object
        in the `__builtins__` dictionnary.
        
        If the object can not be  found, an exception is raised.
        
        The ``rule`` argument has the same meaning as in
        the :meth:`SymbolControl.getvalue()` method. See this method's
        documentation for details.
        
        Example:
            >>> sy = SymbolDict(err=Symbol('wave.Error'))
            >>> sy.getvalue('err')
            <class 'wave.Error'>
        """
        try:
            v = _getvalue(self[key], rule)
            if key not in _reserved:
                self.__dict__[key] = v
            return v
        except Exception:
            if key in self.__dict__:
                del self.__dict__[key]
            raise

    def hasvalue(self, key, rule=Rule.TRY_LOAD_ONCE):
        """Returns a boolean indicating if a value is available for the python object referenced symbolically by the symbol under this key.
        
        Args:
            key(hashable): one of the dictionary keys of this SymbolDict
            rule(Rule): a rule specifying how to obtain the object's value.
                It defaults to ``Rule.TRY_LOAD_ONCE``.
                
        Returns:
            bool: a boolean indicating if a value is available for this key.

        Raises:
            KeyError: if the key is missing.

        If the key is missing in this SymbolDict, the method raises
        a KeyError exception, otherwise, it returns True if the corresponding
        call to :meth:`getvalue()`
        would succeed, and returns False if the call to :meth:`getvalue()` would
        fail.
        
        The rule argument has the same meaning as in :meth:`Symbol.getvalue()`.
        See this method's documentation for details.
        
        Example:
            >>> sy = SymbolDict(err='wave.Error', ham='spam.ham')
            >>> sy.hasvalue('err')
            True
            >>> sy.hasvalue('ham')
            False
            >>> sy.hasvalue('eggs')
            Traceback ...
            KeyError
        """
        try:
            symb = self[key]
            v = _getvalue(symb, rule)
            if key not in _reserved:
                self.__dict__[key] = v
            return True
        except Exception:
            if key in self.__dict__:
                del self.__dict__[key]
            return False
        
    @deprecated
    def __call__(self):
        """Deprecated method. Returns the calling instance."""
        return self
    
    @deprecated
    def symboldict(self):
        """Deprecated method. Returns the calling instance."""
        return self

_reserved = frozenset(dir(dict) + dir(SymbolDict) + ['_strict',])
# print(_reserved)

def LaxSymbolDict(*args, **kwd):
    result = SymbolDict()
    result.strict = False
    result.update(dict(*args, **kwd))
    assert result._strict is False
    return result
