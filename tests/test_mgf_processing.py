from pathlib import Path

import pytest
from click.testing import CliRunner

from mgf_filterer.mgf_processing import load_mgf_files


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mgf_file_path():
    # Assuming the test data is in a subdirectory of the tests directory
    return Path(__file__).parent / "testdata" / "erythroxylum_coca.mgf"


def test_load_mgf_files_valid(runner, mgf_file_path):
    """Test loading a valid .mgf file and check the correct number of spectra."""
    result = runner.invoke(load_mgf_files, [str(mgf_file_path)])
    assert result.exit_code == 0
    expected_number_of_spectra = 1098  # Set this to the number you expect for erythroxylum_coca.mgf
    assert f"Loaded {expected_number_of_spectra} spectra from the file" in result.output


def test_load_mgf_files_nonexistent(runner):
    """Test loading from a nonexistent file path."""
    test_path = "/path/to/nonexistent/mgf_file.mgf"
    result = runner.invoke(load_mgf_files, [test_path])
    assert result.exit_code == 2  # Expecting exit code 2 for Click's missing file handling
    assert "Error:" in result.output
