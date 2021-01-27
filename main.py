from __future__ import annotations

import inspect
import json
import typing
from abc import abstractmethod, ABCMeta
from collections import defaultdict
from dataclasses import dataclass
from inspect import signature
from typing import Type, TypeVar, Dict, NamedTuple, Any, Optional, List

T = TypeVar('T')


class FieldInfo(NamedTuple):
    """ Extract needed info from dataclass fields, functions, etc. """

    field_name: str
    field_type: Type[T]
    default_value: Optional[Any]


def get_field_infos(target: type) -> List[FieldInfo]:
    results = []
    empty = getattr(inspect, '_empty')
    try:
        sign = signature(target)
    except ValueError:
        return []

    type_hints = typing.get_type_hints(target)

    for value in sign.parameters.values():
        default = value.default
        results.append(FieldInfo(
            field_name=value.name,
            field_type=type_hints.get(value.name, value.annotation),
            default_value=default if default is not empty else None
        ))
    return results


@dataclass
class Request:
    url: str


class View(metaclass=ABCMeta):
    request: Request
    url_prefix: str

    @abstractmethod
    def render(self) -> str: ...

    def matches(self) -> bool:
        return self.request.url.startswith(self.url_prefix)

    @classmethod
    def select(cls, registry: Registry) -> View:
        views = registry.get_components(View)
        return next(view for view in views if view.matches())


@dataclass
class Config:
    logo_path: str


@dataclass
class DefaultView(View):
    request: Request
    header: Header
    url_prefix: str = "/default"

    def render(self) -> str:
        return f'''<div>{self.header.render()} -- {self.request.url}</div>'''


@dataclass
class Logo:
    config: Config

    def render(self) -> str:
        return f'<img src="{self.config.logo_path}"/>'


@dataclass
class Header:
    logo: Logo

    def render(self) -> str:
        return f'<h1>{self.logo.render()}</h1>'


class Registry:
    def __init__(self, parent: Registry = None):
        self.classes: Dict[type, List[type]] = defaultdict(list)
        self.singletons: Dict[type, Any] = {}
        self.parent: Optional[Registry] = parent

    def get_components(self, interface: Type[T]) -> List[T]:
        try:
            return [self.singletons[interface]]
        except KeyError:
            pass

        # Use the interface to get the implementation class we want to make
        classes = self.classes.get(interface)
        if not classes:
            if self.parent is not None:
                return self.parent.get_components(interface)
            else:
                classes = [interface]
        return [self._instantiate_cls(cls) for cls in classes]

    def _instantiate_cls(self, cls: Type[T]) -> T:
        # Use inspect to find what values that class wants
        kwargs = {}
        field_infos = get_field_infos(cls)
        if not field_infos:
            raise TypeError(f"Class '{cls.__qualname__}' does not define any "
                            f"constructor parameters")

        for field_info in field_infos:
            if field_info.default_value is not None:
                # This field has a default value, let's presume it
                # isn't something to look up. The actual rule here
                # is more complicated.
                field_value = field_info.default_value
            else:
                field_value = self.get_component(field_info.field_type)

            kwargs[field_info.field_name] = field_value

        # Construct and return the class
        return cls(**kwargs)

    def get_component(self, interface: Type[T]) -> T:
        return next(iter(self.get_components(interface)))

    def register_singleton(self, x: T, cls: Type[T] = None) -> None:
        if cls is None:
            cls = type(x)
        self.singletons[cls] = x

    def register_class(self, interface: Type[T], cls: Type[T]) -> None:
        self.classes[interface].append(cls)

    def configure_from_json(self, filename: str) -> None:
        with open(filename, 'rb') as fd:
            kwargs = json.load(fd)
        self.register_singleton(Config(**kwargs))


def test_header():
    registry = Registry()
    header = registry.get_component(Header)
    assert header.logo.config.logo_path == 'default.png'
    assert header.render() == '<h1><img src="default.png"/></h1>'
