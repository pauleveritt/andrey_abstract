from main import Header, Logo
from registry import Registry, get_field_infos, Config


def test_field_infos() -> None:
    field_infos = get_field_infos(Header)
    assert Logo == field_infos[0].field_type


def test_config(registry: Registry) -> None:
    c = registry.get_component(Config)
    assert isinstance(c, Config)
