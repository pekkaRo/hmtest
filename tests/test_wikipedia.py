"""Test for the wikipedia module."""
from unittest.mock import Mock

import click
import pytest

from hmtest import wikipedia


def test_random_page_uses_given_language(mock_requests_get: Mock) -> None:
    """Assert langauge parameter is passed."""
    wikipedia.random_page(language="fi")
    args, _ = mock_requests_get.call_args
    assert "fi.wikipedia.org" in args[0]


def test_random_page_returns_page(mock_requests_get: Mock) -> None:
    """It returns an instance of Page dataclass."""
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get: Mock) -> None:
    """Exception is raised when invalid json is returned."""
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()
