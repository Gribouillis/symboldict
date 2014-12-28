

Symboldict
==========

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

        >>> sy().getvalue('isfile')
        <function isfile at 0x7f7fd0f40050>
        >>> sy().getvalue('Parser')
        <class 'argparse.ArgumentParser'>
        

The call syntax ``sy()`` should be stressed here. Calling a
``SymbolDict`` instance returns a special lightweight adapter
having the type ``SymbolDictControl``. Direct methods cannot
be called on symboldicts because the attribute operator is overloaded.

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
        

Again, the call syntax ``a()`` enables to bypass the overloading of
the attribute operator. It returns a special adapter having the type
``SymbolControl``.

A method ``hasvalue()`` indicates if a value can be obtained for
the symbol's path. Unlike ``getvalue()``, it does not raise an exception
when there is no value::

        
        >>> symbol.spam.ham().hasvalue()
        False
        

This method also exists for symboldicts. It may raise ``KeyError`` if
the  key is missing in the dictionary::

        
        >>> sy().hasvalue('conju')
        True
        

License
-------

This software is licensed under the `MIT License <http://en.wikipedia.org/wiki/MIT_License>`__

© 2014 Eric Ringeisen
