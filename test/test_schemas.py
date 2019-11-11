import pytest
from jsonschema import RefResolver


@pytest.mark.parametrize("base_path", ("/v1", "/v1/"))
def test_base_path_suffix(swagger_20, base_path):
    # When suffix is present or not present in the raw schema's "basePath"
    swagger_20.raw_schema["basePath"] = base_path
    # Then base path ends with "/" anyway in the swagger instance
    assert swagger_20.base_path == "/v1/"
    assert swagger_20.verbose_name == "Swagger 2.0"
    assert swagger_20.spec_version == "2.0"


@pytest.mark.parametrize(
    "server, base_path",
    (
        (
            [
                {
                    "url": "https://api.example.com/{basePath}/foo/{bar}",
                    "variables": {"basePath": {"default": "v1"}, "bar": {"default": "bar"}},
                }
            ],
            "/v1/foo/bar/",
        ),
        ([], "/"),
    ),
)
def test_open_api_base_path(openapi_30, server, base_path):
    openapi_30.raw_schema["servers"] = server
    assert openapi_30.base_path == base_path


def test_open_api_verbose_name(openapi_30):
    assert openapi_30.verbose_name == "Open API 3.0.0"
    assert openapi_30.spec_version == "3.0.0"


def test_resolver_cache(swagger_20, mocker):
    spy = mocker.patch("schemathesis.schemas.jsonschema.RefResolver", wraps=RefResolver)
    assert "_resolver" not in swagger_20.__dict__
    assert isinstance(swagger_20.resolver, RefResolver)
    assert spy.call_count == 1
    # Cached
    assert "_resolver" in swagger_20.__dict__
    assert isinstance(swagger_20.resolver, RefResolver)
    assert spy.call_count == 1
