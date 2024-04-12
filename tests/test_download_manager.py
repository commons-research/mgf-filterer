from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import requests
from click.testing import CliRunner

from mgf_filterer.download_manager import download_file


@pytest.fixture
def runner():
    return CliRunner()


# Test successful file download
def test_download_file_success(runner, requests_mock):
    test_url = "https://example.com/testfile.mgf"
    test_content = b"Example file content"
    requests_mock.get(test_url, content=test_content)
    destination_folder = "/fake/folder"
    filename = "testfile.mgf"
    dest_path = Path(destination_folder) / filename

    with patch("builtins.open", mock_open()) as mocked_file:
        result = runner.invoke(download_file, [test_url, destination_folder])
        assert result.exit_code == 0
        assert "File downloaded successfully" in result.output
        mocked_file.assert_called_once_with(dest_path, "wb")
        handle = mocked_file()
        handle.write.assert_called_once_with(test_content)


# Test handling of network errors
def test_download_file_network_error(runner, requests_mock):
    test_url = "https://example.com/testfile.mgf"
    requests_mock.get(test_url, exc=requests.exceptions.ConnectionError)
    result = runner.invoke(download_file, [test_url, "/fake/folder"])
    assert result.exit_code != 0
    assert "Failed to download the file" in result.output


# Test HTTP error like 404 not found
def test_download_file_http_error(runner, requests_mock):
    test_url = "https://example.com/testfile.mgf"
    requests_mock.get(test_url, status_code=404)
    result = runner.invoke(download_file, [test_url, "/fake/folder"])
    assert result.exit_code != 0
    assert "Failed to download the file" in result.output
