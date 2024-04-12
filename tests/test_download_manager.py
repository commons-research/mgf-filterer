from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import requests

from mgf_filterer.download_manager import download_file


# Test successful file download
def test_download_file_success(requests_mock):
    test_url = "https://example.com/testfile.mgf"
    test_content = b"Example file content"
    requests_mock.get(test_url, content=test_content)

    destination_folder = Path("/fake/folder")
    filename = "testfile.mgf"
    dest_path = destination_folder / filename

    # Mock open to not actually write to the filesystem
    with patch("builtins.open", mock_open()) as mocked_file:
        download_file(test_url, destination_folder)

        # Check that the file write was called with the correct content
        mocked_file.assert_called_once_with(dest_path, "wb")
        handle = mocked_file()
        handle.write.assert_called_once_with(test_content)


# Test handling of network errors
def test_download_file_network_error(requests_mock):
    test_url = "https://example.com/testfile.mgf"
    requests_mock.get(test_url, exc=requests.exceptions.ConnectionError)

    with pytest.raises(requests.RequestException):
        download_file(test_url, Path("/fake/folder"))


# Test HTTP error like 404 not found
def test_download_file_http_error(requests_mock):
    test_url = "https://example.com/testfile.mgf"
    requests_mock.get(test_url, status_code=404)

    with pytest.raises(requests.HTTPError):
        download_file(test_url, Path("/fake/folder"))
