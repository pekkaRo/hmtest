"""Tests for the main application."""
from unittest.mock import Mock

import click.testing
from click.testing import CliRunner
import pytest
from pytest_mock import MockFixture
import requests

from hmtest import console


@pytest.fixture
def runner() -> CliRunner:
    """Returns click test runner."""
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    """Mocks the wikipedia random page."""
    return mocker.patch("hmtest.wikipedia.random_page")


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It returns lorem ipsum in output."""
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    """Its' method gets called."""
    _ = runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It calles english wikipedia as default."""
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_requests_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It exits with exit code 1 if wikipedia throws exception."""
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """Its' output contains error on exception."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    """Its' language option is passed on to the wikipedia module."""
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    """End to end test returns exit code 0."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
