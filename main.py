import inspect
from dataclasses import dataclass
from typing import Type, TypeVar, Dict


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


T = TypeVar('T')


class Registry:
    def __init__(self):
        self.dict: Dict[type, type] = {
            Logo: Logo,
            Header: Header,
        }

    def get_component(self, interface: Type[T]) -> T:
        cls = self.dict.get(interface, interface)
        kwargs = {}
        for value in inspect.signature(cls).parameters.values():
            name = value.name
            name_type = value.annotation
            default = value.default
            if default is not getattr(inspect, '_empty'):
                kwargs[name] = default
            else:
                kwargs[name] = self.get_component(name_type)
        return cls(**kwargs)
