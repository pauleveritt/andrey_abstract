import pytest

from main import Header, Logo, View, Request, DefaultView
from registry import Registry, get_field_infos, Config


@pytest.fixture
def registry(app_registry: Registry) -> Registry:
    registry = Registry(app_registry)
    registry.register_singleton(Request('/default/foo'))
    registry.register_class(View, DefaultView)
    return registry


@pytest.fixture
def app_registry() -> Registry:
    registry = Registry()
    registry.configure_from_json('config.json')
    return registry
