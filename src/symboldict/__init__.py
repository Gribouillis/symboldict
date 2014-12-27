# -*-coding: utf8-*-
"""symboldict module
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from importlib import import_module
import sys
from .version import __version__

# sublime singleton from the python decorator library

def singleton(cls):
    """Class decorator which creates a unique callable instance"""
    instance = cls()
    instance.__call__ = lambda: instance
    return instance

@singleton
class _VOID_VALUE(object):
    def __repr__(self):
       return '_VOID_VALUE()'
   
_VOID_VALUE = _VOID_VALUE
"""Default value for a :class:`Symbol` before its value is loaded"""


@singleton
class _FAIL_VALUE(object):
    def __repr__(self): return '_FAIL_VALUE()'

_FAIL_VALUE = _FAIL_VALUE
"""Default value for of a :class:`Symbol` for which loading a value failed"""

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
    __slots__ = ("_path", "_value")

    def __init__(self, *parts):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        parts = [str(x) for x in parts]
        s = _DOT.join(x for x in parts if x)
        Symbol._path.__set__(self, s)
        Symbol._value.__set__(self, _VOID_VALUE)

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
        return Symbol._path.__get__(self)
        
        
    def __repr__(self):
        return "Symbol({})".format(repr(Symbol._path.__get__(self)))
    
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
        return (_cid(self) == _cid(other)) and (_getpath(self) == _getpath(other))
    def __ne__(self, other):
        return not (self == other)
    def __le__(self, other):
        return not (self > other)
    def __lt__(self, other):
        return (_cid(self) < _cid(other)) or (
            (_cid(self) == _cid(other)) and (_getpath(self) < _getpath(other)))
    def __ge__(self, other):
        return not (self < other)
    def __gt__(self, other):
        return (_cid(self) > _cid(other)) or (
            (_cid(self) == _cid(other)) and (_getpath(self) > _getpath(other)))
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
        return hash((_cid(self), _getpath(self)))

_getpath = Symbol._path.__get__
def _cid(obj):
    return id(type(obj)) # cannot use .__class__

symbol = Symbol()
"""An instance of :class:`Symbol` with empty path.

Used to build other Symbols by the means of attribute access.

Example:
    >>> symbol.spam.ham
    Symbol('spam.ham')
"""

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
            self.getvalue(rule=rule)
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
        if not _isrule(rule):
            raise TypeError(('Need symboldict.Rule,', type(rule), 'found'))
        v = Symbol._value.__get__(self.__symb)
        if rule is Rule.DONT_LOAD:
            if v in (_VOID_VALUE, _FAIL_VALUE):
                raise VoidValueError(self.__symb)
            else:
                return v
        elif (v is _VOID_VALUE or rule is Rule.FORCE_RELOAD 
                or (v is _FAIL_VALUE and rule is not Rule.TRY_LOAD_ONCE)):
            # we must try to load
            s = str(self.__symb)
            L = s.split(".")
            acc = L[0]
            try:
                try:
                    # may raise ValueError if s is empty string
                    v = import_module(acc)
                except ImportError:
                    # this section may raise AttributeError for example
                    v = __builtins__.get(L[0], _VOID_VALUE)
                    if v is _VOID_VALUE:
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
                Symbol._value.__set__(self.__symb, _FAIL_VALUE)
                raise
            else:
                Symbol._value.__set__(self.__symb, v)
                return v
        elif v is _FAIL_VALUE:
            raise VoidValueError(self.__symb)
        else:
            return v
    
    def path(self):
        """Returns the path of the referenced :class:`Symbol` instance.
        
        Example:
            >>> s = Symbol('socket.socket')
            >>> s().path()
            'socket.socket'
        """
        return Symbol._path.__get__(self.__symb)
    
    def symbol(self):
        """Returns the referenced :class:`Symbol` instance.
        
        Example:
            >>> s = Symbol('socket.socket')
            >>> s().symbol() is s
            True
        """
        return self.__symb

class SymbolDict(dict):
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
    - The dictionary is callable, see :meth:`SymbolDict.__call__()`
    
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
        >>> sy().hasvalue('isfile')
        True
        >>> sy().getvalue('Parser')
        <class 'argparse.ArgumentParser'>
        
    """
    __slots__ = ()
    
    def __new__(cls, *args, **kwargs):
        instance = dict.__new__(cls)
        return instance
    
    def __init__(self, *args, **kwargs):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        dict.__init__(self)
        self.update(dict(*args, **kwargs))
    
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
        dict.update(self, [(k, Symbol(v)) for (k, v) in d.items()])
        
    def __setitem__(self, k, v):
        """Like :meth:`dict.__setitem__()` but converts value to :class:`Symbol`"""
        dict.__setitem__(self, k, Symbol(v))
    
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
        v = self.get(attr, None)
        if v is None:
            raise AttributeError(attr)
        return v().getvalue()
        
    def __call__(self):
        """Calling a :class:`SymbolDict` instance wraps it into a :class:`SymbolDictControl` object.
        
        Returns:
            SymbolDictControl: a lightweight object wrapping the :class:`SymbolDict`.
            
        This allows to bypass the overloading of the dot operator to
        access some methods.
        
        Example:
            >>> sy = SymbolDict(isfile='os.path.isfile')
            >>> sy().getvalue('isfile')
            <function isfile at ...>
            
        """
        return SymbolDictControl(self)
    
    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, dict.__repr__(self))


class SymbolDictControl(object):
    """SymbolDictControl(sy) -> new SymbolDictControl instance
    
    Args:
        sy(SymbolDict): a symboldict referenced by the SymbolDictControl object
        
    This is a class of lightweight wrappers around :class:`SymbolDict` instances
    used to bypass the overriding of the dot operator in this class.
    SymbolDictControl objects are returned by the :meth:`SymbolDict.__call__()`
    method. Their main purpose is to hold methods to manipulate Symbols
    contained in the SymbolDict.
    
    Example:
        >>> sy = SymbolDict(isfile='os.path.isfile')
        >>> sy()
        <symboldict.SymbolDictControl object ...>
        >>> sy().hasvalue('isfile')
        True
        >>> sy().getvalue('isfile')
        <function isfile ...>
        >>> sy().symboldict() is sy
        True

    """
    __slots__ = ('__dict',)

    def __init__(self, symboldict):
        """x.__init__(...) initializes x; see help(type(x)) for signature"""
        self.__dict = symboldict

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
                Also raises KeyError if the key is missing in the
                underlying SymbolDict.
        
        This method tries to obtain a value by importing modules and taking
        attributes according to the dotted path of the :class:`Symbol`
        instance ``self.symboldict()[key]``. In this path, the word
        before the first dot can be the
        name of an importable module or that of a builtin python object
        in the `__builtins__` dictionnary.
        
        If the object can not be  found, an exception is raised.
        
        The ``rule`` argument has the same meaning as in
        the :meth:`SymbolControl.getvalue()` method. See this method's
        documentation for details.
        
        Example:
            >>> sy = SymbolDict(err=Symbol('wave.Error'))
            >>> sy().getvalue('err')
            <class 'wave.Error'>
        """
        return self.__dict[key]().getvalue(rule=rule)

    def hasvalue(self, key, rule=Rule.TRY_LOAD_ONCE):
        """Returns a boolean indicating if a value is available for the python object referenced symbolically by the symbol under this key.
        
        Args:
            key(hashable): one of the dictionary keys of the wrapped SymbolDict
            rule(Rule): a rule specifying how to obtain the object's value.
                It defaults to ``Rule.TRY_LOAD_ONCE``.
                
        Returns:
            bool: a boolean indicating if a value is available for this key.

        Raises:
            KeyError: if the key is missing.

        If the key is missing in the wrapped SymbolDict, this method raises
        a KeyError exception, otherwise, it returns True if the corresponding
        call to :meth:`getvalue()`
        would succeed, and returns False if the call to :meth:`getvalue()` would
        fail.
        
        The rule argument has the same meaning as in :meth:`Symbol.getvalue()`.
        See this method's documentation for details.
        
        Example:
            >>> sy = SymbolDict(err='wave.Error', ham='spam.ham')
            >>> sy().hasvalue('err')
            True
            >>> sy().hasvalue('ham')
            False
            >>> sy().hasvalue('eggs')
            Traceback ...
            KeyError
        """
        return self.__dict[key]().hasvalue(rule=rule)

    def symboldict(self):
        """Returns the wrapped SymbolDict instance"""
        return self.__dict
