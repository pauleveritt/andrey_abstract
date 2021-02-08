from __future__ import annotations

import inspect
from abc import ABCMeta
from collections import defaultdict
from inspect import signature
from typing import NamedTuple, Type, Optional, Any, TypeVar, get_type_hints


class FieldInfo(NamedTuple):
    """ Extract needed info from dataclass fields, functions, etc. """

    field_name: str
    field_type: Type[Component]
    default_value: Optional[Any]


def get_field_infos(target: type) -> list[FieldInfo]:
    results = []
    empty = getattr(inspect, '_empty')
    try:
        sign = signature(target)
    except ValueError:
        return []

    type_hints = get_type_hints(target)

    for value in sign.parameters.values():
        default = value.default
        results.append(FieldInfo(
            field_name=value.name,
            field_type=type_hints.get(value.name, value.annotation),
            default_value=default if default is not empty else None
        ))
    return results


class Component(metaclass=ABCMeta):
    @classmethod
    def select(cls: Type[TC], registry: Registry) -> TC:
        return registry.get_components(cls)[0]


T = TypeVar('T')
TC = TypeVar('TC', bound=Component, covariant=True)


class Registry:
    def __init__(self, parent: Registry = None):
        self.classes: dict[type, list[type]] = defaultdict(list)
        self.singletons: dict[type, Any] = {}
        self.parent: Optional[Registry] = parent

    def get_components(self, interface: Type[TC]) -> list[TC]:
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

    def _instantiate_cls(self, cls: Type[TC]) -> TC:
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
        return cls(**kwargs)  # type: ignore

    def get_component(self, interface: Type[TC]) -> TC:
        return interface.select(self)

    def register_singleton(self, x: T, cls: Type[T] = None) -> None:
        if cls is None:
            cls = type(x)
        self.singletons[cls] = x

    def register_class(self, interface: Type[TC], cls: Type[TC]) -> None:
        self.classes[interface].append(cls)
