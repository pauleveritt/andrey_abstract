import inspect
from dataclasses import dataclass
from inspect import signature
from typing import Type, TypeVar, Dict, NamedTuple, Any, Optional

T = TypeVar('T')


class FieldInfo(NamedTuple):
    """ Extract needed info from dataclass fields, functions, etc. """

    field_name: str
    field_type: Type[T]
    default_value: Optional[Any]


FieldInfos = list[FieldInfo]


def get_field_infos(target: type) -> FieldInfos:
    results = []
    empty = getattr(inspect, '_empty')
    for value in signature(target).parameters.values():
        name = value.name
        name_type = value.annotation
        default = value.default
        results.append(FieldInfo(
            field_name=name,
            field_type=name_type,
            default_value=default if default is not empty else None
        ))
    return results


class View:
    pass


@dataclass
class Config:
    logo_path: str = 'default.png'


class DefaultView(View):
    config: Config


@dataclass
class Logo:
    config: Config = Config()

    def render(self) -> str:
        return f'<img src="{self.config.logo_path}"/>'


@dataclass
class Header:
    logo: Logo

    def render(self) -> str:
        return f'<h1>{self.logo.render()}</h1>'



class Registry:
    def __init__(self):
        self.dict: Dict[type, type] = {
            Logo: Logo,
            Header: Header,
        }

    def get_component(self, interface: Type[T]) -> T:
        # Use the interface to get the implementation class we want to make
        target = self.dict.get(interface, interface)

        # Use inspect to find what values that class wants
        kwargs = {}
        for field_info in get_field_infos(target):
            if field_info.default_value is not None:
                # This field has a default value, let's presume it
                # isn't something to look up. The actual rule here
                # is more complicated.
                field_value = field_info.default_value
            else:
                field_value = self.get_component(field_info.field_type)

            kwargs[field_info.field_name] = field_value

        # Construct and return the class
        return target(**kwargs)


def test_header():
    registry = Registry()
    header = registry.get_component(Header)
    assert header.logo.config.logo_path == 'default.png'
    assert header.render() == '<h1><img src="default.png"/></h1>'
