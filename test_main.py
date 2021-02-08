import pytest

from main import Header, Logo, View, Request, DefaultView, Config


def test_logo(request_registry) -> None:
    logo = request_registry.get_component(Logo)
    assert logo.config.logo_path == 'default.png'
    assert logo.render() == '<img src="default.png"/>'


def test_header(request_registry) -> None:
    header = request_registry.get_component(Header)
    assert header.logo.config.logo_path == 'default.png'
    assert header.render() == '<h1><img src="default.png"/></h1>'


def test_view(request_registry) -> None:
    view = request_registry.get_component(View)
    if isinstance(view, DefaultView):
        assert isinstance(view.header, Header)
        assert isinstance(view.request, Request)
    else:
        pytest.fail("Should have got DefaultView")
    assert view.render() == ('<div><h1><img src="default.png"/></h1> -- '
                             '/default/foo</div>')


def test_views(request_registry) -> None:
    x = request_registry.get_component(View)
    assert x.render() == ('<div><h1><img src="default.png"/></h1> -- '
                          '/default/foo</div>')


def test_config(request_registry) -> None:
    c = request_registry.get_component(Config)
    assert isinstance(c, Config)
