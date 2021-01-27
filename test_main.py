import pytest

from main import Registry, Header, Logo, get_field_infos


@pytest.fixture
def registry():
    registry = Registry()
    registry.configure_from_json('config.json')
    return registry


def test_logo(registry):
    logo = registry.get_component(Logo)
    assert logo.config.logo_path == 'default.png'
    assert logo.render() == '<img src="default.png"/>'


def test_header(registry):
    header = registry.get_component(Header)
    assert header.logo.config.logo_path == 'default.png'
    assert header.render() == '<h1><img src="default.png"/></h1>'


def test_field_infos():
    field_infos = get_field_infos(Header)
    assert Logo == field_infos[0].field_type
