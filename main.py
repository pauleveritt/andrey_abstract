from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import Type

from registry import Component, Config, Registry


@dataclass
class Request(Component):
    url: str


class View(Component):
    request: Request
    url_prefix: str

    @abstractmethod
    def render(self) -> str: ...

    def matches(self) -> bool:
        return self.request.url.startswith(self.url_prefix)

    @classmethod
    def select(cls: Type[View], registry: Registry) -> View:
        views = registry.get_components(View)
        return next(view for view in views if view.matches())


@dataclass
class DefaultView(View):
    request: Request
    header: Header
    url_prefix: str = "/default"

    def render(self) -> str:
        return f'''<div>{self.header.render()} -- {self.request.url}</div>'''


@dataclass
class Logo(Component):
    config: Config

    def render(self) -> str:
        return f'<img src="{self.config.logo_path}"/>'


@dataclass
class Header(Component):
    logo: Logo

    def render(self) -> str:
        return f'<h1>{self.logo.render()}</h1>'
