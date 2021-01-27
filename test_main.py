from main import Registry, Header, Logo, Config


def test_1():
    logo = Logo(Config())
    assert logo.config.logo_path == 'default.png'
    assert logo.render() == '<img src="default.png"/>'


def test_2():
    registry = Registry()
    header = registry.get_component(Header)
    assert header.logo.config.logo_path == 'default.png'
    assert header.render() == '<h1><img src="default.png"/></h1>'
