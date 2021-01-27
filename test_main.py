import pytest

from main import Registry, Header, Logo, get_field_infos, View, Request, DefaultView


@pytest.fixture
def registry(app_registry) -> Registry:
    registry = Registry(app_registry)
    registry.register_singleton(Request('/default/foo'))
    registry.register_class(View, DefaultView)
    return registry


@pytest.fixture
def app_registry() -> Registry:
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


def test_view(registry):
    view = registry.get_component(View)
    if isinstance(view, DefaultView):
        assert isinstance(view.header, Header)
        assert isinstance(view.request, Request)
    else:
        pytest.fail("Should have got DefaultView")
    assert view.render() == ('<div><h1><img src="default.png"/></h1> -- '
                             '/default/foo</div>')


def test_views(registry):
    x = View.select(registry)
    assert x.render() == ('<div><h1><img src="default.png"/></h1> -- '
                          '/default/foo</div>')
