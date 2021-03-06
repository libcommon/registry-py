## -*- coding: UTF-8 -*-
## registry.py
##
## Copyright (c) 2020 libcommon
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in all
## copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
## SOFTWARE.


import os
from typing import Any, ClassVar, Dict, Optional, Tuple, Type


__author__ = "libcommon"


class RegistryMetaclassMixin:
    """Mixin class implementing registry pattern
    with Python metaprogramming.
    """
    __slots__ = ()
    _REGISTRY: ClassVar[Optional[Dict[str, Type[Any]]]] = None

    @classmethod
    def registry(cls) -> Optional[Dict[str, Type[Any]]]:
        """Returns copy of registry."""
        if cls._REGISTRY is None:
            return None
        return dict(cls._REGISTRY)

    @classmethod
    def retrieve(cls, name: str) -> Optional[Type[Any]]:
        """Retrieves name from registry."""
        if cls._REGISTRY is None:
            return None
        return cls._REGISTRY.get(name)

    @classmethod
    def _add_class(cls, name: str, new_cls: Type[Any]) -> None:
        """Perform any necessary checks on new classes (new_cls) before adding to
        registry. For example, checking for the presence of class variables
        or names of new classes.  Default implementation simply adds new class
        to the registry.
        Raises:
            TypeError: if name is already present in the registry.
        """
        if cls._REGISTRY is None:
            return None
        if name in cls._REGISTRY:
            raise TypeError("Type {} already exists in registry".format(name))
        cls._REGISTRY[name] = new_cls
        return None

    def __new__(cls, name: str, bases: Tuple[Type[Any], ...], attrs: Dict[str, Any]):   # pylint: disable=arguments-differ
        """Create new type and pass new class to _add_class."""
        new_cls = type.__new__(cls, name, bases, attrs)
        cls._add_class(name, new_cls)
        return new_cls


if os.environ.get("ENVIRONMENT") == "TEST":
    from abc import ABCMeta, abstractmethod
    import unittest

    class MetaNoRegistry(RegistryMetaclassMixin, ABCMeta):
        """Metaclass without registry."""

    class BaseNoRegistry(metaclass=MetaNoRegistry):
        pass

    class MetaWithRegistry(RegistryMetaclassMixin, ABCMeta):
        """Metaclass with registry."""
        _REGISTRY: ClassVar[Dict[str, Type[Any]]] = dict()

    class BaseWithRegistry(metaclass=MetaWithRegistry):
        @abstractmethod
        def abstract(self) -> str:
            return "ABSTRACT"

    class TestRegistryMetaclassMixin(unittest.TestCase):
        """Tests for RegistryMetaclassMixin."""

        def test_registry_method_registry_none(self):
            """Test registry method when REGISTRY is None"""
            self.assertEqual(None, MetaNoRegistry.registry())

        def test_registry_method_registry_initialized(self):
            """Test registry method when REGISTRY is initialized"""
            self.assertEqual(dict(BaseWithRegistry=BaseWithRegistry), MetaWithRegistry.registry())

        def test_retrieve_method_registry_none(self):
            """Test retrieve method when REGISTRY is None."""
            self.assertEqual(None, MetaNoRegistry.retrieve("BaseNoRegistry"))

        def test_retrieve_method_registry_initialized(self):
            """Test retrieve method when REGISTRY is initialized."""
            self.assertEqual(BaseWithRegistry, MetaWithRegistry.retrieve("BaseWithRegistry"))
