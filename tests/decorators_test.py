from inspect import Signature
from typing import Dict

from automd.decorators import disable_automd, automd
from automd.keys import AutoMDKeys


def test_automd_decorator_inputs():
    @automd(parameter_schema={"key", "value"},
            summary="test_summary",
            description="test_description",
            tags=[{"key": "value"}, {"key_2": "value_2"}])
    def func():
        pass

    test_func = func
    assert hasattr(test_func, AutoMDKeys.function.value)

    automd_params: Dict = getattr(test_func, AutoMDKeys.function.value)
    assert automd_params["parameter_schema"] == {"key", "value"}
    assert automd_params["summary"] == "test_summary"
    assert automd_params["description"] == "test_description"
    assert automd_params["tags"] == [{"key": "value"}, {"key_2": "value_2"}]


def test_automd_decorator_inspections():
    @automd()
    def func(arg_1: str, arg_2: bool) -> int:
        pass

    test_func = func
    assert hasattr(test_func, AutoMDKeys.function.value)

    automd_params: Dict = getattr(test_func, AutoMDKeys.function.value)

    assert "func_signature" in automd_params.keys()
    func_sig: Signature = automd_params["func_signature"]

    assert func_sig.parameters["arg_1"].annotation == str
    assert func_sig.parameters["arg_2"].annotation == bool
    assert automd_params["response_schemas"] == {"200": int}


def test_disable_automd_decorator():
    @disable_automd()
    def func():
        pass

    test_func = func
    assert hasattr(test_func, AutoMDKeys.hide_function.value)
