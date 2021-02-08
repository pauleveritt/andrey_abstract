import pytest

from main import View, Request, DefaultView, configure_from_json
from registry import Registry


@pytest.fixture
def request_registry(app_registry: Registry) -> Registry:
    registry = Registry(app_registry)
    registry.register_singleton(Request('/default/foo'))
    registry.register_class(View, DefaultView)
    return registry


@pytest.fixture
def app_registry() -> Registry:
    registry = Registry()
    configure_from_json(registry, 'config.json')
    return registry
