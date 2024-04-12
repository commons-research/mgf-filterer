from pathlib import Path
from typing import List

import click
from matchms.importing import load_from_mgf

from mgf_filterer.exceptions import MGFFileNotFoundError


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
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
    click.echo(f"Loaded {len(spectra)} spectra from the file.")
    return spectra


# Example usage:
if __name__ == "__main__":
    load_mgf_files()
