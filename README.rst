

Symboldict
==========

Version 0.3.0

`Package documentation <http://symboldict.readthedocs.org>`__

Organize symbols and load them lazily

Install symboldict
------------------
python 2::

        
        pip install symboldict
        

python 3::

        
        pip3 install symboldict
        

Purpose
-------

The symboldict module implements a dictionary type containing symbolic
references to python objects in the hierarchy of importable
modules or builtins objects. Examples of symbolic references are
``'os.path.isdir'``, ``'telnetlib.Telnet'``, ``'complex.conjugate'`` etc.
References to user-defined objects are equally easy.

The module implements a lazy loading mechanism for these symbols, which
means that a dictionary can contain symbols from many different modules
without importing any of these modules until this import becomes necessary
in user code.

Symboldicts are meant to favor loose coupling between different parts
of an application. For example three modules ``A, B, C`` may share a
common symboldict ``sy`` instead of importing each others symbols
directly. ``A`` and ``B`` can use method ``sy.func()`` instead of
function ``C.func()``, thus decreasing the knowledge that each module
possesses about other modules.

Quick Start
-----------

SymbolDict objects
~~~~~~~~~~~~~~~~~~

A ``SymbolDict``, or dictionary of symbols, is typically created by
a statement similar to::

        
        >>> sy = SymbolDict(
        ...     isfile=symbol.os.path.isfile,
        ...     Telnet=symbol.telnetlib.Telnet,
        ...     conju=symbol.complex.conjugate,
        ...     eggs=symbol.spam.eggs,
        ... )
        

It is a regular dictionary, which keys are arbitrary but which values
are instances of a new type ``Symbol``::

        
        >>> sy
        SymbolDict({'eggs': Symbol('spam.eggs'), 'isfile': Symbol('os.path.isfile'), ...})
        >>>
        >>> isinstance(sy, dict)
        True
        

The usual dictionary operations apply::

        
        >>> sy['isfile']
        Symbol('os.path.isfile')
        >>> sy['eggs']
        Symbol('spam.eggs')
        >>> sy['Parser'] = Symbol('argparse.ArgumentParser')
        >>> 'Telnet' in sy
        True
        

Attribute access is overloaded for symboldicts.
It supplies a lazy access to the value symbolically represented by
the ``Symbol`` instance::

        >>> sy.isfile
        <function isfile at 0x7f7fd0f40050>
        >>> sy.Telnet
        <class 'telnetlib.Telnet at 0x7fbb3a518db8'>
        >>> sy.conju
        <method 'conjugate' of 'complex' objects>
        >>> sy.eggs
        Traceback (most recent call last)
            ...
        ImportError: No module named spam
        

This syntax enables user code to manipulate the ``SymbolDict``
instance as if it was a module containing python variables
available through qualified names. Actual modules are imported
only when it is necessary to do so.

The values of these variables can also be obtained by the following
alternative expression,
which handles the case where the dictionary keys are not
character strings or where they are existing attribute names of the
``dict`` class (such as ``'update'`` or ``'clear'``)::

        >>> sy.getvalue('isfile')
        <function isfile at 0x7f7fd0f40050>
        >>> sy.getvalue('Parser')
        <class 'argparse.ArgumentParser'>
        

Previous versions of this module used a call syntax here, requiring
expressions such as ``sy().getvalue('isfile')``. Calling a
``SymbolDict`` instance is deprecated and currently returns
the instance itself.

**Special attributes**

As of version 0.3.0, the valued loaded lazily, such as ``sy.Telnet`` above
are stored in the instance's ``__dict__`` under the
corresponding attribute. It means that subsequent accesses to these values
have the efficiency of a simple attribute access.

To avoid collisions with ordinary dict method names, SymbolDict will normally
reject the use of a certain number of keys such as::

        
          _strict     has_key     itervalues   keys      iterkeys     items
          iteritems   viewkeys    hasvalue     update    fromkeys     clear
          pop         viewitems   symboldict   popitem   setdefault   values
          getvalue    strict      get          copy      viewvalues
        

and magic attribute names such as ``__doc__`` or ``__setattr__``. Using
one of these keys in a symboldict will raise a ``TypeError`` exception.

This restriction on the keys can be removed by unsetting the ``strict``
property::

        
        sy.strict = False
        

It can also be removed at instantiation time by calling the
``LaxSymbolDict``
constructor instead of ``SymbolDict``. For those lax symboldicts, forbidden
keys such as ``'popitem'`` can be used, but the lazy access can only be
obtained through
the ``getvalue()`` method. Loaded values won't be added to the
instance's ``__dict__``.

Symbol objects
~~~~~~~~~~~~~~

Symbol objects (used as values in ``SymbolDict`` instances) wrap a
dot-separated path to a python object, which may exist or not, for example::

        
        >>> a = Symbol('wave.Error')
        >>> b = Symbol('complex.conjugate')
        >>> c = Symbol('spam.ham.eggs')
        

Attribute access is overloaded to allow building other instances
with the dot syntax::

        
        >>> Symbol('spam').ham.eggs
        Symbol('spam.ham.eggs')
        

A special instance named ``symbol`` is defined, which
value is ``Symbol('')``. Its path is empty, and it permits
expressions such as::

        
        >>> a = symbol.wave.Error
        >>> b = symbol.complex.conjugate
        >>> c = symbol.spam.ham.eggs
        

which produce the same result as above.

Defining an instance does *not* trigger an attempt
to retrieve the indicated python object by importing modules or
accessing attributes. However, standalone ``Symbol`` instances
have the ability to fetch this object by calling
the ``getvalue()`` method::

        
        >>> a().getvalue()
        <class 'wave.Error'>
        

The call syntax ``a()`` enables to bypass the overloading of
the attribute operator. It returns a special adapter having the type
``SymbolControl``. Method ``getvalue()`` cannot be called
directly on the ``Symbol`` instance.

A method ``hasvalue()`` indicates if a value can be obtained for
the symbol's path. Unlike ``getvalue()``, it does not raise an exception
when there is no value::

        
        >>> symbol.spam.ham().hasvalue()
        False
        

This method also exists for symboldicts. It may raise ``KeyError`` if
the  key is missing in the dictionary::

        
        >>> sy.hasvalue('conju')
        True
        

License
-------

This software is licensed under the `MIT License <http://en.wikipedia.org/wiki/MIT_License>`__

© 2014-2015 Eric Ringeisen
