from main import Header, Logo
from registry import get_field_infos


def test_field_infos() -> None:
    field_infos = get_field_infos(Header)
    assert Logo == field_infos[0].field_type
