from inspect import Parameter
from typing import Dict
from unittest.mock import patch

import pytest
from openbb_core.app.command_runner import (
    CommandRunner,
    ExecutionContext,
    ParametersBuilder,
)
from openbb_core.app.model.command_context import CommandContext
from openbb_core.app.model.system_settings import SystemSettings
from openbb_core.app.model.user_settings import UserSettings
from openbb_core.app.router import CommandMap


@pytest.fixture()
def execution_context():
    """Set up execution context."""
    sys = SystemSettings()
    user = UserSettings()
    cmd_map = CommandMap()
    return ExecutionContext(cmd_map, "mock/route", sys, user)


@pytest.fixture()
def mock_func():
    """Set up mock function."""

    def mock_func(
        a: int, b: int, c: float = 10.0, d: int = 5, provider_choices: Dict = {}
    ) -> None:
        pass

    return mock_func


def test_execution_context():
    """Test execution context."""
    sys = SystemSettings()
    user = UserSettings()
    cmd_map = CommandMap()
    ctx = ExecutionContext(cmd_map, "mock/route", sys, user)

    assert isinstance(ctx, ExecutionContext)
    assert ctx.system_settings == sys
    assert ctx.user_settings == user
    assert ctx.command_map == cmd_map
    assert ctx.route == "mock/route"


def test_parameters_builder():
    """Test parameters builder."""
    assert ParametersBuilder()


@pytest.mark.parametrize(
    "input_func, expected_annotations",
    [
        (lambda x: x, {"x": Parameter(name="x", kind=Parameter.POSITIONAL_OR_KEYWORD)}),
        (
            lambda a, b, c=10: a + b + c,
            {
                "a": Parameter(name="a", kind=Parameter.POSITIONAL_OR_KEYWORD),
                "b": Parameter(name="b", kind=Parameter.POSITIONAL_OR_KEYWORD),
                "c": Parameter(
                    name="c", kind=Parameter.POSITIONAL_OR_KEYWORD, default=10
                ),
            },
        ),
        (
            lambda x, y, *, z: x + y + z,
            {
                "x": Parameter(name="x", kind=Parameter.POSITIONAL_OR_KEYWORD),
                "y": Parameter(name="y", kind=Parameter.POSITIONAL_OR_KEYWORD),
                "z": Parameter(name="z", kind=Parameter.KEYWORD_ONLY),
            },
        ),
    ],
)
def test_parameters_builder_get_polished_func(input_func, expected_annotations):
    """Test get_polished_func."""
    polished_func = ParametersBuilder.get_polished_func(input_func)

    assert polished_func.__annotations__ == expected_annotations
    assert polished_func.__signature__ == input_func.__signature__


@pytest.mark.parametrize(
    "input_func, expected_params",
    [
        (lambda x: x, [Parameter("x", Parameter.POSITIONAL_OR_KEYWORD)]),
        (
            lambda a, b, c=10: a + b + c,
            [
                Parameter("a", Parameter.POSITIONAL_OR_KEYWORD),
                Parameter("b", Parameter.POSITIONAL_OR_KEYWORD),
                Parameter("c", Parameter.POSITIONAL_OR_KEYWORD, default=10),
            ],
        ),
        (
            lambda x, y, *, z: x + y + z,
            [
                Parameter("x", Parameter.POSITIONAL_OR_KEYWORD),
                Parameter("y", Parameter.POSITIONAL_OR_KEYWORD),
                Parameter("z", Parameter.KEYWORD_ONLY),
            ],
        ),
    ],
)
def test_parameters_builder_get_polished_parameter_list(input_func, expected_params):
    """Test get_polished_parameter_list."""
    param_list = ParametersBuilder.get_polished_parameter_list(input_func)

    assert param_list == expected_params


@pytest.mark.parametrize(
    "input_func, input_args, input_kwargs, expected_result",
    [
        (lambda x: x, (5,), {}, {"x": 5}),
        (lambda a, b, c=10: a + b + c, (2, 3), {}, {"a": 2, "b": 3, "c": 10}),
        (lambda x, y, *, z: x + y + z, (1, 2), {"z": 3}, {"x": 1, "y": 2, "z": 3}),
    ],
)
def test_parameters_builder_merge_args_and_kwargs(
    input_func, input_args, input_kwargs, expected_result
):
    """Test merge_args_and_kwargs."""
    result = ParametersBuilder.merge_args_and_kwargs(
        input_func, input_args, input_kwargs
    )

    assert result == expected_result


@pytest.mark.parametrize(
    "kwargs, system_settings, user_settings, expected_result",
    [
        (
            {"cc": "existing_cc"},
            SystemSettings(),
            UserSettings(),
            {"cc": "mock_cc"},
        ),
    ],
)
def test_parameters_builder_update_command_context(
    kwargs, system_settings, user_settings, expected_result
):
    def other_mock_func(
        cc: CommandContext,
        a: int,
        b: int,
    ) -> None:
        pass

    result = ParametersBuilder.update_command_context(
        other_mock_func, kwargs, system_settings, user_settings
    )

    assert isinstance(result["cc"], CommandContext)
    assert result["cc"].system_settings == system_settings
    assert result["cc"].user_settings == user_settings


@pytest.mark.parametrize(
    "command_coverage, route, kwargs, route_default, expected_result",
    [
        (
            {"route1": ["choice1", "choice2"]},
            "route1",
            {"provider_choices": {"provider": None}},
            None,
            {"provider_choices": {"provider": None}},
        ),
        (
            {"route1": ["choice1", "choice2"]},
            "route1",
            {"provider_choices": {"provider": ["choice1", "choice2"]}},
            {"provider": "choice1"},
            {"provider_choices": {"provider": ["choice1", "choice2"]}},
        ),
        (
            {},
            "route2",
            {},
            {"provider": "default_provider"},
            {},
        ),
        (
            {},
            "route3",
            {"provider_choices": {"provider": "existing_provider"}},
            None,
            {"provider_choices": {"provider": "existing_provider"}},
        ),
    ],
)
def test_parameters_builder_update_provider_choices(
    command_coverage, route, kwargs, route_default, expected_result
):
    with patch(
        "openbb_core.app.command_runner.ProviderInterface",
        **{"return_value.available_providers": ["provider1", "provider2"]}
    ):
        result = ParametersBuilder.update_provider_choices(
            mock_func, command_coverage, route, kwargs, route_default
        )

        assert result == expected_result


def test_parameters_builder_validate_kwargs(mock_func):
    """Test validate_kwargs."""

    # TODO: add more test cases with @pytest.mark.parametrize

    result = ParametersBuilder.validate_kwargs(
        mock_func, {"a": 1, "b": "2", "c": 3.0, "d": 4.3}
    )

    assert result == {"a": 1, "b": 2, "c": 3.0, "d": 4, "provider_choices": {}}


def test_parameters_builder_build(mock_func, execution_context):
    """Test build."""

    # TODO: add more test cases with @pytest.mark.parametrize

    with patch(
        "openbb_core.app.command_runner.ProviderInterface",
        **{"return_value.available_providers": ["provider1", "provider2"]}
    ):
        result = ParametersBuilder.build(
            args=[1, 2],
            kwargs={
                "c": 3,
                "d": "4",
                "provider_choices": {"provider": ["provider1", "provider2"]},
            },
            func=mock_func,
            execution_context=execution_context,
            route="mock/route",
        )

        assert result == {
            "a": 1,
            "b": 2,
            "c": 3.0,
            "d": 4,
            "provider_choices": {"provider": ["provider1", "provider2"]},
        }


def test_command_runner():
    """Test command runner."""
    assert CommandRunner()


def test_command_runner_properties():
    """Test properties."""

    sys = SystemSettings()
    user = UserSettings()
    cmd_map = CommandMap()
    runner = CommandRunner(cmd_map, sys, user)

    assert isinstance(runner, CommandRunner)
    assert runner.system_settings == sys
    assert runner.user_settings == user
    assert runner.command_map == cmd_map


def test_command_runner_build():
    runner = CommandRunner()

    with patch(
        "openbb_core.app.command_runner.StaticCommandRunner",
        **{"return_value.run": True}
    ):
        assert runner.run("mock/route")
