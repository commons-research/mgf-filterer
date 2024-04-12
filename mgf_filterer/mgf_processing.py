from pathlib import Path
from typing import List

from matchms.importing import load_from_mgf

from mgf_filterer.exceptions import MGFFileNotFoundError


def load_mgf_files(filepath: str) -> List:
    """
    Load spectra from a .mgf file.

    Parameters:
    filepath (str): The path to the .mgf file to be loaded.

    Returns:
    List[Spectrum]: A list of Spectrum objects loaded from the file.

    Raises:
    MGFFileNotFoundError: If the .mgf file cannot be found.
    """
    if not Path(filepath).exists():
        raise MGFFileNotFoundError(filepath)

    spectra = list(load_from_mgf(filepath))
    return spectra


# Example usage:
if __name__ == "__main__":
    # Replace 'path_to_your_file.mgf' with the actual file path
    spectra = load_mgf_files("path_to_your_file.mgf")
    print(f"Loaded {len(spectra)} spectra from the file.")
