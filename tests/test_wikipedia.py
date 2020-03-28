from hmtest import wikipedia


def test_random_page_uses_given_language(mock_requests_get):
    wikipedia.random_page(language="fi")
    args, _ = mock_requests_get.call_args
    assert "fi.wikipedia.org" in args[0]
