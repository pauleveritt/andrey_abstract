import pytest

from main import Header, Logo, View, Request, DefaultView
from registry import Registry


def test_logo(registry: Registry) -> None:
    logo = registry.get_component(Logo)
    assert logo.config.logo_path == 'default.png'
    assert logo.render() == '<img src="default.png"/>'


def test_header(registry: Registry) -> None:
    header = registry.get_component(Header)
    assert header.logo.config.logo_path == 'default.png'
    assert header.render() == '<h1><img src="default.png"/></h1>'


def test_view(registry: Registry) -> None:
    view = registry.get_component(View)
    if isinstance(view, DefaultView):
        assert isinstance(view.header, Header)
        assert isinstance(view.request, Request)
    else:
        pytest.fail("Should have got DefaultView")
    assert view.render() == ('<div><h1><img src="default.png"/></h1> -- '
                             '/default/foo</div>')


def test_views(registry: Registry) -> None:
    x = registry.get_component(View)
    assert x.render() == ('<div><h1><img src="default.png"/></h1> -- '
                          '/default/foo</div>')
