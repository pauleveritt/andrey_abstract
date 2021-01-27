from main import Registry, Header, Logo, Config, get_field_infos


def test_logo():
    logo = Logo(Config())
    assert logo.config.logo_path == 'default.png'
    assert logo.render() == '<img src="default.png"/>'


def test_header():
    registry = Registry()
    header = registry.get_component(Header)
    assert header.logo.config.logo_path == 'default.png'
    assert header.render() == '<h1><img src="default.png"/></h1>'


def test_field_infos():
    field_infos = get_field_infos(Header)
    assert Logo == field_infos[0].field_type
