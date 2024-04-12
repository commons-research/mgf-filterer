from pathlib import Path

import pytest

from mgf_filterer.mgf_processing import load_mgf_files


@pytest.fixture
def mgf_file_path():
    # Assuming the test data is in a subdirectory of the tests directory
    return Path(__file__).parent / "testdata" / "erythroxylum_coca.mgf"


def test_load_mgf_files_valid(mgf_file_path):
    """Test loading a valid .mgf file."""
    spectra = list(load_mgf_files(str(Path(__file__).parent / "testdata" / "erythroxylum_coca.mgf")))
    assert len(spectra) == 1098, "No spectra loaded from a valid file."


def test_load_mgf_files_nonexistent():
    """Test loading from a nonexistent file path."""
    with pytest.raises(FileNotFoundError):
        load_mgf_files("nonexistent_file.mgf")


# More tests can be added for different scenarios
