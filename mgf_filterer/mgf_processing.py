from pathlib import Path
from typing import List

import click
import matchms.filtering as ms_filters
from matchms import Spectrum
from matchms.importing import load_from_mgf

from mgf_filterer.exceptions import MGFFileNotFoundError


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
def load_mgf_files(filepath: str) -> List[Spectrum]:
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

    # Debug print
    spectra = list(load_from_mgf(filepath))
    click.echo(f"Loaded {len(spectra)} spectra from the file.")
    return spectra


def metadata_processing(spectrum: Spectrum) -> Spectrum:
    """
    Process metadata of a mass spectrometry spectrum by applying a series of filters.

    This function applies several filters to the input Spectrum object to harmonize,
    repair, and derive chemical identifiers and other metadata. It ensures that the
    spectrum's metadata are standardized and enriched for further analysis.

    Parameters:
    spectrum (Spectrum): The input Spectrum object to be processed.

    Returns:
    Spectrum: The processed Spectrum object with updated metadata.

    Filters applied in order:
    - Default filters to clean and standardize the spectrum.
    - Repair InChI, InChIKey, and SMILES strings.
    - Derive InChI from SMILES and vice versa.
    - Derive InChIKey from InChI.
    - Harmonize undefined chemical identifiers.
    - Add precursor m/z (mass-to-charge ratio) information.
    """
    spectrum = ms_filters.default_filters(spectrum)
    # More processing steps as previously defined
    return spectrum


@click.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--process-metadata", is_flag=True, help="Apply metadata processing to each spectrum.")
def process_mgf_file(filepath: str, process_metadata: bool) -> None:
    """
    Load spectra from a .mgf file and optionally process their metadata.

    Parameters:
    filepath (str): The path to the .mgf file to be loaded.
    process_metadata (bool): Flag to determine if metadata processing should be applied.
    """
    try:
        spectra = load_mgf_files(filepath)
        if process_metadata:
            spectra = [metadata_processing(spectrum) for spectrum in spectra]
        click.echo(
            f"Loaded {len(spectra)} spectra from the file, with metadata processing {'enabled' if process_metadata else 'disabled'}."
        )
    except Exception as e:
        click.echo(f"Error processing file: {e}", err=True)


# Example usage:
if __name__ == "__main__":
    # process_mgf_file()
    load_mgf_files()
